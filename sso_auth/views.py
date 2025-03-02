from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pyotp
import qrcode
import io
import base64
CustomUser = get_user_model()

def verify_2fa_otp(user , otp ):
    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        user.mfa_enabled = True
        user.save()
        return True
    return False

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválidos!")
        return self.render_to_response(self.get_context_data(form=form))

def home(request):
    return render(request, "home.html")

def profile_view(request):   
    user = request.user
    
    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32()
        user.save()
        
    otp_uri = pyotp.totp.TOTP(user.mfa_secret).provisioning_uri(
            name=user.email,
            issuer_name="SSO Auth"
        )

    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    
    
    buffer.seek(0)  
    qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")

    qr_code_data_uri = f"data:image/png;base64,{qr_code}"
    return render(request, 'profile.html', {"qrcode": qr_code_data_uri})

def verify_2fa(request):
    if request.method == 'POST':
        otp = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')
        if not user_id:
            messages.error(request, 'Usuário invalido! Por favor tente novamente.')
            return render(request,'otp_verify.html', {'user_id': user_id})
        
        user = CustomUser.objects.get(id=user_id)
        if verify_2fa_otp(user, otp):
            if request.user.is_authenticated:
                messages.success(request, '2FA ativado com sucesso!')
                return redirect('profile')

            login(request, user)
            messages.success(request, 'Login com sucesso!')
            return redirect('profile')
        else:
            if request.user.is_authenticated:
                messages.error(request, 'Código OTP inválido! Por favor tente novamente.')
                return redirect('profile')
            messages.error(request, 'Código OTP inválido. Por favor tente novamente')
            return render(request,'otp_verify.html', {'user_id': user_id})
       
    return render(request,'otp_verify.html', {'user_id': user_id})

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.mfa_enabled:
                return render(request,'otp_verify.html', {'user_id': user.id})
            login(request, user)
            messages.success(request, 'Login com sucesso!')
            return redirect('profile') 
        else:
            messages.error(request, 'Email ou senha inválida! Por favor tente novamente.')
    return render(request,'login.html')

@login_required
def disable_2fa(request):
    user = request.user
    if user.mfa_enabled:
        user.mfa_enabled = False
        user.save()
        messages.success(request, "A Autenticação de Dois Fatores foi desativada!")
        return redirect('profile')
    else:
        messages.info(request, "2FA já está desativada.")
    return redirect('profile')

@login_required
def logout_page(request):
    logout(request)  
    messages.success(request, 'Você fez o logout com sucesso!') 
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'As senhas estão diferentes. Tente novamente.')
            return render(request, 'signup.html')

        # Check if email is already taken
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email em uso. Tente outro.')
            return render(request, 'signup.html')

        # Create the new user
        user = CustomUser.objects.create_user(username=email, email=email, password=password1)
        user.save()
        messages.success(request, 'Cadastro feito com sucesso! Agora você pode fazer o login.')
        return redirect('login')

    return render(request, 'signup.html')

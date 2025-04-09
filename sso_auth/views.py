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
    next_url = (
        request.GET.get('next') or
        request.session.get('next_url') or
        '/'
    )

    # Se tiver vindo de algum redirect anterior com next, salva de novo
    request.session['next_url'] = next_url
    print(f"[PROFILE_VIEW] next_url = {next_url}")
    
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
    return render(request, 'profile.html', {
        "qrcode": qr_code_data_uri,
        "next": next_url
        })

def verify_2fa(request):
    if request.method == 'POST':
        otp = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')
        next_url = request.POST.get('next') or '/'
        print(f"[VERIFY_2FA - POST] next_url recebido: {next_url}")

        if not user_id:
            messages.error(request, 'Usuário inválido!')
            return render(request,'otp_verify.html', {'user_id': user_id, 'next': next_url})
        
        user = CustomUser.objects.get(id=user_id)
        if verify_2fa_otp(user, otp):
            login(request, user)
            print(f"[VERIFY_2FA - POST] Código válido. Redirecionando para: {next_url}")
            return redirect(next_url)  # redireciona para o "next" original
        else:
            messages.error(request, 'Código OTP inválido.')
            print(f"[VERIFY_2FA - POST] Código inválido. Recarregando OTP com next: {next_url}")
            return render(request,'otp_verify.html', {'user_id': user_id, 'next': next_url})

    # GET request: pega da query string
    user_id = request.GET.get('user_id')
    next_url = request.GET.get('next') or '/'
    print(f"[VERIFY_2FA - GET] Exibindo página OTP com next: {next_url}")
    return render(request, 'otp_verify.html', {'user_id': user_id, 'next': next_url})


def login_page(request):
    next_url = request.GET.get('next') or request.POST.get('next') or request.session.get('next_url') or '/'

    if request.method == 'GET':
        request.session['next_url'] = next_url
        print(f"[LOGIN_PAGE] [GET] next_url salvo na sessão: {next_url}")

    if request.method == 'POST':
        next_url = request.POST.get('next') or request.session.get('next_url') or '/'
        print(f"[LOGIN_PAGE] [POST] Recuperado next_url da sessão ou POST: {next_url}")

        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)

            if not user.mfa_enabled:
                messages.info(request, "Por favor ative o 2FA antes de continuar.")
                return redirect('profile')

            print(f"[LOGIN_PAGE] Redirecionando para verificação de OTP com next: {next_url}")
            return render(request, 'otp_verify.html', {'user_id': user.id, 'next': next_url})

        else:
            messages.error(request, 'Email ou senha inválida! Por favor tente novamente.')

    print(f"[LOGIN_PAGE] Render de GET ou erro - next: {next_url}")
    return render(request,'login.html', {'next': next_url})

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
    next_url = request.GET.get('next') or 'http://localhost:3000'
    return redirect(next_url)

def signup_view(request):
    next_url = (
        request.GET.get('next') or
        request.POST.get('next') or
        request.session.get('next_url') or
        '/'
    )

    if request.method == 'GET':
        request.session['next_url'] = next_url
        print(f"[SIGNUP_PAGE] [GET] next_url salvo na sessão: {next_url}")

    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'As senhas estão diferentes. Tente novamente.')
            return render(request, 'signup.html', {'next': next_url})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email em uso. Tente outro.')
            return render(request, 'signup.html', {'next': next_url})

        user = CustomUser.objects.create_user(username=email, email=email, password=password1)
        user.save()
        messages.success(request, 'Cadastro feito com sucesso! Agora você pode fazer o login.')
        return redirect(f'/login?next={next_url}')

    return render(request, 'signup.html', {'next': next_url})


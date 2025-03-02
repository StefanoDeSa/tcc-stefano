from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválidos.")
        return self.render_to_response(self.get_context_data(form=form))

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, "registration/register.html", {"form": form})

@login_required
def home(request):
    return render(request, "home.html")
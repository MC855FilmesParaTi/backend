import re
from django.forms import Form
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def home(request):
    # HttpResponse("<H1>Seja bem-vindo a filmes pra ti!<H1!><br><hr><br><a href=\"oauth2/logout\">Logout</a><br><a href=\"oauth2/login\">Login</a><br><a href=\"oauth2/login_no_sso\">Login (no SSO)</a>")
    return render(request, "home.html")


def signup(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {
        'form': form
    })

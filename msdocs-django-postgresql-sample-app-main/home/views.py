from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("<H1>Seja bem-vindo a filmes pra ti!<H1!><br><hr><br><a href=\"oauth2/logout\">Logout</a><br><a href=\"oauth2/login\">Login</a><br><a href=\"oauth2/login_no_sso\">Login (no SSO)</a>")

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import redirect, render

from utils.html_content_factory import HomePageFactory

# This class will be called on every request to the server


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        # get_response is a callable that will be called on every request
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is not authenticated (logged in)
        if not request.user.is_authenticated and request.path in ['/']:
            # If not, redirect them to the login page
            return redirect('/login')

        # Otherwise, call the next middleware in the chain
        response = self.get_response(request)

        # Finally, return the response
        return response

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'new/home/login.html', context={'error': 'Error in login or password', 'register': 'register', 'login': 'login'})
    else:
        if request.user.is_authenticated:
            return redirect('/')
        context = {'register': 'register', 'login': 'login'}
        return render(request, 'new/home/login.html', context=context)


def logout(request):
    django_logout(request)
    return redirect('/login')


def register(request):
    # set payload register url to context

    context = {'register': 'register', 'login': 'login'}

    return render(request, 'new/home/register.html', context=context)


def home(request):
    card_page_icon = "/assets/img/icons/icon_group.svg"
    card_page = 'new/components/card_info.html'
    card_page_info = {
        'title': 'Total employee',
        'details': 10, 
        'meta': 'HR', 
        'icon': card_page_icon
        }

    home = HomePageFactory.create_home_page().to_json()

    context = {'register': 'register', 'login': 'login',
               'card_page': card_page, 'card_page_context': card_page_info, 'content': home}
    return render(request, 'eui/main/dashboard.html', context=context)

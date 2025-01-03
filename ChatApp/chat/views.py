from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login

def chatPage(request, *args, **kwargs):
    """
    Renders the chat page. Redirects to the login page if the user is not authenticated.

    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: The rendered chat page or redirection to login.
    """
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    return render(request, "chat/chatPage.html", {})


def registerPage(request):
    """
    Handles user registration. Redirects to the chat page after successful registration and login.

    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: The registration page or redirection to chat after registration.
    """
    if request.user.is_authenticated:
        return redirect('chat-page')  

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat-page')
    else:
        form = RegisterForm()

    return render(request, 'chat/registerPage.html', {'form': form})

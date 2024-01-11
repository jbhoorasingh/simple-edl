from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/gui/login/')
def gui_home(request):
    current_page = 'home_edl'
    current_page_title = "Lists"
    return render(request, 'gui/home.html',
                  {'current_page': current_page,
                   'current_page_title': current_page_title})


# @login_required(login_url='/gui/login/')
# def gui_list_edl(request):
#     current_page = 'gui_list_edl'
#     current_page_title = "Lists"
#     return render(request, 'gui/home.html',
#                   {'current_page': current_page,
#                    'current_page_title': current_page_title})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Replace 'home' with the URL to redirect to after login
    else:
        form = LoginForm()

    return render(request, 'gui/login.html', {'form': form})
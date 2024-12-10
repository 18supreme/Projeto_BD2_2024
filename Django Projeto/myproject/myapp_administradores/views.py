from django.shortcuts import render


def admin_home(request):
    user_id = request.session.get('user_id')

    return render(request, 'admin_home.html')
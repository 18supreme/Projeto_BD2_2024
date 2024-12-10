from django.shortcuts import render


def admin_home(request):
    user_id = request.session.get('user_id')

    return render(request, 'admin_home.html')


def admin_viaturas(request):
    return render(request, 'admin_viaturas.html')


def admin_reservas(request):
    return render(request, 'admin_reservas.html')


def admin_manutencoes(request):
    return render(request, 'admin_manutencoes.html')


def admin_administracao(request):
    return render(request, 'admin_administracao.html')

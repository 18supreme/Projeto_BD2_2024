from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import basededados as bd

def clientes_home(request):
    user_id = request.session.get('user_id')
    
    # Executar a consulta para contar o número total de reservas do utilizador atual
    total_reservas = bd.getTotalReservasByUser(user_id)
    
    # Executar a consulta para obter a percentagem de danos do utilizador atual
    percentagem_danos = bd.getDanosByUser(user_id)

    # Executar a consulta para obter a marca mais usada do utilizador atual
    marca_preferida = bd.getMarcaFavoritaByUser(user_id)
    
    # Executar a consulta para obter o modelo mais usado do utilizador atual
    modelo_preferido = bd.getModeloFavoritaByUser(user_id)
    
    # Executar a consulta para obter a média de KM realizados pelo utilizador atual
    MédiaKmPercorridos = bd.getMedKmByUser(user_id)
    
    # Executar a consulta para obter o total dos KM realizados pelo utilizador atual
    TotalKmPercorridos = bd.getTotalKmByUser(user_id)

    # Executar a consulta para obter as 3 viaturas mais requisitadas
    viaturas_tendencias = bd.getTop3Viaturas()
    
    # Passar os valores para o template
    return render(request, 'clientes_home.html', {
        'total_reservas': 1 if total_reservas else "Sem reservas",
        'percentagem_danos': percentagem_danos if percentagem_danos else "0",
        'marca_preferida': marca_preferida[0] if marca_preferida else "-",
        'modelo_preferido': modelo_preferido[0] if modelo_preferido else "-",
        'mediaKmPercorridos': MédiaKmPercorridos if MédiaKmPercorridos else "0",
        'TotalKmPercorridos': TotalKmPercorridos if TotalKmPercorridos else "0",
        'viaturas': viaturas_tendencias  # Passando a lista de viaturas
    })


def viaturas_list(request):
    
    # Executar a consulta para obter todas as viaturas
    viaturas = bd.getViaturas()
    
    # Retorna a lista de viaturas para o template
    return render(request, 'viaturas_list.html', {'viaturas': viaturas})


def viatura_detail(request, id):
    
    # Executar a consulta para obter os detalhes de uma viatura
    viatura = bd.getDetailViaturaById(id)

    if viatura:
        return render(request, 'viatura_detail.html', {'viatura': viatura})
    else:
        return render(request, 'viatura_detail.html', {'error': 'Viatura não encontrada.'})


def reservas_list(request):
    ID_user = request.session.get('user_id')
    
    # Executar a consulta para todas as reservas do utilizador
    reservas = bd.getListReservaById(ID_user)
    
    # Retorna a lista de viaturas para o template
    return render(request, 'reservas_list.html', {'reservas': reservas})


def criar_reserva(request, viatura_id):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        # Obtendo os valores do formulário
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        # Executar a consulta para todas as reservas do utilizador
        conflito = bd.getconflitoReserva(viatura_id, data_inicio, data_fim)

        if conflito > 0:
            # Se houver conflito, retorna uma mensagem ao usuário
            return HttpResponse("A viatura já está reservada nesse intervalo de datas.", status=400)

        # Se não houver conflito, insere a nova reserva
        bd.CreateNewReserva(data_inicio, data_fim, False, '', 0, viatura_id, user_id, 1)

        # Redireciona para a lista de viaturas
        return redirect('viaturas_list')

    # Se for uma requisição GET, exibe o formulário
    return render(request, 'reserva_form.html')


def reserva_cancelar(request, reserva_id):
    if request.method == 'POST':
        
        # Atualiza o estado da reserva para cancelada
        bd.UpdateReserva(reserva_id, 5)

            # Adicionar mensagem de sucesso
        return redirect('reservas_list')
 
    # Se for uma requisição GET, exibe o formulário
    return render(request, 'reservas_list.html')

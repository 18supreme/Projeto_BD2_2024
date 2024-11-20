from django.shortcuts import render, get_object_or_404, redirect
from .models import Curso
from .forms import CursoForm
from django.contrib import messages
from django.http import HttpResponse
import datetime, json

def curso_list(request):
    cursos = Curso.objects.all()
    return render(request, 'curso_list.html', {'cursos': cursos})

def curso_detail(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'curso_detail.html', {'curso': curso})

def curso_create(request):
    if request.method == "POST":
        try:
            nome = request.POST['nome']
            tipo_curso = int(request.POST['tipo_curso'])
            apresent = request.POST['apresent']
            said_prof = request.POST['said_prof']
            
            # Construir o plano curricular a partir dos dados do formulário
            planocur = []
            disciplinas = request.POST.getlist('disciplina')
            sems = request.POST.getlist('sem')
            anos = request.POST.getlist('ano')
            hts = request.POST.getlist('ht')
            
            for i in range(len(disciplinas)):
                planocur.append({
                    "des": disciplinas[i],
                    "sem": int(sems[i]),
                    "ano": int(anos[i]),
                    "ht": int(hts[i])
                })
                
            avqual = request.POST.get('avqual', '').split(',')
            avqual = list(map(int, filter(None, avqual)))  # Ignora entradas vazias
            
            # Processamento automático de "outr_inf"
            outr_inf = {}  # Usamos um dicionário vazio por padrão
            outr_inf['observacoes'] = request.POST.get('outr_inf', '')  # A entrada do usuário se torna uma observação
            outr_inf['data_criacao'] = str(datetime.datetime.now())  # Adiciona a data de criação
            # Você pode adicionar mais campos padrão aqui, se necessário
            
            # Cria uma nova instância do modelo Curso
            curso = Curso(
                nome=nome,
                tipo_curso=tipo_curso,
                apresent=apresent,
                said_prof=said_prof,
                planocur=planocur,
                avqual=avqual,
                outr_inf=outr_inf
            )
            curso.save()  # Salva o curso no banco de dados

            return redirect('curso_list')  # Redireciona para a lista de cursos após a criação
        except Exception as e:
            print(f"Erro ao criar curso: {e}")  # Exibe o erro no console
            return HttpResponse("Erro ao criar curso.")  # Retorna uma mensagem de erro ao usuário
    return render(request, 'curso_create.html')  # Renderiza o formulário se não for uma solicitação POST

def curso_update(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == "POST":
        try:
            nome = request.POST['nome']
            tipo_curso = int(request.POST['tipo_curso'])
            apresent = request.POST['apresent']
            said_prof = request.POST['said_prof']
            
            # Atualiza o plano curricular
            planocur = []
            for i in range(len(request.POST.getlist('planocur_des'))):
                disciplina = {
                    'des': request.POST.getlist('planocur_des')[i],
                    'sem': int(request.POST.getlist('planocur_sem')[i]),
                    'ano': int(request.POST.getlist('planocur_ano')[i]),
                    'ht': int(request.POST.getlist('planocur_ht')[i]),
                }
                planocur.append(disciplina)

            avqual = list(map(int, request.POST['avqual'].split(',')))  # Converte as notas de avaliação para uma lista de inteiros
            
            # Atualiza outras informações
            outr_inf = {
                'observacoes': request.POST['outr_inf']
            }

            # Atualiza os campos do curso
            curso.nome = nome
            curso.tipo_curso = tipo_curso
            curso.apresent = apresent
            curso.said_prof = said_prof
            curso.planocur = planocur
            curso.avqual = avqual
            curso.outr_inf = outr_inf

            curso.save()  # Salva as alterações no banco de dados

            return redirect('curso_list')  # Redireciona para a lista de cursos
        except Exception as e:
            print(f"Erro ao atualizar curso: {e}")
            return HttpResponse("Erro ao atualizar curso.")  # Retorna uma mensagem de erro ao usuário

    return render(request, 'curso_update.html', {'curso': curso})  # Renderiza o formulário de edição

def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == "POST":
        curso.delete()
        return redirect('curso_list')
    return render(request, 'curso_confirm_delete.html', {'curso': curso})

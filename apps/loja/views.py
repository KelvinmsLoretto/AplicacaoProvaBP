from django.http import HttpResponse
from .models import Produto
from django.shortcuts import render
from django.shortcuts import redirect
from apps.clientes.models import Cliente 
from apps.emprestimos.models import Emprestimo 

def index(request):
    return HttpResponse("Bem-vindo à página inicial!")

def cliente(request):
    return HttpResponse("Página de clientes!")

def emprestimos(request):
    return HttpResponse("Página de empréstimos!")

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'loja/listar_produtos.html', {'produtos': produtos})

def deletar_todos_clientes(request):
    Cliente.objects.all().delete()  
    return redirect('nome_da_view_principal')  

def deletar_todos_emprestimos(request):
    Emprestimo.objects.all().delete()
    return redirect('nome_da_view_principal')


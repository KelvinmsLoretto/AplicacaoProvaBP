from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('cliente', views.cliente, name='cliente'),  
    path('emprestimos', views.emprestimos, name='emprestimos'),  
    path('produtos', views.listar_produtos, name='listar_produtos'),
    path('deletar-clientes/', views.deletar_todos_clientes, name='deletar_todos_clientes'),
    path('deletar-emprestimos/', views.deletar_todos_emprestimos, name='deletar_todos_emprestimos'),
]

from django.urls import path
from .views import EmprestimoViewSet

urlpatterns = [
    path('clientes/<str:cpf>/emprestimos/', EmprestimoViewSet.as_view({'get': 'buscar_por_cpf'}), name='buscar-emprestimo'),
    path('clientes/<str:pk>/emprestimos/simular/', EmprestimoViewSet.as_view({'post': 'simular_emprestimo'}), name='simular-emprestimo'),
    path('clientes/<str:pk>/emprestimos/criar/', EmprestimoViewSet.as_view({'post': 'criar_emprestimo'}), name='criar-emprestimo'),
    path('<uuid:uuid>/aprovar/', EmprestimoViewSet.as_view({'get': 'aprovar_emprestimo'}), name='aprovar-emprestimo'),
]

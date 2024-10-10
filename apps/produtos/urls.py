from django.urls import path
from apps.produtos.views import ProdutoViewSet

urlpatterns = [
    path('produtos/', ProdutoViewSet.as_view({'get': 'buscar_produtos'}), name='buscar-produtos'),
    path('produto/create', ProdutoViewSet.as_view({'post': 'create'}), name='criar-produto'),
    path('produto/update/<int:pk>/', ProdutoViewSet.as_view({'put': 'update'}), name='atualizar-produto'),
    path('produto/deletar/<int:pk>/', ProdutoViewSet.as_view({'delete': 'delete'}), name='deletar-produto'),
    path('produtos/importar', ProdutoViewSet.as_view({'get': 'importar_dados_do_site'}), name='importar-produto-do-site'),
    path('produtos/exportar-produtos-csv/', ProdutoViewSet.as_view({'get': 'export_produtos_csv'}), name='export_produtos_csv'),
]

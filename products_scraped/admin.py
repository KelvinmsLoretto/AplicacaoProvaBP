from django.contrib import admin
from .models import ProductScraped

@admin.register(ProductScraped)
class ProductScrapedAdmin(admin.ModelAdmin):
    """
    Configuração do admin para ProductScraped
    """
    list_display = ['nome', 'preco', 'fonte', 'data_coleta']
    list_filter = ['fonte', 'data_coleta']
    search_fields = ['nome', 'descricao']
    readonly_fields = ['data_coleta']
    
    fieldsets = (
        ('Informações do Produto', {
            'fields': ('nome', 'descricao', 'preco')
        }),
        ('Metadados', {
            'fields': ('fonte', 'data_coleta'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Ordena por data de coleta mais recente"""
        return super().get_queryset(request).order_by('-data_coleta')

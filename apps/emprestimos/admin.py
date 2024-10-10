from django.contrib import admin
from .models import Emprestimo

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'valor_solicitado', 'taxa_juros', 'num_parcelas', 'valor_total', 'aprovado', 'data_solicitacao')
    search_fields = ('cliente__nome', 'id')
    list_filter = ('aprovado', 'num_parcelas')
    ordering = ('-data_solicitacao',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for emprestimo in queryset:
            emprestimo.calcular_valor_total()
            emprestimo.calcular_valor_parcela()
        return queryset

    def save_model(self, request, obj, form, change):
        if not change:  # Se for um novo empréstimo, calcula o valor total e da parcela
            obj.calcular_valor_total()
            obj.calcular_valor_parcela()
        super().save_model(request, obj, form, change)

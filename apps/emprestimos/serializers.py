from rest_framework import serializers
from .models import Emprestimo
from apps.clientes.serializers import ClienteSerializer

class SimularEmprestimoSerializer(serializers.Serializer):
    valor_solicitado = serializers.DecimalField(max_digits=10, decimal_places=2)
    taxa_juros = serializers.DecimalField(max_digits=5, decimal_places=2)
    num_parcelas = serializers.IntegerField()

    def validate_num_parcelas(self, value):
        if value <= 0:
            raise serializers.ValidationError("O número de parcelas deve ser maior que 0.")
        return value

    
class EmprestimoSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        cliente = self.context['cliente']
        
        numero_emprestimos = Emprestimo.objects.filter(cliente=cliente).count()
        if numero_emprestimos >= 1:
            raise serializers.ValidationError("O cliente já possui o número máximo de empréstimos permitidos.")

        emprestimo = Emprestimo(
            cliente=cliente,
            valor_solicitado=data['valor_solicitado'],
            taxa_juros=data['taxa_juros'],
            num_parcelas=data['num_parcelas']
        )

        valor_total = emprestimo.calcular_valor_total()

        if valor_total <= 0:
            raise serializers.ValidationError("Simulação inválida. O valor total do empréstimo deve ser maior que zero.")
        
        if valor_total >= 10000:
            raise serializers.ValidationError("Simulação inválida. O valor total do empréstimo deve ser entre 1 e 10000.")
        
        valor_parcela = emprestimo.calcular_valor_parcela()

        if valor_parcela <= 0:
            raise serializers.ValidationError("O valor da parcela deve ser maior que zero.")
        
        # Validação da taxa de juros
        taxa_juros = float(data['taxa_juros'])
        if taxa_juros < 3.14 or taxa_juros > 6:
            raise serializers.ValidationError("A taxa de juros deve estar entre 3.14% e 6.5%.")


        data['valor_total'] = valor_total
        data['valor_parcela'] = valor_parcela

        return data

    class Meta:
        model = Emprestimo
        exclude = ['cliente']

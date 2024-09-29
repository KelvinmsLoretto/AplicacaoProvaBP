from rest_framework import serializers
from .models import Cliente, DadosPessoais, ContaBancaria

class DadosPessoaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosPessoais
        fields = ['cep', 'rua', 'uf', 'numero', 'bairro']

class ContaBancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaBancaria
        fields = ['numero_conta', 'dv_conta', 'agencia', 'dv_agencia']

class ClienteSerializer(serializers.ModelSerializer):
    dados_pessoais = DadosPessoaisSerializer(many=True, required=False)
    conta_bancaria = ContaBancariaSerializer(many=False, required=False)

    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'beneficio', 'estado_civil', 'sexo', 
                  'nome_mae', 'nome_pai', 'email', 'dados_pessoais', 'conta_bancaria']

    def create(self, validated_data):
        # Tente extrair dados pessoais e conta bancária, usando valores padrão se não estiverem presentes
        dados_pessoais_data = validated_data.pop('dados_pessoais', None)
        conta_bancaria_data = validated_data.pop('conta_bancaria', None)

        # Verifique se os dados pessoais foram fornecidos e se são válidos
        if dados_pessoais_data:
            dados_pessoais_serializer = DadosPessoaisSerializer(data=dados_pessoais_data, many=True)
            if not dados_pessoais_serializer.is_valid():
                raise serializers.ValidationError(dados_pessoais_serializer.errors)
        else:
            dados_pessoais_serializer = None  # Caso não haja dados pessoais

        # Verifique se a conta bancária foi fornecida e se é válida
        if conta_bancaria_data:
            conta_bancaria_serializer = ContaBancariaSerializer(data=conta_bancaria_data)
            if not conta_bancaria_serializer.is_valid():
                raise serializers.ValidationError(conta_bancaria_serializer.errors)
        else:
            conta_bancaria_serializer = None  # Caso não haja conta bancária

        # Agora, crie o cliente
        cliente = Cliente.objects.create(**validated_data)

        # Se dados pessoais foram fornecidos, salve-os
        if dados_pessoais_serializer:
            dados_pessoais_serializer.save(cliente=cliente)

        # Se conta bancária foi fornecida, salve-a
        if conta_bancaria_serializer:
            conta_bancaria_serializer.save(cliente=cliente)

        return cliente


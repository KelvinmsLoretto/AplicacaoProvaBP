from rest_framework import serializers
from apps.produtos.models import Produto

class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco']

    def create(self, validated_data):
        return Produto.objects.create(**validated_data)

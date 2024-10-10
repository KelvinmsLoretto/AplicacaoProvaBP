import requests
import re
import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.produtos.models import Produto
from apps.produtos.serializers import ProdutosSerializer
import csv
from django.http import HttpResponse

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutosSerializer

    def buscar_produtos(self, request):
        produtos = Produto.objects.all()
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            produto = Produto.objects.get(pk=pk)
        except Produto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(produto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            produto = Produto.objects.get(pk=pk)
        except Produto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def importar_dados_do_site(self, request):
        login_url = 'https://www.saucedemo.com/'
        inventory_url = 'https://www.saucedemo.com/static/js/main.018d2d1e.chunk.js'
        login_payload = {
            'user-name': 'standard_user',
            'password': 'secret_sauce'
        }
        
        with requests.Session() as session:
            session.post(login_url, data=login_payload)
            response = session.get(inventory_url)
            content = response.text

            if content:
                parts = content.split('D=[')
                extracted_data = []
                for part in parts[1:]:
                    parted_json = part.split(']')[0]
                    items = parted_json.split('},')
                    for item in items:
                        item = item.replace("}", "") + '}'
                        item = re.sub(r'(\w+):', r'"\1":', item)
                        item_dict = json.loads(item)

                        extracted_data.append({
                            'nome': item_dict['name'],
                            'descricao': item_dict['desc'],
                            'preco': item_dict['price']
                        })

                for data in extracted_data:
                    Produto.objects.create(**data)

            return Response(status=status.HTTP_201_CREATED)
        
    def export_produtos_csv(self, request):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="produtos.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Nome', 'Descrição', 'Preço'])

        produtos = Produto.objects.all()
        for produto in produtos:
            writer.writerow([produto.id, produto.nome, produto.descricao, produto.preco])
        return response
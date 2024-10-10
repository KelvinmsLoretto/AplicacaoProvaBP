import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.produtos.models import Produto

class ProdutoViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.produto_data = {
            'nome': 'Produto Teste',
            'descricao': 'Descrição do Produto Teste',
            'preco': '10.00'
        }
        self.produto = Produto.objects.create(**self.produto_data)

    def test_buscar_produtos(self):
        response = self.client.get('/api/v1/produtos/produtos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['nome'], self.produto_data['nome'])

    def test_criar_produto(self):
        produto_data = {
            'nome': 'Novo Produto',
            'descricao': 'Descrição do Novo Produto',
            'preco': '20.00'
        }
        response = self.client.post('/api/v1/produtos/produto/create', data=json.dumps(produto_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 2)
        self.assertEqual(Produto.objects.get(id=2).nome, produto_data['nome'])

    def test_atualizar_produto(self):
        updated_data = {
            'nome': 'Produto Atualizado',
            'descricao': 'Descrição Atualizada',
            'preco': '15.00'
        }
        response = self.client.put(f'/api/v1/produtos/produto/update/{self.produto.id}/', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, updated_data['nome'])

    def test_deletar_produto(self):
        response = self.client.delete(f'/api/v1/produtos/produto/deletar/{self.produto.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Produto.objects.count(), 0)

    def test_importar_dados_do_site(self):
        response = self.client.request('/api/v1/produtos/produtos/importar')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
        self.assertGreater(Produto.objects.count(), 0)

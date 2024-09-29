from .serializers import EmprestimoSerializer, SimularEmprestimoSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Cliente, Emprestimo
from drf_yasg import openapi

class EmprestimoViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="Buscar por emprestimos de um cliente",
        responses={
            200: openapi.Response('Simulação realizada com sucesso', SimularEmprestimoSerializer),            
            }
    )
    def buscar_por_cpf(self, request, cpf=None):
        try:
            cliente = Cliente.objects.get(cpf=cpf)
        except Cliente.DoesNotExist:
            return Response({"erro": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        emprestimos = Emprestimo.objects.filter(cliente=cliente)

        serializer = EmprestimoSerializer(emprestimos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def aprovar_emprestimo(self, request, uuid=None):
        try:
            # Obtém o empréstimo pelo UUID
            emprestimo = Emprestimo.objects.get(id=uuid)
        except Emprestimo.DoesNotExist:
            return Response({"erro": "Empréstimo não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Aprova o empréstimo
        emprestimo.aprovado = True
        emprestimo.save()

        # Serializa o objeto do empréstimo
        emprestimo_serializado = EmprestimoSerializer(emprestimo)

        # Retorna os dados do empréstimo aprovado
        return Response(emprestimo_serializado.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
        operation_description="Simula o valor total de um empréstimo",
        request_body=SimularEmprestimoSerializer,
        responses={200: openapi.Response('Simulação realizada com sucesso', SimularEmprestimoSerializer)}
    )
    def simular_emprestimo(self, request, pk=None):
        cliente = Cliente.objects.get(pk=pk)
        serializer = EmprestimoSerializer(data=request.data, context={'cliente': cliente})

        if serializer.is_valid():
            emprestimo = Emprestimo(
                cliente=cliente,
                valor_solicitado=serializer.validated_data['valor_solicitado'],
                taxa_juros=serializer.validated_data['taxa_juros'],
                num_parcelas=serializer.validated_data['num_parcelas']
            )

            valor_solicitado = serializer.validated_data['valor_solicitado']
            taxa_juros = serializer.validated_data['taxa_juros']
            num_parcelas = serializer.validated_data['num_parcelas']
            valor_total = emprestimo.calcular_valor_total()
            valor_parcela = emprestimo.calcular_valor_parcela()

            return Response({
                'valor_solicitado': valor_solicitado,
                'taxa_juros': taxa_juros,
                'num_parcelas': num_parcelas,
                'valor_total': valor_total,
                'valor_parcela': valor_parcela
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Simula o valor total de um empréstimo e salva",
        request_body=SimularEmprestimoSerializer,
        responses={200: openapi.Response('Simulação realizada com sucesso', SimularEmprestimoSerializer)}
    )
    def criar_emprestimo(self, request, pk=None):
        cliente = Cliente.objects.get(pk=pk)
        serializer = EmprestimoSerializer(data=request.data, context={'cliente': cliente})

        if serializer.is_valid():
            # Criar e salvar o empréstimo
            emprestimo = Emprestimo(
                cliente=cliente,
                valor_solicitado=serializer.validated_data['valor_solicitado'],
                taxa_juros=serializer.validated_data['taxa_juros'],
                num_parcelas=serializer.validated_data['num_parcelas']
            )
            emprestimo.calcular_valor_total()
            emprestimo.calcular_valor_parcela()
            emprestimo.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



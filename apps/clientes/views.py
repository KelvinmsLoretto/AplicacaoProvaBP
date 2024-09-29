from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().prefetch_related('dados_pessoais', 'conta_bancaria')
    serializer_class = ClienteSerializer

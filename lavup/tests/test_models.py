from django.test import TestCase

from lavup.models import Cliente


class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome="João Silva", whatsapp="11999998888")

    def test_criacao_cliente(self):
        """Teste básico de criação de cliente"""
        self.assertEqual(self.cliente.nome, "João Silva")
        self.assertEqual(self.cliente.whatsapp, "11999998888")
        self.assertTrue(self.cliente.created_at)

    def test_str_representation(self):
        """Teste da representação em string do modelo"""
        self.assertEqual(str(self.cliente), "João Silva")

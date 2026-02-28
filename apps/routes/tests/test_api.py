from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class RouteAPITestCase(TestCase):
    """
    Pruebas básicas para la API de rutas.
    """

    def setUp(self):
        """Configurar datos de prueba."""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Autenticar cliente
        self.client.force_authenticate(user=self.user)

    def test_routes_list_endpoint(self):
        """Probar que el endpoint de listar rutas funciona."""
        response = self.client.get('/api/routes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_health_check(self):
        """Probar que la API responde."""
        response = self.client.get('/api/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_authentication_required(self):
        """Probar que endpoints requieren autenticación."""
        # Desautenticar
        self.client.force_authenticate(user=None)
        
        response = self.client.get('/api/routes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_route_statuses_endpoint(self):
        """Probar que el endpoint de estados funciona."""
        response = self.client.get('/api/route-statuses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_priorities_endpoint(self):
        """Probar que el endpoint de prioridades funciona."""
        response = self.client.get('/api/priorities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_locations_endpoint(self):
        """Probar que el endpoint de ubicaciones funciona."""
        response = self.client.get('/api/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

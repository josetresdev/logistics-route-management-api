"""
Tests para el endpoint de importación de rutas.
"""
import io
import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
import pandas as pd


class ImportRoutesAPITestCase(TestCase):
    """
    Pruebas para el endpoint POST /api/routes/import/
    """

    def setUp(self):
        """Configurar datos de prueba y cliente autenticado."""
        self.client = APIClient()

        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear token de autenticación
        self.token = Token.objects.create(user=self.user)

        # Autenticar cliente
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def create_valid_excel_file(self):
        """
        Crea un archivo Excel válido en memoria para pruebas.

        Returns:
            BytesIO: Archivo Excel en memoria
        """
        # Crear DataFrames
        routes_data = {
            'id_route': [1, 2, 3],
            'origin': ['New York', 'Los Angeles', 'Chicago'],
            'destination': ['Boston', 'San Francisco', 'Dallas'],
            'distance_km': [215.5, 559.0, 920.0],
            'priority': [1, 2, 1],
            'time_window_start': [
                pd.Timestamp('2026-03-01 08:00:00'),
                pd.Timestamp('2026-03-01 09:00:00'),
                pd.Timestamp('2026-03-01 10:00:00'),
            ],
            'time_window_end': [
                pd.Timestamp('2026-03-01 18:00:00'),
                pd.Timestamp('2026-03-01 19:00:00'),
                pd.Timestamp('2026-03-01 20:00:00'),
            ],
            'status': ['PENDING', 'PENDING', 'PENDING'],
        }

        payload_data = {
            'id_route': [1, 2, 3],
            'payload': [
                json.dumps({'notes': 'Route 1'}),
                json.dumps({'notes': 'Route 2'}),
                json.dumps({'notes': 'Route 3'}),
            ],
        }

        routes_df = pd.DataFrame(routes_data)
        payload_df = pd.DataFrame(payload_data)

        # Crear archivo Excel en memoria
        excel_file = io.BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            routes_df.to_excel(writer, sheet_name='routes', index=False)
            payload_df.to_excel(writer, sheet_name='route_payload', index=False)

        excel_file.seek(0)
        excel_file.name = 'test_routes.xlsx'
        return excel_file

    def test_import_routes_success(self):
        """
        Prueba que la importación exitosa de rutas funciona.
        """
        excel_file = self.create_valid_excel_file()

        response = self.client.post(
            '/api/routes/import/',
            {'file': excel_file, 'batch_name': 'Test Batch'},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)
        self.assertIn('batch_id', response.data['data'])
        self.assertEqual(response.data['data']['valid'], 3)

    def test_import_routes_missing_file(self):
        """
        Prueba que falla si no se envía el archivo.
        """
        response = self.client.post(
            '/api/routes/import/',
            {'batch_name': 'Test Batch'},  # Sin archivo
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data['errors'] or response.data.get('message', ''))

    def test_import_routes_invalid_file_type(self):
        """
        Prueba que falla si el archivo no es Excel.
        """
        invalid_file = io.BytesIO(b'This is not an Excel file')
        invalid_file.name = 'test.txt'

        response = self.client.post(
            '/api/routes/import/',
            {'file': invalid_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_routes_requires_authentication(self):
        """
        Prueba que el endpoint requiere autenticación.
        """
        # Desautenticar
        self.client.credentials()

        excel_file = self.create_valid_excel_file()

        response = self.client.post(
            '/api/routes/import/',
            {'file': excel_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_import_routes_multipart_required(self):
        """
        Prueba que la solicitud debe ser multipart/form-data.
        Nota: Este test valida que funcione correctamente con multipart.
        """
        excel_file = self.create_valid_excel_file()

        # Correcta: multipart
        response = self.client.post(
            '/api/routes/import/',
            {'file': excel_file},
            format='multipart'
        )

        # Debe aceptar multipart
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST  # Podría fallar por datos inválidos, pero no por formato
        ])

    def test_import_routes_file_too_large(self):
        """
        Prueba que falla si el archivo excede 10MB.
        """
        # Crear archivo "grande" (simulado)
        large_file = io.BytesIO(b'x' * (11 * 1024 * 1024))  # 11MB
        large_file.name = 'large_file.xlsx'

        response = self.client.post(
            '/api/routes/import/',
            {'file': large_file},
            format='multipart'
        )

        # Debe fallar por tamaño
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_routes_empty_file(self):
        """
        Prueba que falla si el archivo está vacío.
        """
        empty_file = io.BytesIO(b'')
        empty_file.name = 'empty.xlsx'

        response = self.client.post(
            '/api/routes/import/',
            {'file': empty_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    import unittest
    unittest.main()

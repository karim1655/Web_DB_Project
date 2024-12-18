import os
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from web_app.models import Course, Attendance, File, CustomUser
from django.utils import timezone
from web_db_project import settings

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Creazione di un utente personalizzato
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='pAssWord123',
            email='testuser@example.com',
            user_type='person'
        )

        # Creazione di un Quality Manager
        self.quality_manager = CustomUser.objects.create_user(
            username='manager',
            password='pAssWord123',
            email='manager@example.com',
            user_type='quality_manager'
        )

        # Creazione di un corso
        self.course = Course.objects.create(
            year=2024,
            course_n="C001",
            course_name="Test Course",
            planned_date=timezone.now(),
            effective_date=timezone.now(),
            type="Technical",
            start="Start Test",
            check_review="Pending",
            end="End Test",
            duration=10.5,
            i_e="Internal",
            trainer="Test Trainer",
            cost=500,
            requirement="Basic Knowledge"
        )

    def test_login_view(self):
        """Test login view"""
        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'pAssWord123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect dopo il login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_course_list_view(self):
        """Test visualizzazione lista corsi"""
        self.client.login(username='testuser', password='pAssWord123')
        response = self.client.get(reverse('courses'))  # Corretto da 'course_list'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.course_name)

    def test_course_detail_view(self):
        """Test visualizzazione dettagli corso"""
        self.client.login(username='testuser', password='pAssWord123')
        response = self.client.get(reverse('course_detail', kwargs={'pk': self.course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.course_name)

    def test_create_course_view(self):
        """Test creazione corso da parte del Quality Manager"""
        self.client.login(username='manager', password='pAssWord123')
        response = self.client.post(reverse('course_create'), {
            'year': 2024,
            'course_n': 'C002',
            'course_name': 'New Test Course',
            'planned_date': '2024-02-01T10:00',
            'effective_date': '2024-02-10T10:00',
            'type': 'Technical',
            'start': 'Start New Test',
            'check_review': 'Pending',
            'end': 'End New Test',
            'duration': 8,
            'i_e': 'External',
            'trainer': 'Another Trainer',
            'cost': 600,
            'requirement': 'Advanced Knowledge'
        })
        self.assertEqual(response.status_code, 302)  # Redirect dopo creazione
        self.assertTrue(Course.objects.filter(course_name="New Test Course").exists())

    def test_search_view(self):
        """Test ricerca corsi"""
        self.client.login(username='testuser', password='pAssWord123')
        response = self.client.get(reverse('search'), {
            'course_name': self.course.course_name
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.course_name)



# Directory temporanea per i file dei test
TEST_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'files')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FilesTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Creazione di un utente personalizzato
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='pAssWord123',
            email='testuser@example.com',
            user_type='person'
        )

        # Creazione di un corso
        self.course = Course.objects.create(
            year=2024,
            course_n="C001",
            course_name="Test Course",
            planned_date=timezone.now(),
            effective_date=timezone.now(),
            type="Technical",
            start="Start Test",
            check_review="Pending",
            end="End Test",
            duration=10.5,
            i_e="Internal",
            trainer="Test Trainer",
            cost=500,
            requirement="Basic Knowledge"
        )

    def tearDown(self):
        """Rimuove i file creati durante i test."""
        for root, dirs, files in os.walk(TEST_MEDIA_ROOT):
            for file in files:
                os.remove(os.path.join(root, file))


    def test_file_upload_view(self):
        """Test upload file associato a un corso"""
        test_file_path = os.path.join(TEST_MEDIA_ROOT, 'testfile.txt')

        # Creazione di un file temporaneo per il test
        with open(test_file_path, 'w') as f:
            f.write('Test File Content')

        with open(test_file_path, 'rb') as f:
            self.client.login(username='testuser', password='pAssWord123')
            response = self.client.post(reverse('upload_file', kwargs={'pk': self.course.id}), {
                'file': f
            })

        # Controlla il redirect
        self.assertEqual(response.status_code, 302)

        # Controlla che il file sia salvato
        self.assertTrue(File.objects.filter(course_id=self.course.id).exists())

        # Controlla che il file sia salvato nella directory corretta
        uploaded_file = File.objects.get(course_id=self.course.id)
        uploaded_file_path = os.path.join(TEST_MEDIA_ROOT, 'uploads', uploaded_file.file.name.split('/')[-1])
        self.assertTrue(os.path.exists(uploaded_file_path))


    def test_create_course_view_as_normal_user(self):
        """Test che verifica che un normale utente non possa creare corsi"""
        self.client.login(username='testuser', password='pAssWord123')
        response = self.client.post(reverse('course_create'), {
            'year': 2024,
            'course_n': 'C004',
            'course_name': 'Unauthorized User Test Course',
            'planned_date': '2024-04-01T10:00',
            'effective_date': '2024-04-10T10:00',
            'type': 'Technical',
            'start': 'Start Unauthorized Test',
            'check_review': 'Pending',
            'end': 'End Unauthorized Test',
            'duration': 15,
            'i_e': 'External',
            'trainer': 'Test Unauthorized',
            'cost': 900,
            'requirement': 'No Requirement'
        })
        self.assertEqual(response.status_code, 403)  # Accesso negato
        self.assertFalse(Course.objects.filter(course_name="Unauthorized User Test Course").exists())




class ViewTests1(TestCase):
    def setUp(self):
        # Creazione di utenti con ruoli diversi
        self.quality_manager = CustomUser.objects.create_user(username="manager", password="password", user_type="quality_manager")
        self.person = CustomUser.objects.create_user(username="person", password="password", user_type="person")

        # Creazione di un corso
        self.course = Course.objects.create(course_name="Test Course", )

    def test_access_denied_for_unauthenticated_users(self):
        """Test che verifica che gli utenti non autenticati non possano accedere a determinate views."""
        response = self.client.get(reverse("course_create"))
        self.assertNotEqual(response.status_code, 200)  # Dovrebbe essere un redirect o 403

    def test_access_denied_for_unauthorized_users(self):
        """Test che verifica che gli utenti senza permessi non possano accedere a views protette."""
        self.client.login(username="person", password="password")
        response = self.client.get(reverse("course_delete", args=[self.course.id]))
        self.assertEqual(response.status_code, 403)  # Accesso negato

    def test_context_data_in_home_view(self):
        response = self.client.get(reverse('home'))  # Usa la URL corretta
        self.assertEqual(response.status_code, 200)
        # Aggiorna il nome chiave per il contesto
        self.assertIn("planned", response.context)

    def test_redirect_after_course_creation(self):
        """Test che verifica il redirect corretto dopo la creazione di un corso."""
        self.client.login(username="manager", password="password")
        response = self.client.post(reverse("course_create"), {"course_name": "New Course"})
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Course.objects.filter(course_name="New Course").exists())

    def test_role_specific_behavior(self):
        """Test che verifica che solo determinati ruoli possano accedere a specifiche funzionalità."""
        self.client.login(username="person", password="password")
        response = self.client.get(reverse("course_create"))
        self.assertEqual(response.status_code, 403)  # Accesso negato

        self.client.login(username="manager", password="password")
        response = self.client.get(reverse("course_create"))
        self.assertEqual(response.status_code, 200)  # Accesso consentito

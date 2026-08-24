from django.core.management.base import BaseCommand
from core.models import Category, Seminar
from accounts.models import User
from django.utils import timezone
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.core.files import File

seminars = [
    {
        'title': 'Django Backend Development',
        'description': 'Learn how to build web applications with Django and Python.',
        'price': 6000000,
        'location': 'Tehran',
        'is_public': True,
        'is_inperson': True,
        'session_start': timezone.now() + timedelta(days=7),
        'session_end': timezone.now() + timedelta(days=7, hours=2),
        'category': 'Programming',
        'image': 'django.png',
    },
    {
        'title': 'Python Programming Basics',
        'description': 'Learn the fundamentals of Python programming from scratch.',
        'price': 8000000,
        'location': 'Online',
        'is_public': True,
        'is_inperson': False,
        'session_start': timezone.now() - timedelta(hours=2),
        'session_end': timezone.now() + timedelta(hours=2),
        'category': 'Programming',
        'image': 'python.png',
    },
    {
        'title': 'UI/UX Design Workshop',
        'description': 'Learn the fundamentals of modern UI and UX design.',
        'price': 7500000,
        'location': 'Tehran',
        'is_public': False,
        'is_inperson': True,
        'session_start': timezone.now() - timedelta(days=2, hours=4),
        'session_end': timezone.now() - timedelta(days=2),
        'category': 'Design',
        'image': 'ui-ux.jpeg',
    },
]

class Command(BaseCommand):
    help = 'Seed initial data into the database'

    seed_images_dir = Path(settings.BASE_DIR) / 'seed_data' / 'seminar_images'

    def handle(self, *args, **options):
        categories = [
            'Programming',
            'Artificial Intelligence',
            'Web Development',
            'Mobile Development',
            'Data Science',
            'Cybersecurity',
            'Business',
            'Marketing',
            'Design',
            'Personal Development',
            'Finance',
            'Health & Wellness',
            'Other',
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)

        teacher, created = User.objects.get_or_create(
            username='seed_teacher',
            defaults={
                'first_name': 'seed',
                'last_name': 'teacher',
                'email': 'seed_teacher@gmail.com',
            }
        )

        if created:
            teacher.set_password('seed_teacher_password')
            teacher.save()

        for seminar_data in seminars:
            category = Category.objects.get(name=seminar_data['category'])
            image_path = self.seed_images_dir / seminar_data['image']

            if not image_path.exists():
                self.stdout.write(self.style.ERROR(f'Seed image not found: {seminar_data['image']}'))
                return

            with image_path.open('rb') as image_file:
                seminar, created = Seminar.objects.get_or_create(
                    title = seminar_data['title'],
                    defaults={
                        'teacher': teacher,
                        'description': seminar_data['description'],
                        'price': seminar_data['price'],
                        'location': seminar_data['location'],
                        'is_public': seminar_data['is_public'],
                        'is_inperson': seminar_data['is_inperson'],
                        'session_start': seminar_data['session_start'],
                        'session_end': seminar_data['session_end'],
                        'category': category,
                    }
                )

                if created:
                    seminar.image.save(seminar_data['image'], File(image_file), save=True)

        self.stdout.write(self.style.SUCCESS('categories, seed_teacher and seminars seeded successfully!'))
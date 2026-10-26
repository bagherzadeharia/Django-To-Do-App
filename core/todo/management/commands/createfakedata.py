import random
from faker import Faker
from django.core.management.base import BaseCommand

from todo.models import Task
from accounts.models import User

class Command(BaseCommand):
    help = "This command creates fake tasks for testing purposes"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.faker.email(),
            password="Test@123456",
            is_verified=True
        )

        user.full_name = self.faker.first_name() + " " + self.faker.last_name()
        user.save()

        for _ in range(5):
            Task.objects.create(
                title=self.faker.sentence(nb_words=3).rstrip('.'),
                complete=random.choice([True, False]),
                user=user
            )

        print('Tasks have been added successfully')

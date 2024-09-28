# Guarda esto como un archivo dentro de cualquier aplicación Django en la carpeta management/commands


from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Deletes all migration files in all apps'

    def handle(self, *args, **options):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        for subdir, dirs, files in os.walk(project_root):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".py") and 'migrations' in filepath and not file == '__init__.py':
                    os.remove(filepath)
                    self.stdout.write(self.style.SUCCESS(f'Removed {filepath}'))

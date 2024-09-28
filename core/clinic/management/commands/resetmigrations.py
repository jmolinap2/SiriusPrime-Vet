# Guarda esto como un archivo dentro de cualquier aplicación Django en la carpeta management/commands


ffrom django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Deletes all migration files in all apps'

    def handle(self, *args, **options):
        # Obtiene la ruta absoluta del archivo actual (__file__ es el archivo actualmente ejecutado).
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

        for subdir, dirs, files in os.walk(project_root):
            for file in files:
                filepath = os.path.join(subdir, file)
                # Añade condición para evitar borrar el archivo actual del comando
                if filepath.endswith(".py") and 'migrations' in filepath and filepath != current_file and file != '__init__.py':
                    os.remove(filepath)
                    self.stdout.write(self.style.SUCCESS(f'Removed {filepath}'))


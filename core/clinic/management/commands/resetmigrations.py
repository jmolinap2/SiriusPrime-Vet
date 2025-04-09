


from django.core.management.base import BaseCommand
from django.conf import settings  # Importa las configuraciones de Django
import os

class Command(BaseCommand):
    help = 'Elimina todos los archivos de migración en todas las apps'

    def handle(self, *args, **options):
        # Usamos settings.BASE_DIR para obtener la raíz del proyecto
        project_root = settings.BASE_DIR
        virtual_env = os.environ.get('VIRTUAL_ENV')  # Obtén la ruta del entorno virtual si existe
        self.stdout.write(self.style.NOTICE(f"Raíz del proyecto: {project_root}"))
        if virtual_env:
            self.stdout.write(self.style.NOTICE(f"Entorno virtual detectado: {virtual_env}"))

        # Recorrer todos los subdirectorios y archivos
        for subdir, dirs, files in os.walk(project_root):
            # Ignorar el directorio del entorno virtual si está definido
            if virtual_env and subdir.startswith(virtual_env):
                continue

            self.stdout.write(self.style.NOTICE(f"Revisando directorio: {subdir}"))
            for file in files:
                # Crear la ruta completa del archivo
                filepath = os.path.join(subdir, file)
                
                # Verificar si el archivo es una migración y no es __init__.py
                if filepath.endswith(".py") and 'migrations' in filepath and file != '__init__.py':
                    # Confirmar antes de eliminar
                    confirm = input(f"¿Quieres eliminar este archivo de migración? {filepath} (s/n): ").lower()
                    
                    if confirm == 's':
                        os.remove(filepath)
                        self.stdout.write(self.style.SUCCESS(f"Eliminado {filepath}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"No se eliminó {filepath}"))

        # Mensaje final cuando termine el proceso
        self.stdout.write(self.style.SUCCESS("Proceso completado."))



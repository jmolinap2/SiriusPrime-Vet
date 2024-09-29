import os
import subprocess

def run_git_commands():
    # Pide el mensaje del commit al usuario
    commit_message = input("Ingresa el mensaje del commit: ")

    # Confirma si desea continuar
    confirm = input(f"¿Estás seguro de hacer commit con el mensaje '{commit_message}'? (s/n): ").lower()

    if confirm == 's':
        try:
            # Ejecuta los comandos git uno por uno
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push"], check=True)

            print("¡Cambios añadidos, commiteados y enviados exitosamente!")

        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando: {e}")
    else:
        print("Operación cancelada.")

if __name__ == "__main__":
    run_git_commands()

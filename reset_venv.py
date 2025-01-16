import os
import shutil
import subprocess

def reset_venv():
    # Remover o ambiente virtual antigo
    if os.path.exists('.venv'):
        shutil.rmtree('.venv')
        print(".venv removido com sucesso.")

    # Criar um novo ambiente virtual
    subprocess.run(["python", "-m", "venv", ".venv"])
    print(".venv recriado com sucesso.")

    # Ativar e instalar dependências
    activate_script = ".venv/bin/activate" if os.name != "nt" else ".venv\\Scripts\\activate.bat"
    subprocess.run(["pip", "install", "-r", "requirements.txt"], shell=True)
    print("Dependências instaladas com sucesso.")

if __name__ == "__main__":
    reset_venv()

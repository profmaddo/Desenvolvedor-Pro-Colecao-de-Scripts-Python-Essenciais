from setuptools import setup, find_packages
import os

def read_requirements():
    """Lê todos os arquivos requirements.txt das subpastas e consolida as dependências."""
    requirements = set()
    for root, dirs, files in os.walk("."):
        if "requirements.txt" in files:
            with open(os.path.join(root, "requirements.txt")) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        requirements.add(line)
    return list(requirements)

setup(
    name="Colecao de Scripts Python Essenciais",
    version="1.0.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    description="Este projeto é parte integrando do E-book.",
    author="Marco Aurélio Dias de Oliveira",
    author_email="profmaddo@gmail.com",
    url="https://github.com/profmaddo/Desenvolvedor-Pro-Colecao-de-Scripts-Python-Essenciais.git",  # Altere para o repositório real
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

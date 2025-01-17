from rembg import remove
from tqdm import tqdm
import time

imagem_original = "imagens/leao-com-bg.jpg"
imagem_processada = "imagens/leao-sim-bg.png"

'''
Dica: Caso execute o script e ocorra um erro
      por falta da biblioteca onnxruntime

import onnxruntime as ort
ModuleNotFoundError: No module named 'onnxruntime'

Sem sair da IDE, abra o terminal e digite o comando
abaixo para instalar a dependência 'onnxruntime'

pip install onnxruntime
'''


def processamento():
    # Abrindo a imagem de entrada
    print(f'Nome da imagem original: {imagem_original}\n')
    print(f'Criando nova imagem sem background: {imagem_processada}')

    # Adiciona a barra de progresso
    with tqdm(total=100, desc="Removendo Background", unit="%", ncols=80) as pbar:
        # Simula o início do processamento
        time.sleep(0.5)
        pbar.update(10)  # Atualiza para 10%

        # Lendo o arquivo original
        with open(imagem_original, 'rb') as input_file:
            input_data = input_file.read()
            time.sleep(0.5)
            pbar.update(20)  # Atualiza para 30%

        # Removendo o fundo
        output = remove(input_data)
        time.sleep(0.5)
        pbar.update(40)  # Atualiza para 70%

        # Salvando a imagem resultante
        with open(imagem_processada, 'wb') as output_file:
            output_file.write(output)
            time.sleep(0.5)
            pbar.update(30)  # Atualiza para 100%


# Ponto de entrada
if __name__ == '__main__':
    print('Script para Remover Background de Imagens')
    processamento()
    print('Processamento finalizado..')

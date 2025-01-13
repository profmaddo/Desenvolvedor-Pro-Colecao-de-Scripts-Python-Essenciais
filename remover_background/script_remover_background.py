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

    # Simula etapas para demonstrar a barra de progresso
    with open(imagem_original, 'rb') as input_file:
        # Adiciona a barra de progresso
        with tqdm(total=100, desc="Removendo Background", unit="%") as pbar:
            # Removendo o fundo
            time.sleep(0.5)  # Simula o início do processamento
            output = remove(input_file.read())
            pbar.update(50)  # Atualiza para 50% após leitura

            # Salvando a imagem resultante
            with open(imagem_processada, 'wb') as output_file:
                output_file.write(output)
                time.sleep(0.5)  # Simula o tempo restante para salvar
                pbar.update(50)  # Atualiza para 100%

# Ponto de entrada
if __name__ == '__main__':
    print('Script para Remover Background de Imagens')
    processamento()
    print(f'Processamento finalizado..')

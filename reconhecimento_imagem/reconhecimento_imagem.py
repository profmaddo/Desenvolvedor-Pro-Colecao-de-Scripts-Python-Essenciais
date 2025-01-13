
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import DetrImageProcessor, DetrForObjectDetection
import datetime
import os
import sqlite3

'''
Instale as seguintes dependências

pip install pillow
pip install timm

'''

# Caminho para a imagem de entrada
# Substitua pelo caminho da sua imagem
image_path = "imagens/frutas.png"


# Função para criar o banco de dados e a tabela
def criar_banco_de_dados():
    conn = sqlite3.connect("database/imagens.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS objetos_detectados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_imagem TEXT,
                numero_objeto INTEGER,
                nome_objeto TEXT,
                data_hora TEXT
            )
        """)
    conn.commit()
    conn.close()


# Função para salvar os dados no banco
def salvar_dados(nome_imagem, numero_objeto, nome_objeto):
    conn = sqlite3.connect("database/imagens.sqlite")
    cursor = conn.cursor()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
            INSERT INTO 
            objetos_detectados (nome_imagem, numero_objeto, nome_objeto, data_hora)
            VALUES (?, ?, ?, ?)
            """,
        (nome_imagem, numero_objeto, nome_objeto, data_hora))
    conn.commit()
    conn.close()


# Função para listar os dados do banco
def listar_dados():
    conn = sqlite3.connect("database/imagens.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM objetos_detectados ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


# Função principal de processamento
def processamento(image_path):
    # Carregar o modelo e o processador
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")

    # Abrir a imagem
    image = Image.open(image_path).convert("RGB")

    # Pré-processar a imagem
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Processar as detecções
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs,
            target_sizes=target_sizes, threshold=0.9)[0]

    # Desenhar na imagem
    draw = ImageDraw.Draw(image)
    # Ajuste conforme necessário
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20) if os.path.exists(font_path) \
           else None

    for idx, (score, label, box) in enumerate(zip(results["scores"],
                                                  results["labels"],
                                                  results["boxes"])):
        label_name = model.config.id2label[label.item()]
        box = [round(i, 2) for i in box.tolist()]
        draw.rectangle(box, outline="green", width=8)  # Borda verde

        # Calcular o tamanho do texto usando textbbox
        if font:
            # (left, top, right, bottom)
            text_bbox = draw.textbbox((0, 0), label_name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        else:
            text_width, text_height = 100, 20  # Valores padrão para texto sem fonte

        # Desenhar fundo preto para o texto
        text_background = [
            box[0],
            box[1] - text_height - 4,
            box[0] + text_width + 4,
            box[1]
        ]
        draw.rectangle(text_background, fill="black")  # Fundo preto

        # Adicionar texto branco
        text_position = (box[0] + 2, box[1] - text_height - 2)
        # Texto branco
        draw.text(text_position, label_name, fill="white", font=font)

        # Salvar os dados no banco de dados
        salvar_dados(os.path.basename(image_path), idx + 1, label_name)

    # Salvar a nova imagem com data e hora no nome
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{os.path.splitext(image_path)[0]}_processed_{timestamp}.jpg"
    image.save(output_path)
    print(f"Imagem processada salva como: {output_path}")

    # Listar e imprimir os dados do banco de dados
    print("\nDados no banco de dados:")
    dados = listar_dados()
    for row in dados:
        print(row)


if __name__ == "__main__":
    # Criar o banco de dados e a tabela
    criar_banco_de_dados()

    # Executar o processamento
    processamento(image_path)

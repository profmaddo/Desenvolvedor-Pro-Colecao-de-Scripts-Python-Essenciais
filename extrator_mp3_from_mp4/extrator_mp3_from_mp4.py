#!/usr/bin/env python3

import moviepy as mp
from pydub import AudioSegment
from pydub.effects import normalize
import numpy as np
import os
import sys
import time
from datetime import datetime


def processamento(video_path):
    """
    Extrai o áudio de um arquivo de vídeo MP4, aplica normalização e redução de ruídos,
    e salva o áudio em formato MP3 com data e hora no nome.

    Args:
        video_path (str): Caminho do arquivo de vídeo MP4.
    """
    # Validar formato do arquivo
    if not video_path.lower().endswith(".mp4"):
        print("Erro: O arquivo deve estar no formato MP4.")
        return

    # Obter nome do arquivo de saída com data e hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_audio_path = f"{os.path.splitext(video_path)[0]}_audio_{timestamp}.mp3"

    try:
        start_time = time.time()

        # Passo 1: Extrair áudio do vídeo
        print("Extraindo áudio do vídeo...")
        video = mp.VideoFileClip(video_path)
        # Salvar áudio temporariamente como WAV
        temp_audio_path = "temp_audio.wav"
        # WAV para máxima qualidade
        video.audio.write_audiofile(temp_audio_path, codec="pcm_s16le")

        # Passo 2: Carregar o áudio extraído
        print("Carregando áudio para processamento...")
        audio = AudioSegment.from_file(temp_audio_path)

        # Passo 3: Normalizar o áudio
        print("Normalizando o áudio...")
        audio = normalize(audio)

        # Passo 4: Reduzir ruído (simples)
        print("Reduzindo ruído...")

        def reduce_noise(audio_segment, noise_reduction_level=20):
            """
            Reduz o ruído aplicando um filtro simples.

            Args:
                audio_segment (AudioSegment): Áudio a ser processado.
                noise_reduction_level (int): Redução em dB.

            Returns:
                AudioSegment: Áudio com ruído reduzido.
            """
            samples = np.array(audio_segment.get_array_of_samples())
            filtered_samples = np.where(abs(samples) > noise_reduction_level, samples, 0)
            return audio_segment._spawn(filtered_samples.astype(np.int16).tobytes())

        audio = reduce_noise(audio)

        # Passo 5: Salvar o áudio como MP3
        print("Salvando áudio como MP3...")
        audio.export(output_audio_path, format="mp3", bitrate="320k")

        # Limpar o arquivo temporário
        os.remove(temp_audio_path)

        elapsed_time = time.time() - start_time
        print(f"MP3 extraído e salvo em: {output_audio_path}")
        print(f"Processamento concluído em {elapsed_time:.2f} segundos.")

    except Exception as e:
        print(f"Erro ao processar o vídeo: {e}")


if __name__ == "__main__":
    # Validar argumentos do terminal
    if len(sys.argv) != 2:
        print("Uso: extrair_audio <caminho_do_video.mp4>")
        sys.exit(1)

    video_path = sys.argv[1]
    if not os.path.exists(video_path):
        print(f"Erro: Arquivo {video_path} não encontrado.")
        sys.exit(1)

    # Executar o processamento
    processamento(video_path)

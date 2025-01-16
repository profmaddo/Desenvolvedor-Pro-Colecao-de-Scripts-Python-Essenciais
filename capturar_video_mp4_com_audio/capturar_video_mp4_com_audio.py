import os
import cv2
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import platform
import pyaudio
import wave
import subprocess
from time import sleep


## brew install portaudio
## pip install pyaudio
## pip install opencv-python
## pip install ffmpeg-python


is_capturing = False  # Variável global para controlar a captura
capture_thread = None
output_path = None  # Caminho do vídeo em captura

def check_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erro", "Conecte uma webcam USB para continuar")
        return False
    cap.release()
    return True

def get_webcam_info():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "N/A", "N/A", "N/A", False

    webcam_name = platform.node()
    usb_port = "USB 0"
    resolution = f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
    audio_support = True  # Suporte para microfone
    cap.release()

    return webcam_name, usb_port, resolution, audio_support

def record_audio(output_audio_path):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    frames = []
    while is_capturing:
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_audio_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def start_video_processing(label_frame):
    global is_capturing, capture_thread, output_path

    if not check_webcam():
        return

    if is_capturing:
        messagebox.showinfo("Info", "A captura já está em andamento.")
        return

    def process_video():
        global is_capturing, output_path
        if not os.path.exists("capturas"):
            os.makedirs("capturas")

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 20)  # Garante taxa de quadros correta
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_video_path = f"capturas/video_{timestamp}.mp4"
        output_audio_path = f"capturas/audio_{timestamp}.wav"
        final_output_path = f"capturas/final_{timestamp}.mp4"
        output_path = final_output_path

        out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame_width, frame_height))

        is_capturing = True

        # Aguarda um pequeno tempo antes de iniciar o vídeo para sincronizar com o áudio
        audio_thread = threading.Thread(target=record_audio, args=(output_audio_path,))
        audio_thread.start()
        sleep(0.1)

        while is_capturing and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            out.write(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = cv2.resize(frame, (400, 300))
            photo = tk.PhotoImage(master=label_frame, data=cv2.imencode('.ppm', frame_image)[1].tobytes())
            label_frame.config(image=photo)
            label_frame.image = photo

        cap.release()
        out.release()
        is_capturing = False
        audio_thread.join()

        # Combinar vídeo e áudio usando subprocess e ajustar offset
        command = [
            "ffmpeg", "-y",
            "-i", output_video_path,
            "-itsoffset", "0.1",  # Ajuste de sincronização (atraso do áudio)
            "-i", output_audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            final_output_path
        ]
        subprocess.run(command)

        # Remover arquivos intermediários
        os.remove(output_video_path)
        os.remove(output_audio_path)

        messagebox.showinfo("Concluído", f"Vídeo salvo em: {final_output_path}")

    capture_thread = threading.Thread(target=process_video)
    capture_thread.start()

def stop_video_processing():
    global is_capturing

    if not is_capturing:
        messagebox.showinfo("Info", "Nenhuma captura está em andamento.")
        return

    is_capturing = False

def exit_application(root):
    global is_capturing
    if is_capturing:
        stop_video_processing()
    root.destroy()

def create_gui():
    root = tk.Tk()
    root.title("Gravação de Vídeo com Webcam")
    root.geometry("600x400")

    webcam_name, usb_port, resolution, audio_support = get_webcam_info()

    label_frame = tk.Label(root, text="", bg="black", width=50, height=15)
    label_frame.pack(pady=10)

    start_button = tk.Button(root, text="Iniciar Captura", command=lambda: start_video_processing(label_frame), width=20)
    start_button.pack(pady=5)

    stop_button = tk.Button(root, text="Finalizar Captura", command=stop_video_processing, width=20)
    stop_button.pack(pady=5)

    exit_button = tk.Button(root, text="Sair", command=lambda: exit_application(root), width=20)
    exit_button.pack(pady=5)

    info_button = tk.Button(root, text=f"Webcam: {webcam_name} | Porta: {usb_port}", width=50, relief=tk.RAISED)
    info_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

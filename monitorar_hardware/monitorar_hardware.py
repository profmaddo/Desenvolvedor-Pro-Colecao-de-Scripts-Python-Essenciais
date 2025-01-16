import time
import psutil
import platform
from datetime import datetime

def processamento():
    """Obtém a temperatura do processador (se suportado pelo sistema)."""
    try:
        if hasattr(psutil, "sensors_temperatures"):
            sensors = psutil.sensors_temperatures()
            if sensors:
                for name, entries in sensors.items():
                    if entries:
                        return entries[0].current
            return "N/A"  # Não encontrado
        else:
            return "Temperatura não suportada pelo sistema."
    except Exception as e:
        return f"Erro ao obter temperatura: {str(e)}"

def get_ram_disponivel():
    """Obtém a quantidade de memória RAM disponível."""
    mem = psutil.virtual_memory()
    return mem.available / (1024 * 1024)  # Convertendo para MB

def get_cpu_info():
    """Obtém informações sobre o processador."""
    try:
        cpu_info = {
            "fabricante": platform.processor(),
            "velocidade_ghz": psutil.cpu_freq().current / 1000
                                if psutil.cpu_freq() else "N/A",
            "cores_totais": psutil.cpu_count(logical=True),
            "cores_fisicos": psutil.cpu_count(logical=False),
            "percentual_uso": psutil.cpu_percent(interval=1)
        }
        return cpu_info
    except Exception as e:
        return {"Erro": str(e)}

def get_os_info():
    """Obtém informações sobre o sistema operacional."""
    try:
        system_name = platform.system()
        version = platform.version()
        release = platform.release()
        return f"{system_name} {release} (versão {version})"
    except Exception as e:
        return f"Erro ao obter informações do sistema: {str(e)}"

while True:
    # Data e hora
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Dados do hardware e sistema
    cpu_temp = processamento()
    ram_available = get_ram_disponivel()
    cpu_info = get_cpu_info()
    os_info = get_os_info()

    # Exibindo as informações
    print(f"[{current_time}]")
    print(f"Sistema Operacional: {os_info}")
    print(f"Temperatura do Processador: {cpu_temp}°C")
    print(f"Memória RAM Disponível: {ram_available:.2f} MB")
    print(f"Fabricante do Processador: {cpu_info['fabricante']}")
    print(f"Velocidade do Processador: {cpu_info['velocidade_ghz']} GHz")
    print(f"Núcleos Totais: {cpu_info['cores_totais']} (Lógicos)")
    print(f"Núcleos Físicos: {cpu_info['cores_fisicos']}")
    print(f"Percentual de Uso do CPU: {cpu_info['percentual_uso']}%")
    print("-" * 50)

    # Espera 30 segundos antes de repetir
    time.sleep(30)

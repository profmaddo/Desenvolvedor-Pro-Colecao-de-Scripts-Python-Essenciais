import psutil
import platform

def processamento():
    # Processador
    cpu_info = platform.processor()

    # Temperatura atual (se suportado pelo sistema)
    try:
        temperatures = psutil.sensors_temperatures()
        cpu_temp = temperatures["coretemp"][0].current \
            if "coretemp" in temperatures else "Não disponível"

    except (AttributeError, KeyError):
        cpu_temp = "Não disponível"

    # Total de Cores
    total_cores = psutil.cpu_count(logical=False)
    total_threads = psutil.cpu_count(logical=True)

    # Sistema Operacional e Versão do Kernel
    os_info = platform.system()
    os_version = platform.release()

    # Memória RAM Total e Disponível
    memory_info = psutil.virtual_memory()
    total_ram_mb = round(memory_info.total / (1024 * 1024), 2)
    available_ram_mb = round(memory_info.available / (1024 * 1024), 2)

    # Informações sobre os Discos
    disks = psutil.disk_partitions()
    disk_info = []
    for idx, partition in enumerate(disks):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_disk_mb = round(usage.total / (1024 * 1024), 2)
            free_disk_mb = round(usage.free / (1024 * 1024), 2)
            disk_info.append({
                "Disco": idx + 1,
                "Espaço Total (MB)": total_disk_mb,
                "Espaço Disponível (MB)": free_disk_mb,
                "Ponto de Montagem": partition.mountpoint
            })
        except PermissionError:
            # Algumas partições podem não permitir acesso, ignoramos essas.
            disk_info.append({
                "Disco": idx + 1,
                "Espaço Total (MB)": "Acesso negado",
                "Espaço Disponível (MB)": "Acesso negado",
                "Ponto de Montagem": partition.mountpoint
            })

    # Exibir informações
    print("=== Informações do Sistema ===")
    print(f"Processador: {cpu_info}")
    print(f"Temperatura Atual: {cpu_temp} °C")
    print(f"Total de Cores: {total_cores}")
    print(f"Total de Threads: {total_threads}")
    print(f"Sistema Operacional: {os_info}")
    print(f"Versão do Kernel: {os_version}")
    print(f"Memória RAM Total: {total_ram_mb} MB")
    print(f"Memória RAM Disponível: {available_ram_mb} MB")
    print(f"Quantidade de Discos Instalados: {len(disks)}")

    print("\n=== Informações dos Discos ===")
    for info in disk_info:
        print(f"Disco {info['Disco']}:")
        print(f"  - Ponto de Montagem: {info['Ponto de Montagem']}")
        print(f"  - Espaço Total: {info['Espaço Total (MB)']} MB")
        print(f"  - Espaço Disponível: {info['Espaço Disponível (MB)']} MB")
        print()

if __name__ == "__main__":
    processamento()

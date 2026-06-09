

import random

def coletar():

    #Simula a coleta de telemetria do satélite de observação ambiental EnviroSat.
    #Retorna um dicionário com os parâmetros obrigatórios da Trilha 2.

    telemetria = {
        "quantidade_de_focus_do_sensor_térmico": random.randint(0, 20),       # Quantidade de focos de calor detectados
        "status_do_sensor_óptico": random.choice(["OPERACIONAL", "DEGRADADO", "FALHA"]),
        "buffer_de_imagens_retidas": random.randint(0, 80),     # Imagens na fila aguardando downlink
        "precisao_da_geolocalização_(em_metros)": round(random.uniform(0.5, 20), 2),  # Margem de erro em metros
        "percentual_de_bateria_disponível": round(random.uniform(10.0, 100.0), 2) # Percentual de carga (%)
    }
    return telemetria
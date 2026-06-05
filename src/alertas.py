def avaliar(dados):
    """
    Avalia a telemetria recebida do satélite e gera alertas baseados
    nos limites operacionais rigorosos da missão EnviroSat.
    """
    alertas = []

    # Regra 1: Alto índice de focos de incêndio ativos (Risco Ecológico Máximo)
    if dados["quantidade_de_focus_do_sensor_térmico"] >= 5:
        alertas.append({
            "parametro": "quantidade_de_focus_do_sensor_térmico",
            "nivel": "CRÍTICO",
            "mensagem": f"Alerta de Incêndio: {dados['quantidade_de_focus_do_sensor_térmico']} focos térmicos ativos detectados. Risco iminente à biodiversidade e comunidades locais."
        })

    # Regra 2: Degradação ou Falha Total do Sensor Óptico RGB+NIR
    if dados["status_do_sensor_óptico"] in ["DEGRADADO", "FALHA"]:
        alertas.append({
            "parametro": "status_do_sensor_óptico",
            "nivel": "ALERTA" if dados["status_do_sensor_óptico"] == "DEGRADADO" else "CRÍTICO",
            "mensagem": f"Subsistema óptico principal operando em estado de {dados['status_do_sensor_óptico']}. Impossibilidade de validação jurídica de imagens para aplicação de multas pelo IBAMA."
        })

    # Regra 3: Buffer de imagens retidas acumulando perigosamente (Risco de perda de dados temporais)
    if dados["buffer_de_imagens_retidas"] > 40:
        alertas.append({
            "parametro": "buffer_de_imagens_retidas",
            "nivel": "ALERTA",
            "mensagem": f"Gargalo de Downlink: {dados['buffer_de_imagens_retidas']} imagens acumuladas no buffer de telemetria. Atraso crítico no tempo de resposta das brigadas terrestres."
        })

    # Regra 4: Margem de Erro de Geolocalização acima do tolerado para fiscalização
    if dados["precisao_da_geolocalização_(em_metros)"] > 10.0:
        alertas.append({
            "parametro": "precisao_da_geolocalização_(em_metros)",
            "nivel": "ALERTA",
            "mensagem": f"Desvio de órbita detectado: Margem de erro de {dados['precisao_da_geolocalização_(em_metros)']} metros impossibilita o envio de coordenadas confiáveis para equipes de campo."
        })

    # Regra 5: Nível de Energia de Bateria em limite subsistencial
    if dados["percentual_de_bateria_disponível"] < 20.0:
        alertas.append({
            "parametro": "percentual_de_bateria_disponível",
            "nivel": "CRÍTICO",
            "mensagem": f"Falha de alimentação energética: Apenas {dados['percentual_de_bateria_disponível']}% de bateria disponível. Risco de desligamento forçado do payload ambiental."
        })

    return alertas
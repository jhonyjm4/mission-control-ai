import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
import src.telemetria as telemetria
import src.alertas as alertas
load_dotenv()

# Identificação da trilha — ALTEREM conforme a escolha do grupo
TRILHA = "envirosat" # "agrosat" | "envirosat" | "connectsat" | "mobilitysat"

client = Client(
   host="https://ollama.com",
   headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY', '')}
)

def llm(prompt, system=None, max_tokens=2000, temperature=0.3):
   """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
   messages = []
   if system:
      messages.append({"role": "system", "content": system})
   messages.append({"role": "user", "content": prompt})
   try:
      return client.chat(
         model="gpt-oss:120b", messages=messages,
         options={"num_predict": max_tokens, "temperature": temperature},
         stream=False
      )['message']['content'].strip()
   except Exception as e:
      return f"⚠️ Erro ao consultar IA: {e}"

def load_system_prompt():
   """Lê o system prompt do arquivo prompts/system_prompt.md"""
   path = Path("prompts/system_prompt.md")
   if path.exists():
      return path.read_text(encoding="utf-8")
   return "Você é um analista de dados de satélites ambientais."

class MissionEngine:
   """Motor de análise — vocês completam os métodos abaixo."""

   def __init__(self):
      self.trilha = TRILHA
      self.system_prompt = load_system_prompt()

   def is_ready(self):
      return True

   def status_snapshot(self):
      """Prepara e formata o panorama de telemetria imediato para o comando /status."""
      dados = telemetria.coletar()
      lista_alertas = alertas.avaliar(dados)

      snapshot = f"=== MONITORAMENTO DE PAYLOAD: {self.trilha.upper()} ===\n"
      for parametro, valor in dados.items():
         snapshot += f"• {parametro.replace('_', ' ').title()}: {valor}\n"

      snapshot += f"\nAlertas Automáticos Detectados ({len(lista_alertas)}):\n"
      if not lista_alertas:
         snapshot += " ✓ Sistemas operando em conformidade com as metas ecológicas."
      else:
         for al in lista_alertas:
            snapshot += f" [⚠️ {al['nivel']}] {al['mensagem']}\n"

      return snapshot

   def analyze(self, pergunta_usuario):
      """Combina os dados brutos de telemetria e regras de software no prompt da IA."""
      dados = telemetria.coletar()
      lista_alertas = alertas.avaliar(dados)

      prompt_contextualizado = f"""
      [DADOS DE TELEMETRIA EM TEMPO REAL]
      Focos Térmicos Ativos: {dados['quantidade_de_focus_do_sensor_térmico']}
      Status do Sensor Óptico RGB+NIR: {dados['status_do_sensor_óptico']}
      Imagens Acumuladas no Buffer: {dados['buffer_de_imagens_retidas']}
      Margem de Erro de Geolocalização: {dados['precisao_da_geolocalização_(em_metros)']} metros
      Nível de Carga da Bateria: {dados['percentual_de_bateria_disponível']}%

      [ALERTAS DO SCRIPT PYTHON]
      {lista_alertas if lista_alertas else "Nenhuma inconformidade de hardware identificada."}

      [REQUISIÇÃO DO OPERADOR]
      "{pergunta_usuario}"

      Com base nos dados estruturados acima e em suas diretrizes operacionais, elabore um diagnóstico conectando a telemetria ao impacto real em solo na Terra.
      """
      return llm(prompt_contextualizado, system=self.system_prompt)

   def gerar_relatorio_status(self):
      """
      Coleta as métricas em tempo real e força o gpt-oss:120b a redigir
      um relatório cognitivo focado nos erros encontrados e impactos terrestres.
      """
      dados = telemetria.coletar()
      lista_alertas = alertas.avaliar(dados)

      prompt_auditoria = f"""
           SISTEMA DE AUDITORIA AUTOMÁTICA — ANÁLISE DE STATUS [{self.trilha.upper()}]

           [DADOS DE TELEMETRIA EM TEMPO REAL]
           Focos Térmicos Ativos: {dados['quantidade_de_focus_do_sensor_térmico']}
           Status do Sensor Óptico RGB+NIR: {dados['status_do_sensor_óptico']}
           Imagens Acumuladas no Buffer: {dados['buffer_de_imagens_retidas']}
           Margem de Erro de Geolocalização: {dados['precisao_da_geolocalização_(em_metros)']} metros
           Nível de Carga da Bateria: {dados['percentual_de_bateria_disponível']}%

          Em caso de perguntas expecífcas responda primeiro a pergunta com base nos dados e depois gere o relatório
           """
      return llm(prompt_auditoria, system=self.system_prompt)
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))

def show_banner():
   """Exibe banner ASCII colorido no início."""
   banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
   console.print(Text(banner, style="bold #C9126E"))
   console.print(Panel.fit(
"Sistema de monitoramento e análise por IA generativa.\n"
          "Use /help para ver os comandos · /exit para sair.\n"
          "Modelo: gpt-oss:120b via Ollama Cloud",
          title="◆ MISSION CONTROL", border_style="#C9126E"
))

def show_response(text):
   """Renderiza resposta da IA em painel com timestamp."""
   now = datetime.now().strftime("%H:%M")
   console.print(Panel(text, title="◆ Mission Control",
                       subtitle=now, border_style="#C9126E"))
def run_cli(engine):
   """Loop principal da CLI."""
   show_banner()
   if not engine.is_ready():
      console.print(" ⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="yellow")

   while True:
      try:
         user_input = session.prompt("❯ ").strip()
      except (KeyboardInterrupt, EOFError):
         break
      if not user_input:
         continue
      if user_input == "/exit":
         break
      if user_input == "/help":
         console.print("Comandos: /help /status /about /clear /exit")
         continue
      if user_input == "/status":
         with console.status("[bold #06B6D4]Gerando Relatório de Diagnóstico com IA...[/]"):
            try:
               # Em vez de apenas ler o snapshot, pedimos para a IA analisar o snapshot atual que ela gerou.
               relatorio_ia = engine.gerar_relatorio_status()
               show_response(relatorio_ia)
            except Exception as e:
               console.print(f"\n[red]⚠ Erro ao gerar relatório pela IA: {e}[/red]\n")
         continue
      if user_input == "/about":
         print(f"Sistema operacional: Mission Control AI")
         print(f"\nTrilha Ativa: {engine.trilha.upper()}")
         print(f"\nA missão do Mission Control AI, operada em conjunto com o satélite de observação terrestre EnviSat, tem como foco central a automação inteligente do monitoramento geoespacial e ambiental em tempo real através de Inteligência")
         print(f"Artificial Generativa. Ao integrar um motor analítico avançado diretamente na interface do operador, a missão resolve o crítico problema do atraso na detecção manual de desmatamentos ilegais e queimadas na região Amazônica")
         print(f"e no Cerrado. Através do processamento imediato de telemetrias complexas (como capacidade de buffer de imagem, anomalias em sensores ópticos e variações térmicas), o sistema traduz dados brutos em diagnósticos acionáveis e")
         print(f"alertas de segurança instantâneos, permitindo que órgãos de fiscalização e o setor privado mitiguem desastres ecológicos e controlem focos de incêndio antes que tomem proporções catastróficas.")
         continue
      if user_input == "/clear":
         console.clear(); show_banner(); continue
      else:
         with console.status("[bold #06B6D4]Consultando IA...[/]"):
            try:
               # Envia a pergunta do operador diretamente ao motor de análise
               resposta_llm = engine.analyze(user_input)

               # Exibe a resposta estruturada dentro do painel estilizado com timestamp
               show_response(resposta_llm)
            except Exception as e:
               console.print(f"\n[red]⚠ Erro ao processar requisição na IA: {e}[/red]\n")



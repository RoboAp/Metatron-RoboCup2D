#!/usr/bin/env python3
import sys

class MetatronTelemetry:
    def __init__(self, team_name="Metatron"):
        self.team_name = team_name
        self.total_cycles = 0
        self.side = None  # Vai ser "l" (esquerda) ou "r" (direita)
        
        # Métricas de Eventos (Playmodes)
        self.gols = 0
        self.escanteios = 0
        self.faltas = 0

    def processar_log(self, arquivo_rcg):
        try:
            with open(arquivo_rcg, 'r') as f:
                for linha in f:
                    
                    # 1. MAPEAMENTO DE LADO (Descobrir quem é 'l' e quem é 'r')
                    if "(team " in linha and self.side is None:
                        partes = linha.replace("(", "").replace(")", "").split()
                        if len(partes) >= 4:
                            if self.team_name in partes[2]:
                                self.side = "l"
                            elif self.team_name in partes[3]:
                                self.side = "r"
                        
                        if self.side:
                            print(f"🔍 Time '{self.team_name}' identificado no lado: '{self.side}'")
                        else:
                            print(f"⚠️ Aviso: Time '{self.team_name}' não encontrado nesta partida.")

                    # 2. CONTAGEM DE CICLOS (Tempo de jogo)
                    if "(show " in linha:
                        self.total_cycles += 1

                    # 3. EXTRAÇÃO DE EVENTOS TÁTICOS (Playmodes)
                    if "(playmode " in linha and self.side:
                        # Conta gols do lado correto (ex: goal_l_1, goal_r_2)
                        if f"goal_{self.side}_" in linha:
                            self.gols += 1
                        # Conta escanteios a favor
                        elif f"corner_kick_{self.side}" in linha:
                            self.escanteios += 1
                        # Conta faltas sofridas a favor
                        elif f"free_kick_{self.side}" in linha:
                            self.faltas += 1

        except FileNotFoundError:
            print(f"❌ Erro: Arquivo {arquivo_rcg} não encontrado.")
            sys.exit(1)

    def exibir_relatorio(self):
        print("\n" + "="*40)
        print(f"📊 RELATÓRIO TÁTICO — PROJETO METATRON")
        print("="*40)
        print(f"👁️ Espionando: {self.team_name} (Lado: {self.side})")
        print(f"⏱️ Total de Ciclos da Partida: {self.total_cycles}")
        print("-" * 40)
        print(f"🎯 Métrica de Eventos Ofensivos:")
        print(f"  • Gols Marcados: {self.gols}")
        print(f"  • Escanteios a favor: {self.escanteios}")
        print(f"  • Faltas/Tiros Livres a favor: {self.faltas}")
        print("="*40 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 Uso: python3 analisar_telemetria.py <caminho_do_log.rcg> [nome_do_time]")
    else:
        time_alvo = sys.argv[2] if len(sys.argv) > 2 else "Metatron"
        analisador = MetatronTelemetry(team_name=time_alvo)
        analisador.processar_log(sys.argv[1])
        analisador.exibir_relatorio()
#!/usr/bin/env python3
import sys
import re
import math

class MetatronTelemetry:
    def __init__(self, team_name="Metatron"):
        self.team_name = team_name
        self.side = None
        self.total_cycles = 0
        
        # Métricas de Eventos (Playmodes)
        self.gols = 0
        self.escanteios = 0
        self.faltas = 0
        
        # Métricas de Jogo Dinâmico (Tracking de Coordenadas)
        self.posse_ciclos_l = 0
        self.posse_ciclos_r = 0
        
        self.passes_certos = 0
        self.passes_errados = 0
        
        # Estado interno para rastrear a bola
        self.ultimo_toque_time = None
        self.ultimo_toque_jogador = None
        self.distancia_dominio = 1.5 # Raio (em metros) para considerar que o jogador tem a posse

    def calcular_distancia(self, x1, y1, x2, y2):
        return math.hypot(x1 - x2, y1 - y2)

    def processar_log(self, arquivo_rcg):
        try:
            with open(arquivo_rcg, 'r') as f:
                for linha in f:
                    
                    # 1. MAPEAMENTO DE LADO E LEITURA DO PLACAR
                    if "(team " in linha:
                        partes = linha.replace("(", "").replace(")", "").split()
                        # Estrutura: team tempo time_l time_r gol_l gol_r
                        if len(partes) >= 6:
                            if self.side is None:
                                if self.team_name in partes[2]:
                                    self.side = "l"
                                    print(f"🔍 Time '{self.team_name}' identificado no lado: '{self.side}'")
                                elif self.team_name in partes[3]:
                                    self.side = "r"
                                    print(f"🔍 Time '{self.team_name}' identificado no lado: '{self.side}'")
                            
                            # Atualiza o placar do time a cada ocorrência da tag
                            if self.side == "l":
                                self.gols = int(partes[4])
                            elif self.side == "r":
                                self.gols = int(partes[5])

                    # 2. EXTRAÇÃO DE EVENTOS TÁTICOS (Faltas e Escanteios)
                    if "(playmode " in linha and self.side:
                        if f"corner_kick_{self.side}" in linha:
                            self.escanteios += 1
                        elif f"free_kick_{self.side}" in linha:
                            self.faltas += 1

                    # 3. TELEMETRIA DE COORDENADAS (Posse e Passes)
                    if "(show " in linha:
                        self.total_cycles += 1
                        
                        # Extrai coordenadas da bola: aceitando (b x y) ou ((b) x y)
                        bola_match = re.search(r'\(\(?b\)? ([-+]?\d*\.\d+|[-+]?\d+) ([-+]?\d*\.\d+|[-+]?\d+)', linha)
                        if not bola_match:
                            continue
                            
                        bx, by = float(bola_match.group(1)), float(bola_match.group(2))
                        
                        # Extrai jogadores com o padrão rcg: ((l 1) tipo estado x y)
                        jogadores = re.findall(r'\(\(([lr]) (\d+)\) [^ ]+ [^ ]+ ([-+]?\d*\.\d+|[-+]?\d+) ([-+]?\d*\.\d+|[-+]?\d+)', linha)                       
                        jogador_mais_proximo = None
                        menor_distancia = float('inf')
                        
                        for time, num, jx_str, jy_str in jogadores:
                            jx, jy = float(jx_str), float(jy_str)
                            dist = self.calcular_distancia(bx, by, jx, jy)
                            
                            if dist < menor_distancia:
                                menor_distancia = dist
                                jogador_mais_proximo = (time, num)
                        
                        # Se a bola está muito próxima de alguém, esse alguém tem a posse
                        if jogador_mais_proximo and menor_distancia <= self.distancia_dominio:
                            time_atual, jogador_atual = jogador_mais_proximo
                            
                            # Contabiliza ciclo de posse geral
                            if time_atual == 'l':
                                self.posse_ciclos_l += 1
                            else:
                                self.posse_ciclos_r += 1
                                
                            # Lógica de análise de passes (Focada no nosso time)
                            if self.ultimo_toque_time is not None:
                                # O time mudou de posse? Interceptação / Passe Errado
                                if self.ultimo_toque_time == self.side and time_atual != self.side:
                                    self.passes_errados += 1
                                    
                                # O mesmo time manteve a bola, mas foi outro jogador? Passe Certo
                                elif self.ultimo_toque_time == self.side and time_atual == self.side and self.ultimo_toque_jogador != jogador_atual:
                                    self.passes_certos += 1
                                    
                            self.ultimo_toque_time = time_atual
                            self.ultimo_toque_jogador = jogador_atual

        except FileNotFoundError:
            print(f"❌ Erro: Arquivo {arquivo_rcg} não encontrado.")
            sys.exit(1)

    def exibir_relatorio(self):
        total_posse_ciclos = self.posse_ciclos_l + self.posse_ciclos_r
        
        # Prevenção de divisão por zero
        if total_posse_ciclos == 0: total_posse_ciclos = 1 
        
        pct_posse_l = (self.posse_ciclos_l / total_posse_ciclos) * 100
        pct_posse_r = (self.posse_ciclos_r / total_posse_ciclos) * 100
        
        minha_posse = pct_posse_l if self.side == 'l' else pct_posse_r

        print("\n" + "="*50)
        print(f"📊 RELATÓRIO TÁTICO AVANÇADO — PROJETO METATRON")
        print("="*50)
        print(f"👁️ Time Monitorado: {self.team_name} (Lado: {self.side.upper() if self.side else 'Desconhecido'})")
        print(f"⏱️ Duração da Partida: {self.total_cycles} ciclos")
        print("-" * 50)
        print(f"⚽ Controle de Jogo:")
        print(f"  • Posse de Bola: {minha_posse:.1f}%")
        print(f"  • Passes Certos: {self.passes_certos}")
        print(f"  • Passes Errados (Bolas perdidas): {self.passes_errados}")
        print("-" * 50)
        print(f"🎯 Eventos Ofensivos:")
        print(f"  • Gols Marcados: {self.gols}")
        print(f"  • Escanteios a favor: {self.escanteios}")
        print(f"  • Faltas/Tiros Livres a favor: {self.faltas}")
        print("="*50 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 Uso: python3 analisar_telemetria.py <caminho_do_log.rcg> [nome_do_time]")
    else:
        # Se nenhum time for passado, o padrão é o time do projeto
        time_alvo = sys.argv[2] if len(sys.argv) > 2 else "Metatron"
        analisador = MetatronTelemetry(team_name=time_alvo)
        analisador.processar_log(sys.argv[1])
        analisador.exibir_relatorio()
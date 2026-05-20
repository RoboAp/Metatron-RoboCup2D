# ⚽🤖 Projeto Metatron - RobôAP

Bem-vindo ao repositório oficial do **Metatron**, o projeto de desenvolvimento da categoria **RoboCup 2D Simulation** da equipe **RobôAP** (UTFPR Campus Apucarana). Este projeto foca na aplicação de inteligência artificial, geometria computacional e estratégia coletiva utilizando a base do *Pyrus2D*.

---

## 👥 Estrutura do Squad & Divisão de Papéis

Como operamos em um time enxuto de 3 pessoas, o projeto é dividido em braços técnicos específicos para garantir que o desenvolvimento aconteça simultaneamente:

* **Michel (Líder / Infraestrutura & Integração):**
    * Responsável pela padronização do ambiente de desenvolvimento (Zorin OS / Python Venv).
    * Automação de scripts de testes e gerenciamento de fluxo no GitHub.
    * Responsável pela consolidação do TDP (Technical Description Paper) e documentação final.
* **Plinio (Lógica de Decisão & Ataque):**
    * Responsável pelo "Cérebro" do robô (mapeamento do `sample_player.py`, `main.py` e `player.py`).
    * Desenvolvimento de estados de decisão de ataque: quando correr atrás da bola e quando chutar ao gol.
    * Refinamento das redes neurais para otimização tática.
* **Gabriel (Física Computacional, Geometria & Defesa):**
    * Responsável pelo domínio da biblioteca `pyrusgeom` e sistema de coordenadas do campo.
    * Cálculos matemáticos de interceptação de bola (ponto de encontro futuro) e física do chute.
    * Desenvolvimento do comportamento do Goleiro e triangulação espacial de posicionamento.

---

## 🗓️ Cronograma de Desenvolvimento Sincronizado

O desenvolvimento é focado no **Método PPP (Progresso, Planos e Problemas)** com relatórios semanais. O esforço de cada membro varia conforme a fase atual:

| Fase | Objetivo Principal | Foco do Trabalho (Paralelo) |
| :--- | :--- | :--- |
| **Fase 1** | **Setup & Teoria** | **Michel:** Configuração do Git e ambiente.<br>**Plinio:** Estudo do fluxo de visão (`see`).<br>**Gabriel:** Estudo das coordenadas e vetores. |
| **Fase 2** | **Agente Individual** | **Michel:** Automação de treinos.<br>**Plinio:** Lógica de perseguição e chute.<br>**Gabriel:** Cálculo de interceptação e goleiro base. |
| **Fase 3** | **Inteligência Coletiva** | **Michel:** Análise de arquivos `.rcg` de rivais.<br>**Plinio & Gabriel:** Implementação da Triangulação de Delaunay e passes rápidos para vencer o *Simple Team*. |
| **Fase 4** | **Otimização & Amistosos** | **Todo o Squad:** Ajuste fino de redes neurais, correção de bugs críticos e participação em amistosos remotos com outras universidades. |
| **Fase 5** | **CBR & Legado** | **Michel:** Escrita e revisão do TDP oficial.<br>**Plinio & Gabriel:** Validação final do código e preparação do ambiente para a competição nacional. |

---

## 🏃 Sprint 1: Fundação (Em Andamento)
**Objetivo da Sprint:** Sair da inércia, garantir que o simulador roda liso nas máquinas do time e entender como o robô ouve e enxerga o servidor.

* [ ] **Michel:** Criar o script automatizado `iniciar_jogo.sh` para subir os 22 players e monitor sem quebrar dependências.
* [ ] **Plinio:** Criar um fluxograma inicial de tomada de decisão com base nas mensagens de percepção que o robô recebe.
* [ ] **Gabriel:** Mapear e documentar as funções principais da classe `Vector2D` da biblioteca `pyrusgeom` para cálculo de distância robô-bola.

---

## 🛠️ Requisitos Rápidos de Inicialização (Ambiente)

Certifique-se de que está a usar o **Zorin OS** atualizado e execute no terminal dentro da pasta do projeto:

```bash
# 1. Ativar o Ambiente Virtual
source venv/bin/activate

# 2. Iniciar o Servidor Oficial da Liga
rcssserver

# 3. Iniciar o Monitor Visual
rcssmonitor

# 4. Conectar os 11 Jogadores do Metatron
python3 main.py --team Metatron --players 11

#!/bin/bash

# Define a pasta alvo e o time.
DIRETORIO=${1:-"logs"}
TIME_ALVO=${2:-"Metatron"}

echo "🚀 Iniciando Máquina de Análise em Lote — Projeto Metatron"
echo "📂 Buscando replays (.rcg) na pasta: $DIRETORIO"
echo "👁️ Espionando o time: $TIME_ALVO"
echo "======================================================"

if [ ! -d "$DIRETORIO" ]; then
    echo "❌ Erro: A pasta '$DIRETORIO' não existe."
    exit 1
fi

contador=0

for arquivo in "$DIRETORIO"/*.rcg; do
    if [ -e "$arquivo" ]; then
        echo "▶️ Extraindo métricas da partida: $(basename "$arquivo")"
        
        # Agora o bash passa o TIME_ALVO para o Python!
        python3 analisar_telemetria.py "$arquivo" "$TIME_ALVO"
        
        contador=$((contador + 1))
        echo "------------------------------------------------------"
    fi
done

if [ $contador -eq 0 ]; then
    echo "⚠️ Nenhum arquivo .rcg encontrado em '$DIRETORIO'."
else
    echo "✅ Análise concluída! $contador partidas processadas."
fi
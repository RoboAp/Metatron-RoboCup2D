#!/bin/bash

# --- CONFIGURAÇÃO DE AMBIENTE - PROJETO METATRON ---
echo "🚀 Iniciando a configuração e padronização do ambiente..."

# 1. Definir o caminho dinâmico do projeto (onde o script está localizado)
DIR_PROJETO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR_PATH"

echo "📂 Diretório do projeto definido em: $DIR_PATH"

# 2. Dar permissão de execução para os scripts utilitários
echo "🔧 Aplicando permissões de execução nos scripts..."
if [ -f "kill_robos.sh" ]; then
    chmod +x kill_robos.sh
    echo "  [✓] kill_robos.sh blindado."
fi

# Criando ou atualizando o script de análise de telemetria diretamente
cat << 'EOF' > analisar_partida.sh
#!/bin/bash
# Script automatizado para rodar a análise de logs da Sprint 2
source venv/bin/activate
echo "📊 Iniciando extração de métricas dos arquivos .rcg..."
# Aqui rodará o interpretador que você criar para ler os logs
python3 -c "print('Análise de logs ativada. Taxa de acerto de chutes sendo processada...')"
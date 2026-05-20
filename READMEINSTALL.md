# 🛠️ Manual de Instalação e Configuração do Ambiente

Este guia contém o passo a passo detalhado para compilar o servidor oficial da RoboCup 2D, o monitor visual e configurar a base em Python (*Pyrus2D*) no **Zorin OS** (ou distribuições baseadas em Ubuntu).

---

## 1. Preparando o Terreno (Dependências do Sistema)

Antes de baixar os códigos do simulador, precisamos instalar todas as ferramentas de compilação, bibliotecas gráficas do Qt e a biblioteca Boost. Abra o seu terminal (`Ctrl + Alt + T`) e execute o comando abaixo:

```bash
sudo apt update
sudo apt install build-essential cmake automake autoconf libtool flex bison \
libboost-all-dev qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools \
libfontconfig1-dev libaudio-dev libxt-dev libglib2.0-dev libxi-dev libxrender-dev -y
```
---

## 2. Instalando o Servidor (rcssserver)

O servidor funciona como o "juiz" e o "mundo físico" da partida. Ele roda as regras do jogo e se comunica com os nossos robôs via pacotes UDP.

1. Baixe o pacote de código-fonte mais recente no GitHub oficial do rcsoccersim:
(https://github.com/rcsoccersim/rcssserver)
2. Extraia o arquivo baixado, entre na pasta via terminal e compile seguindo os comandos:

```bash
tar -xzvf rcssserver-*.tar.gz
cd rcssserver-*
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig
```

--- 

## 3. Instalando o Monitor (rcssmonitor)

O monitor é a interface gráfica que permite assistir ao jogo dos robôs em tempo real na tela.(

1.Baixe a versão correspondente no GitHub oficial do rcsoccersim monitor:
(https://github.com/rcsoccersim/rcssmonitor)
2.Extraia o arquivo e repita o processo de compilação padrão:

```bash
tar -xzvf rcssmonitor-*.tar.gz
cd rcssmonitor-*
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig
```


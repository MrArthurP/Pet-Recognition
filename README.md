# 🐾 Alimentador Inteligente para Múltiplos Pets

> Protótipo de alimentador automático IoT para múltiplos animais de estimação, com controle via Wi-Fi, aplicação web e integração com ESP8266.

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
  - [Firmware (Arduino/ESP8266)](#firmware-arduinoesp8266)
  - [Aplicação Web (Django)](#aplicação-web-django)
  - [Inteligência Artificial](#inteligência-artificial)
- [Funcionalidades](#funcionalidades)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## Sobre o Projeto

O aumento no número de animais domésticos por residência e a crescente preocupação com sua saúde criam uma demanda real por soluções acessíveis de manejo alimentar. O controle inadequado da qualidade e quantidade da ração pode causar obesidade, desnutrição e outras complicações graves — problemas que soluções comerciais existentes endereçam, mas a custos elevados e inacessíveis para a maioria dos tutores.

Este projeto desenvolve um **protótipo de Alimentador Inteligente para Múltiplos Pets** que automatiza o processo de alimentação, minimizando o esforço manual dos tutores e promovendo a saúde dos animais. O sistema é composto por:

- Um **mecanismo físico** com espiral giratória acionada por motor de alto torque para distribuição de ração;
- Um **microcontrolador ESP8266** programado via Arduino IDE para controle local e conectividade;
- Uma **aplicação web Django** para gerenciamento de usuários, pets e agendamentos de alimentação;
- Comunicação via **Wi-Fi + protocolo MQTT** entre o dispositivo e a aplicação;
- Um módulo de **Inteligência Artificial** para reconhecimento de múltiplos pets.

---

## Arquitetura do Sistema

```
┌─────────────────┐         MQTT / Wi-Fi        ┌──────────────────────┐
│  Aplicação Web  │◄────────────────────────────►│  ESP8266 (NodeMCU)   │
│    (Django)     │                              │  Firmware Arduino    │
└────────┬────────┘                              └──────────┬───────────┘
         │                                                  │
         │  HTTP / REST                              Motor + Espiral
         │                                         (Distribuição de Ração)
┌────────▼────────┐
│  Dashboard Web  │
│  Controle de    │
│  Pets e Usuários│
└─────────────────┘
         │
┌────────▼────────┐
│  Módulo de IA   │
│  Reconhecimento │
│  de Múltiplos   │
│  Pets           │
└─────────────────┘
```

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
| --- | --- |
| Sistema Operacional | Wsl2 (Subsistema Windows) |
| Firmware | C++ (Arduino IDE), ESP8266, MQTT |
| Backend | Python 3, Django |
| Banco de Dados | SQLite3 |
| Frontend | HTML/CSS/JS (templates Django) |
| Inteligência Artificial | Python (modelo de reconhecimento de imagem), WSL2 (com suporte a GPU local via CUDA) |
| Comunicação IoT | Wi-Fi, protocolo MQTT |
| Hardware | ESP8266 NodeMCU, Esp32Cam, Arduino Uno, motor de alto torque, espiral distribuidora |

---

## Estrutura do Repositório

```
📦 raiz do repositório
├── 📁 arduino/
│   └── 📁 CelulaDeCarga/
│       └── CelulaDeCarga.ino        # Firmware do ESP8266 (controle do alimentador)
│
├── 📁 lateX/                        # Documentação acadêmica do projeto (LaTeX)
│
├── 📁 python/
│   ├── 📁 Django/                   # Aplicação web principal
│   │   ├── 📁 Dashboard/            # App de painel de controle
│   │   ├── 📁 EspNodeMCU/           # App de integração com o hardware
│   │   ├── 📁 media/                # Arquivos de mídia enviados pelos usuários
│   │   ├── 📁 meu_projeto/          # Configurações centrais do projeto Django
│   │   ├── db.sqlite3               # Banco de dados local
│   │   ├── manage.py                # CLI do Django
│   │   ├── models.py                # Modelos de dados globais
│   │   └── requirements.txt         # Dependências Python
│   │
│   └── 📁 Inteligencia_Artificial/  # Módulo de reconhecimento de pets
│       ├── 📁 anchor/               # Configurações de âncoras (detecção de objetos)
│       ├── 📁 application_data/     # Dados da aplicação de IA
│       ├── 📁 negative/             # Imagens negativas para treinamento
│       ├── 📁 positive/             # Imagens positivas para treinamento
│       ├── 📁 training_checkpoints/ # Checkpoints do treinamento do modelo
│       └── Reconhecimento_Multiplos...  # Script principal de reconhecimento
│
└── README.md
```

---

## Pré-requisitos

### Firmware (ESP8266)
- [Arduino IDE](https://www.arduino.cc/en/software) (versão 1.8+)
- Suporte à placa ESP8266 instalado no Arduino IDE
- Bibliotecas: `PubSubClient` (MQTT), `ESP8266WiFi`
- Subsistema WSL2 configurado.

### Aplicação Web
- Python 3.11.15
- pip 26.2

### Inteligência Artificial
- Python  3.11.15
- Dependências listadas em `requirements.txt`

---

## Configurações

### WSL2 

Para que o código seja executado corretamente é necessário realizar a instalação do subsistema Ubuntu ``WSL2`` devido à falta de compatibilidade da biblioteca `TensorFlow` como `Windows` no treinamento da **Inteligência Artificial**. A seguir está o passo a passo para realizar a instalação do subsistema e utilização via VsCode:

1. Instale o subsistema Linux via comando **PoweShell** `wsl --install`. O subsistema da distro `Ubuntu` será instalada no computador

> Verifique nas configurações do seu computador `Painel de Controle → Programas e Recursos → Ativar ou Desativar Programas e Recursos do Windows` a opção `Subsistema Linux para Windows` esteja ativada

2. Após feita a instalação, mova este projeto para uma pasta dentro do usuário do **Linux**: `Ubuntu → home → usuário → pasta do projeto`. Abra a pasta via **VsCode**, que deverá identificar o subsistema automaticamente. Uma outra forma seria abrir o **cmd** do **Ubuntu** e digitar `code .` que o vs code será aberto via **Ubuntu**, e após isso, você selecionará a pasta do projeto.

3. Para que a placa de vídeo (GPU) do seu computador seja identificada pelo sistema, é necessário informar ao sistema onde estão localizadas as bibliotecas **CUDA** no sistema via comando `export` e `source ~/.bashrc`:

```
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

4. Após feito isso, execute a célula de importação de bibliotecas de Inteligência Artificial e verifique se a GPU for encontrada.

## Funcionalidades

- [x] Controle do alimentador via aplicação web
- [x] Comunicação MQTT entre ESP8266 e servidor
- [x] Cadastro de usuários e perfis de pets
- [x] Dashboard de monitoramento
- [x] Reconhecimento de múltiplos pets por câmera
- [x] Distribuição automatizada de ração por espiral giratória
- [ ] Agendamento de alimentações recorrentes *(em desenvolvimento)*
- [ ] Notificações em tempo real para o tutor *(em desenvolvimento)*
- [ ] App mobile *(planejado)*

---

## Pendências

- [x] Adicionar arquivo .cpp de configuração da ESP32CAM
- [x] Usar extensão `PlatformIO` para debug do código **arduino** e **esp** diretamente pelo projeto
- [ ] Ferificar se os códigos das placas rodam via **Platformio IDE**
- [ ] Aumentar o Dataset de imagens **positivas** via _webscrapping_ de outros animais e estrurar o conjunto para que funcione com essas novas imagens
- [ ] Melhorar a avaliação do modelo.

---

<!-- ## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
3. Commit suas mudanças: `git commit -m 'feat: adiciona minha feature'`
4. Faça o push para sua branch: `git push origin feature/minha-feature`
5. Abra um Pull Request. -->

---

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

<p align="center">Desenvolvido com ❤️ para o bem-estar dos pets 🐶🐱</p>
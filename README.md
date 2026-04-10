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
|---|---|
| Firmware | C++ (Arduino IDE), ESP8266, MQTT |
| Backend | Python 3, Django |
| Banco de Dados | SQLite3 |
| Frontend | HTML/CSS/JS (templates Django) |
| Inteligência Artificial | Python (modelo de reconhecimento de imagem) |
| Comunicação IoT | Wi-Fi, protocolo MQTT |
| Hardware | ESP8266 NodeMCU, motor de alto torque, espiral distribuidora |

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

### Aplicação Web
- Python 3.8+
- pip

### Inteligência Artificial
- Python 3.8+
- Dependências listadas em `requirements.txt`

---

## Como Executar

### Firmware (Arduino/ESP8266)

1. Abra o arquivo `arduino/CelulaDeCarga/CelulaDeCarga.ino` na Arduino IDE.
2. Configure as variáveis de rede no código:
   ```cpp
   const char* ssid     = "SEU_WIFI";
   const char* password = "SUA_SENHA";
   const char* mqtt_server = "IP_DO_BROKER";
   ```
3. Selecione a placa **NodeMCU 1.0 (ESP-12E Module)** e a porta serial correta.
4. Faça o upload do firmware para o dispositivo.

### Aplicação Web (Django)

1. Acesse o diretório do projeto:
   ```bash
   cd python/Django
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

6. Acesse a aplicação em `http://localhost:8000`.

### Inteligência Artificial

1. Acesse o diretório:
   ```bash
   cd python/Inteligencia_Artificial
   ```

2. Certifique-se de que as dependências estão instaladas (consulte `requirements.txt` na pasta Django ou instale individualmente os pacotes necessários).

3. Execute o script de reconhecimento:
   ```bash
   python Reconhecimento_Multiplos....py
   ```

> **Nota:** Para treinar o modelo com seus próprios dados, adicione imagens positivas em `positive/` e negativas em `negative/` antes de executar o treinamento.

---

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

- [ ] Adicionar arquivo Arduino de configuração da ESP32CAM 

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
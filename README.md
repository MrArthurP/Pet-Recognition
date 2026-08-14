# 🐾 Alimentador Inteligente para Múltiplos Pets

> Protótipo de alimentador automático IoT para múltiplos animais de estimação utilizando Visão Computacional, com controle via Wi-Fi, aplicação web e integração com ESP8266/ESP32CAM/Arduino.

## Tecnologias Utilizadas

| Camada | Tecnologia |
| --- | --- |
| Sistema Operacional | Wsl2 (Subsistema Windows) |
| Firmware | C++ (Arduino IDE), ESP8266, MQTT |
| Backend | Python3, Django, JupyterNotebook|
| Banco de Dados | SQLite3 |
| Frontend | HTML/CSS/JS (templates Django) |
| Inteligência Artificial | Python (modelo de reconhecimento de imagem), WSL2 (com suporte a GPU local via CUDA) |
| Comunicação IoT | Wi-Fi, protocolo MQTT |
| Hardware | ESP8266 NodeMCU, Esp32Cam, Arduino Uno|

---

## Estrutura do Repositório (Estruturação em Andamento)

```
📦 raiz do repositório
├── 📁 embedded/
│   ├── 📁 Arduino-Uno/
│   ├── 📁 Esp-32CAM/
│   └── 📁 Esp-8266/
│
├── 📁 docs/
│   ├── 📁 Latex/
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
│           ├── 📁 dog1/
│           ├── 📁 dog2/
|           ...
│       ├── 📁 application_data/     # Dados da aplicação de IA
│       ├── 📁 negative/             # Imagens negativas para treinamento
│       ├── 📁 positive/             # Imagens positivas para treinamento
│           ├── 📁 dog1/
│           ├── 📁 dog2/
|           ...
│       ├── 📁 training_checkpoints/ # Checkpoints do treinamento do modelo
│       └── Reconhecimento_Multiplos...  # Script principal de reconhecimento
│
└── README.md
```

---

## Pré-requisitos

### Firmware
- Extensões do VsCode:
   - Platform IO IDE
   - Monitor Serial
- Subsistema WSL2.
   - Configurado para uso da GPU Local.

### Aplicação Web
- Frontend:
   - Django
   - Html
   - CSS
- Backend:
   - Python
   - JavaScript

### Inteligência Artificial
- Treino e construção do modelo CNN:
   - TensorFlow
- PipeLine:
   - Scikit-Learn.Keras
- WebScrapping
   - Sellenium
- Augumentação de Dados:
   - TensorFlow
   - Pillow
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

### WebScrapping usando WSL2

Utiliza-se um Script WebScrapping para a construção do dataset de treinamento. Para que funcione corretamente é necessário realizar a instalação do ``Google Chrome`` no subsistema **Linux** do **Windows**: **WSL2**. Para isso, faça a instalação usando os comandos via cmd:
```
sudo apt update
sudo apt install -y wget curl gpg
curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable
```
Após isso, garanta que o **selenium** tenha permissão suficiente para executar o *webscrapping*:
```
chmod +x /home/siifa/.cache/selenium/chromedriver/linux64/151.0.7922.76/chromedriver
```

#### Orientações
O Script webscrapping tem a funcionalidade de buscar extrair as fotos de uma galeria em uma página web, que contêm diversas páginas de fotos da mesma galeria. O algoritmo acessa a página principal, e de acordo com o número de páginas específicados pelo usuário, acessa as outras páginas/rotas da galeria de fotos. 

Existem duas formas de executar o Script: extração de uma única galeria, ou de várias galerias.

**Única Galeria:** Para extrair fotos de uma única galeria, basta mudar os valores de `BASE_URL` para a url específica e `TOTAL_PAGES` para a quantidade de páginas que a galeria possui.

**Multiplas Galerias:** Para extrair fotos de várias galerias, basta adicionar todas as urls e a quantidade de páginas das respectivas galerias da forma `BASE_URL_LIST = [(url1, pags1), (url2, pags2), ...]`.

`OUTPUT_PATH` sempre será igual a `POS_PATH`, para que as imagens possam serem armazenadas na pasta de imagens positivas, mas você pode alterar seu valor com o que desejar. O Script lê quantos cachorros já existem na pasta, e cria uma pasta com nome específico de acordo com o número de cachorros já salvos. 

> Observa-se a necessidade de realizar uma limpeza nas imagens adquiridas, não esqueça de retirar as imagens que não contém as informações necessárias para o treinamento.

### Django

...

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

- [x] Adicionar arquivo .cpp de configuração da ESP32CAM
- [x] Usar extensão `PlatformIO` para debug do código **arduino** e **esp** diretamente pelo projeto
- [x] Realizar Limpeza de Dados nas pastas `positive/dogx`
- [ ] Verificar se os códigos das placas rodam via **Platformio IDE**
- [ ] Aumentar o Dataset de imagens **positivas** via _webscrapping_ de outros animais e estrurar o conjunto para que funcione com essas novas imagens
- [ ] Melhorar a avaliação do modelo.
- [ ] Reestruturar as pastas do repositório.

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

...

---

<p align="center">Desenvolvido com ❤️ para o bem-estar dos pets 🐶🐱</p>
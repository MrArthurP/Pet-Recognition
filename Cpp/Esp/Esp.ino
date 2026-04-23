#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <PubSubClient.h>
#include <time.h> // Para trabalhar com horários

// Definições
#define TOPICO_SUBSCRIBE "Alimentador_TccRecebe"
#define TOPICO_PUBLISH   "Alimentador_TccEnvio"
#define ID_MQTT  "rakel"

// Pinagem do NodeMCU
#define Motor    5 // D1 (GPIO 5)
#define NivelPrototipo    14 // D5 (GPIO 14)

// Configuração da rede WiFi
const char* SSID = "Arthur";
const char* PASSWORD = "tutu2023";

// URL do servidor Django para enviar dados
const char* SERVER_URL = "http://192.168.185.78:8000/update_button/";

// Configurações MQTT
const char* BROKER_MQTT = "test.mosquitto.org";
int BROKER_PORT = 1883;

// Objetos globais
WiFiClient espClient;
PubSubClient MQTT(espClient);

// Variáveis para armazenar os horários e mensagens
String horario1;
String horario2;
String tempoMotor;
String msg; // Variável global para armazenar a mensagem recebida
bool motorLigado = false;
bool motorLigouNoHorario1 = false;
bool motorLigouNoHorario2 = false;

// Protótipos das funções
void initWiFi();
void initMQTT();
void reconnectWiFi();
void reconnectMQTT();
void VerificaConexoesWiFIEMQTT();
void mqtt_callback(char* topic, byte* payload, unsigned int length);
void ligarMotor(bool porHorario);
void desligarMotor();
void tirarfoto();
void enviaEstadoBotao(int nivel, const String& estado);

void setup() {
    Serial.begin(115200);
    delay(1000);

    pinMode(Motor, OUTPUT);
    digitalWrite(Motor, LOW);

    pinMode(NivelPrototipo, INPUT);

    initWiFi();
    initMQTT();

    // Configura o horário atual
    configTime(-3 * 3600, 0, "pool.ntp.org"); // -3 horas em segundos // Ajuste o fuso horário conforme necessário
}

void loop() {
    VerificaConexoesWiFIEMQTT();
    MQTT.loop();

    // Verifica o horário atual
    time_t now = time(nullptr);
    struct tm *timeinfo = localtime(&now);
    char buffer[6]; // Para armazenar a hora no formato HH:MM
    sprintf(buffer, "%02d:%02d", timeinfo->tm_hour, timeinfo->tm_min);
    Serial.print("Horario 1:");
    Serial.println(horario1);
    Serial.print("Horario 2:");
    Serial.println(horario2);
    Serial.print("Buffer:");
    Serial.println(buffer);

    // Se os horários coincidem, liga o motor apenas uma vez por horário
    if (horario1 == buffer && !motorLigouNoHorario1) {
        ligarMotor(true); // Indica que o motor deve ser ligado pelo horário
        motorLigouNoHorario1 = true;
    } else if (horario2 == buffer && !motorLigouNoHorario2) {
        ligarMotor(true);
        motorLigouNoHorario2 = true;
    }

    // Reseta os flags de controle após passar do horário
    if (horario1 != buffer) {
        motorLigouNoHorario1 = false;
    }
    if (horario2 != buffer) {
        motorLigouNoHorario2 = false;
    }

    // Liga o motor ao receber a mensagem "Start_Motor"
    if (msg == "Start_Motor" && !motorLigado) {
        ligarMotor(false);
    }

    // Mantém o motor ligado até receber "Stop_Motor"
    if (msg == "Stop_Motor") {
        desligarMotor();
    }

    if (msg == "Tirar_Foto") {
        tirarfoto();
    }

    if (msg == "Encher_Alimentador") {
        encherAlimentador();
    }

    // Debounce e leitura do nível do protótipo
    static bool estadoNivelPrototipoAnt = HIGH;
    static unsigned long debounceNivelProt;

    bool estadoNivelPrototipo = digitalRead(NivelPrototipo);

    if ((millis() - debounceNivelProt) > 50) {
        if (estadoNivelPrototipo != estadoNivelPrototipoAnt) {
            debounceNivelProt = millis();
            if (estadoNivelPrototipo) {
              Serial.println("Nivel Baixo");
              enviaEstadoBotao(1, "NivelBaixo");
            } else {
              Serial.println("Nivel Alto");
              enviaEstadoBotao(1, "NivelAlto");
            }
        }
        estadoNivelPrototipoAnt = estadoNivelPrototipo;
    }

    delay(500);  // Ajuste o delay conforme necessário
}

void ligarMotor(bool porHorario) {
    if (!motorLigado) {
        Serial.println("Ligando o motor...");
        digitalWrite(Motor, HIGH);
        motorLigado = true;

        if (porHorario) {
            // Multiplicando tempoMotor por 1000 e convertendo para inteiro
            int tempoEmMilissegundos = tempoMotor.toInt() * 1000;
            delay(tempoEmMilissegundos); // Aguarda o tempo especificado
            desligarMotor(); // Desliga o motor após o tempo especificado
        }
    }
}

void desligarMotor() {
    if (motorLigado) {
        Serial.println("Desligando o motor...");
        digitalWrite(Motor, LOW);
        motorLigado = false;
    }
}

void tirarfoto() {

  Serial.println("Você recebeu o comando para tirar foto");

}

void encherAlimentador() {
    if (!motorLigado) {
        Serial.println("Ligando o motor por 100 segundos...");
        digitalWrite(Motor, HIGH);
        delay(60000);
        motorLigado = true;
    }
}

void initWiFi() {
  delay(10);
  WiFi.disconnect(true);
  delay(1000);
  Serial.println("Conectando-se na rede WiFi...");

  WiFi.begin(SSID, PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  delay(2000);
  Serial.println("Conectado na rede WiFi");
  Serial.println("Endereço IP:");
  Serial.println(WiFi.localIP());
}

void initMQTT() {
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  MQTT.setCallback(mqtt_callback);
}

void reconnectMQTT() {
  while (!MQTT.connected()) {
    Serial.print("* Tentando se conectar ao Broker MQTT: ");
    Serial.println(BROKER_MQTT);
    if (MQTT.connect(ID_MQTT)) {
      Serial.println("Conectado com sucesso ao broker MQTT!");
      MQTT.subscribe(TOPICO_SUBSCRIBE);
    } else {
      Serial.println("Falha ao reconectar no broker.");
      Serial.println("Nova tentativa de conexão em 2s");
      delay(2000);
    }
  }
}

void reconnectWiFi() {
  if (WiFi.status() == WL_CONNECTED)
    return;

  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Reconectado na rede WiFi");
  Serial.println("Endereço IP:");
  Serial.println(WiFi.localIP());
}

void VerificaConexoesWiFIEMQTT() {
  if (!MQTT.connected())
    reconnectMQTT();
  reconnectWiFi();
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
    msg = ""; // Limpa a variável global antes de usá-la
    for (int i = 0; i < length; i++) {
        msg += (char)payload[i];
    }

    Serial.print("Mensagem recebida do tópico: ");
    Serial.println(topic);
    Serial.println(msg); // Print da mensagem recebida

    // Verificação adicional para garantir que a função está sendo chamada
    if (length == 0) {
        Serial.println("Nenhuma mensagem recebida (comprimento = 0)");
    }

    if (msg == "Start_Motor") {
        Serial.println("Recebeu Comando: Start_Motor");
        ligarMotor(false);
    } else if (msg == "Stop_Motor") {
        Serial.println("Recebeu Comando: Stop_Motor");
        desligarMotor();
    } else if (msg.startsWith("Horarios:")) {
        // Processa horários
        int pos1 = msg.indexOf(':') + 1;
        Serial.print("Primeiro pos1:");
        Serial.println(pos1);
        int pos2 = msg.indexOf(',', pos1);
        Serial.print("Primeiro pos2:");
        Serial.println(pos2);
        horario1 = msg.substring(pos1, pos2); // Extrai horario1
        horario1.trim(); // Remove espaços indesejados
        Serial.print("Horario1:");
        Serial.println(horario1);

        pos1 = pos2 + 1; // Atualiza pos1 para o próximo valor
        Serial.print("Segundo pos1:");
        Serial.println(pos1);
        pos2 = msg.indexOf(',', pos1); // Busca o próximo ',' para o tempoMotor
        Serial.print("Segundo pos2:");
        Serial.println(pos2);
        horario2 = msg.substring(pos1, pos2); // Extrai horario2
        horario2.trim(); // Remove espaços indesejados
        Serial.print("Horario2:");
        Serial.println(horario2);

        // Extrai o tempo do motor
        tempoMotor = msg.substring(pos2 + 1); // Extrai tempoMotor (5)
        tempoMotor.trim(); // Remove espaços indesejados
        Serial.print("tempoMotor:");
        Serial.println(tempoMotor);
    } else {
        Serial.println("Mensagem desconhecida ou vazia.");
    }
}
String getCSRFToken() {
    HTTPClient http;
    WiFiClient client;

    String url = "http://192.168.185.78:8000/get_csrf_token/";
    http.begin(client, url);

    int httpResponseCode = http.GET();
    String csrfToken = "";

    if (httpResponseCode > 0) {
        csrfToken = http.getString();
        csrfToken.trim();

        if (csrfToken.startsWith("\"") && csrfToken.endsWith("\"")) {
            csrfToken = csrfToken.substring(1, csrfToken.length() - 1);
        }
    } else {
        Serial.print("Erro ao obter CSRF Token: ");
        Serial.println(httpResponseCode);
    }

    http.end();
    return csrfToken;
}

void enviaEstadoBotao(int nivel, const String& estado) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        WiFiClient client;
        String url = SERVER_URL;
        http.begin(client, url);

        http.addHeader("Content-Type", "application/x-www-form-urlencoded");
        String csrfToken = getCSRFToken();
        http.addHeader("X-CSRFToken", csrfToken);
        // Cria a mensagem para enviar
        
        String mensagem = "nivel=" + String(nivel) + "&estado=" + estado;
        Serial.print("Nivel: ");
        Serial.println(nivel);
        Serial.print("Estado: ");
        Serial.println(estado);

        
        // Print do payload que está sendo enviado
        Serial.println("Enviando payload: " + mensagem);

        int codigoHTTP = http.POST(mensagem);
        String resposta = http.getString();

        Serial.println("Código HTTP da resposta: " + String(codigoHTTP));
        Serial.println("Resposta do servidor: " + resposta);

        http.end();
    }
}




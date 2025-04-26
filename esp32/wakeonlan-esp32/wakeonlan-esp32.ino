#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiUdp.h>
#include <Ticker.h>

Ticker watchdogTicker;
bool shouldReboot = false;

unsigned long lastPingTime = 0;
const unsigned long pingInterval = 5000;

unsigned long lastRestartTime = 0;
const unsigned long restartInterval = 5 * 60 * 1000;

void rebootDevice() {
  Serial.println("Watchdog timeout! Reiniciando...");
  ESP.restart();
}

void feedWatchdog() {
  shouldReboot = false;
  watchdogTicker.once(10, rebootDevice);
}

const char* ssid = "wifi";
const char* password = "password";

byte mac[6] = { 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA };

const char* mqtt_servers[] = {
  "mqtt.eclipseprojects.io",
  "broker.emqx.io",
  "broker.hivemq.com"
};
const int mqtt_port = 1883;
const int num_brokers = 3;
int current_broker = 0;

const char* topic_subscribe = "exampleWakeOnLan/wol";
const char* topic_ping = "exampleWakeOnLan/ping";
const char* topic_publish = "exampleWakeOnLan/feedback";

WiFiClient espClient;
PubSubClient client(espClient);
WiFiUDP udp;

void sendWOL(byte *macAddress) {
  byte magicPacket[102];

  for (int i = 0; i < 6; i++) magicPacket[i] = 0xFF;
  for (int i = 1; i <= 16; i++) {
    for (int j = 0; j < 6; j++) {
      magicPacket[i * 6 + j] = macAddress[j];
    }
  }

  udp.beginPacket("255.255.255.255", 9);
  udp.write(magicPacket, sizeof(magicPacket));
  udp.endPacket();

  Serial.println("Magic packet enviado!");
  client.publish(topic_publish, "WOL_ENVIADO:SUCESSO");
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida [");
  Serial.print(topic);
  Serial.print("] ");

  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  if (message == "ON") {
    udp.begin(9);
    sendWOL(mac);
    Serial.println("Comando WOL executado");
  } else {
    client.publish(topic_publish, "ERRO:COMANDO_INVALIDO");
  }
}

void switchBroker() {
  current_broker = (current_broker + 1) % num_brokers;
  Serial.print("Alternando para o broker: ");
  Serial.println(mqtt_servers[current_broker]);

  client.setServer(mqtt_servers[current_broker], mqtt_port);
}

void reconnect() {
  if (client.connected()) return;

  Serial.println("\nIniciando conexão MQTT...");
  client.setSocketTimeout(30);
  client.setKeepAlive(60);

  String clientId = "ESP32-" + String(mac[3], HEX) + String(mac[4], HEX) + String(mac[5], HEX);

  if (client.connect(clientId.c_str())) {
    Serial.print("Conectado ao broker MQTT: ");
    Serial.println(mqtt_servers[current_broker]);
    client.subscribe(topic_subscribe);
    client.publish(topic_publish, "RECONECTADO");
  } else {
    Serial.print("Falha na conexão com ");
    Serial.print(mqtt_servers[current_broker]);
    Serial.println(". Estado: " + String(client.state()));
    switchBroker();
    delay(2000);
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();

  client.setServer(mqtt_servers[current_broker], mqtt_port);
  client.setCallback(callback);
  client.setBufferSize(128);

  watchdogTicker.once(10, rebootDevice);
  lastRestartTime = millis();
}

void loop() {
  feedWatchdog();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi desconectado, reconectando...");
    setup_wifi();
    delay(1000);
    return;
  }

  if (!client.connected()) {
    reconnect();
  }

  if (millis() - lastPingTime > pingInterval) {
    lastPingTime = millis();
    client.publish(topic_ping, "PING:ONLINE");
    Serial.println("Ping MQTT enviado.");
  }

  if (millis() - lastRestartTime >= restartInterval) {
    Serial.println("Reinício programado: 5 minutos atingidos.");
    ESP.restart();
  }

  client.loop();
  delay(100);
}
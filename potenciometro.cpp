#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

int pinPotenciometro = 34;
int ledPin = 14; // Pin del LED

// URL de la API en Firebase
String serverName = "https://herokuiot-default-rtdb.firebaseio.com/dispositivos/2/valor.json";

unsigned long lastTime = 0;
unsigned long timerDelay = 500;
int lastValorPotenciometro = -1;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  // Conectar a la red WiFi
  WiFi.begin(ssid, password);
  Serial.println("Conectando");
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Conectado a la red WiFi con la dirección IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("Temporizador configurado a 5 segundos (variable timerDelay), tomará 5 segundos antes de publicar la primera lectura.");
}

void loop() {
  // Leer el valor del potenciómetro
  int valorPotenciometro = analogRead(pinPotenciometro);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Convertir el valor del potenciómetro a formato de cadena
    String valorPotStr = String(valorPotenciometro);

    // Iniciar la conexión HTTP a la URL de Firebase
    http.begin(serverName.c_str());

    // Enviar una solicitud HTTP PUT con el valor del potenciómetro
    int httpResponseCodePotenciometro = http.PUT(valorPotStr);

    if (httpResponseCodePotenciometro > 0) {
      Serial.print("Código de respuesta HTTP (Potenciómetro): ");
      Serial.println(httpResponseCodePotenciometro);
      Serial.print("Valor del potenciómetro enviado: ");
      Serial.println(valorPotenciometro);
    } else {
      Serial.print("Código de error (Potenciómetro): ");
      Serial.println(httpResponseCodePotenciometro);
      Serial.print("Valor del potenciómetro no enviado. Error.");
    }

    // Liberar recursos para la solicitud del potenciómetro
    http.end();
  }

  delay(timerDelay);
}
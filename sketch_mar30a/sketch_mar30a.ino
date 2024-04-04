#include <HTTPClient.h>
#include <WiFi.h>
#include <HardwareSerial.h>
#include <WebServer.h>
#include <ESP32Servo.h>

Servo servoMotor;

// Variables para almacenar SSID y contraseña
const int maxChars = 50;  // Tamaño máximo de los strings
char ssid[maxChars];
char password[maxChars];
const uint16_t port = 80;
WebServer server(port);

// Flags para indicar el estado de la conexión WiFi y la confirmación de datos
bool wifiConnected = false;
bool dataConfirmed = false;

void setup() {
  // Inicializamos el puerto serial
  Serial.begin(115200);
  servoMotor.attach(2);
  servoMotor.write(90);

  // Pedimos al usuario que introduzca el SSID por el monitor serie
  Serial.println("Inicializando...");
  Serial.println("Por favor introduzca el SSID:");
  readSerialString(ssid);

  // Pedimos al usuario que introduzca la contraseña por el monitor serie
  Serial.println("Por favor introduzca la contraseña:");
  readSerialString(password);

  // Confirmamos que se han introducido los datos
  dataConfirmed = true;

  // Si los datos están confirmados, intentamos conectarnos a la red WiFi
  if (dataConfirmed) {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Conectando a WiFi...");
    }
    wifiConnected = true;  // Marcamos como conectado una vez que se haya establecido la conexión WiFi
    Serial.println("Conectado a WiFi. exitosamente");
    Serial.println(WiFi.localIP().toString());

    // Configurar la ruta para la petición GET
    server.on("/led", HTTP_GET, handleLed);
    // Iniciar el servidor web
    server.begin();
    Serial.println("Servidor web iniciado en el puerto: ");
    Serial.println(port);
  }
}

void loop() {
  // Manejar las peticiones del servidor web
  server.handleClient();
}

// Función para leer una cadena desde el puerto serial
void readSerialString(char *buffer) {
  int index = 0;
  while (true) {
    while (!Serial.available()) {
      // Esperar hasta que se reciba un dato
    }
    char receivedChar = Serial.read();
    if (receivedChar == '\n' || receivedChar == '\r' || index >= maxChars - 1) {
      buffer[index] = '\0';  // Terminar la cadena
      break;
    }
    buffer[index++] = receivedChar;
  }
}

void handleLed() {
  // Imprimir "Petición recibida" en el monitor serial
  Serial.println("Petición recibida");

  // Obtener el parámetro numérico de la petición HTTP
  String numberStr = server.arg("number");
  if (numberStr.length() > 0) {
    int angle = numberStr.toInt(); // Convertir el String a entero
    //aqui movemos el servo x grados
    if(angle >= 0 && angle <= 180){
      servoMotor.write(angle); // Mueve el servo al ángulo especificado
      Serial.println("Ángulo modificado a: " + String(angle)); 
    } else {
      Serial.println("Error: El ángulo debe estar entre 0 y 180 grados"); // Imprime un mensaje de error si el ángulo está fuera del rango válido
    }
  }

  // Enviar una respuesta a la petición HTTP
  server.send(200, "text/plain", "Petición recibida");
}

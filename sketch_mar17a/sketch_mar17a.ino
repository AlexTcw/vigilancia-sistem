#include <ESP32Servo.h>

Servo servoMotor;

void setup() {
  Serial.begin(115200);
  servoMotor.attach(2);
  servoMotor.write(90);
  Serial.println("Ingrese un angulo");

}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt(); // Lee el ángulo como un entero desde el monitor serie
    if (angle >= 0 && angle <= 180) { // Verifica si el ángulo está dentro del rango válido
      servoMotor.write(angle); // Mueve el servo al ángulo especificado
      Serial.println("Angulo modificado a: " + String(angle)); // Imprime el ángulo modificado en el monitor serie
    } else {
      Serial.println("Error: El angulo debe estar entre 0 y 180 grados"); // Imprime un mensaje de error si el ángulo está fuera del rango válido
    }
    while (Serial.available() > 0) {
      Serial.read(); // Limpia el buffer serial
    }
  }
}

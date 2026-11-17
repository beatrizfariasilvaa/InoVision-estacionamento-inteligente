#include <Servo.h>

const int PINO_SERVO = 9;
const int PINO_SENSOR[3] = {2, 3, 4};
const int PINO_VERDE[3] = {5, 7, 10};
const int PINO_VERMELHO[3] = {6, 8, 11};

const int CANCELA_FECHADA = 0;              
const int CANCELA_ABERTA  = 90;             
const unsigned long TEMPO_ABERTA = 3000;    

Servo cancela;
String estadoAnterior = "";   

void setup() {
  Serial.begin(9600);
  Serial.println("INICIO");
  cancela.attach(PINO_SERVO);
  cancela.write(CANCELA_FECHADA);

  for (int i = 0; i < 3; i++) {
    pinMode(PINO_SENSOR[i], INPUT);         
    pinMode(PINO_VERDE[i], OUTPUT);
    pinMode(PINO_VERMELHO[i], OUTPUT);
  }
}


String lerVagas() {
  String estado = "";
  for (int i = 0; i < 3; i++) {
    bool ocupada = digitalRead(PINO_SENSOR[i]) == LOW;
    digitalWrite(PINO_VERMELHO[i], ocupada ? HIGH : LOW);
    digitalWrite(PINO_VERDE[i], ocupada ? LOW : HIGH);
    estado += ocupada ? "1" : "0";
  }
  return estado;
}

void abrirCancela() {
  cancela.write(CANCELA_ABERTA);
  delay(TEMPO_ABERTA);
  cancela.write(CANCELA_FECHADA);
}

void loop() {
  String estado = lerVagas();
  if (estado != estadoAnterior) {
    Serial.print("VAGAS:");
    Serial.println(estado);
    estadoAnterior = estado;
  }

  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    if (comando == "ABRIR") {
      Serial.println("OK:ABRINDO");
      abrirCancela();
    }
  }

  delay(50);
}

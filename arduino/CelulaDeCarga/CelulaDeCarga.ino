#include "HX711.h"

// Definindo os pinos do HX711
#define DOUT 7  // Data Out do HX711
#define SCK 5   // SCK do HX711
#define LSL_Prototipo 4

HX711 scale;  // Instância do HX711

float calibration_factor = -7050; // Ajuste esse valor para calibrar

void setup() {
  Serial.begin(115200);
  pinMode(LSL_Prototipo, OUTPUT);
  
  // Configurando a célula de carga
  scale.begin(DOUT, SCK);
  scale.set_scale(calibration_factor);   // Ajusta o fator de escala inicial
  scale.tare();        // Zera a balança
  
  Serial.println("Coloque um peso conhecido na balança para calibrar.");
  delay(5000); // Espera 5 segundos para você colocar o peso
}

void loop() {
  // Lendo o valor da célula de carga
  float weight = scale.get_units(10);  // Média de 10 leituras
  
  // Imprimindo o valor no Serial Monitor
  Serial.print("Peso: ");
  Serial.print(weight);
  Serial.println(" g");
  
  // Se você conhece o peso que está na balança, ajuste o fator de calibração
  // Exemplo: Se o peso conhecido é 500g e a leitura é 450g, você pode ajustar assim:
  Serial.print("Fator de Calibração Atual: ");
  Serial.println(calibration_factor);
  if (weight > 3.5){
    Serial.println("Nível alto");
    digitalWrite(LSL_Prototipo, LOW); //Nível alto
  } else {
    Serial.println("Nível baixo");
    digitalWrite(LSL_Prototipo, HIGH); // Nível baixo
  }
  delay(1000);  // Espera 1 segundo antes da próxima leitura
}

// #define ADDO 7 //Data Out
// #define ADSK 5 //SCK
// #define LSL_Prototipo 4

// unsigned long ReadCount();
// unsigned long convert;

// void setup() {
//   pinMode(ADDO, INPUT_PULLUP);
//   pinMode(ADSK, OUTPUT);
//   pinMode(LSL_Prototipo, OUTPUT);

//   Serial.begin(115200);
//   // put your setup code here, to run once:

// }

// void loop() {

//   convert = ReadCount();
//   Serial.println(convert);
//   delay(2000);
//   // put your main code here, to run repeatedly:

//   if (convert > 8239800){
//     Serial.println("Nível alto");
//     digitalWrite(LSL_Prototipo, LOW); //Nível alto
//   }else{
//     Serial.println("Nível baixo");
//     digitalWrite(LSL_Prototipo, HIGH); // Nível baixo
//   }


// }

// unsigned long ReadCount(){
//   unsigned long Count = 0;
//   unsigned char i;

//   digitalWrite(ADSK, LOW);
//   while(digitalRead(ADDO));

//   for(i=0;i<24;i++){
//     digitalWrite(ADSK, HIGH);
//     Count = Count <<1;
//     digitalWrite(ADSK, LOW);
//     if(digitalRead(ADDO)) Count++;
//   }
//   digitalWrite(ADSK, HIGH);
//   Count = Count^0x800000;
//   digitalWrite(ADSK, LOW);

//   return(Count);
// }

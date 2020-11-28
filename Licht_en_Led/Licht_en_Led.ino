int ldrPin = A0;              // poort waar de sensor aan zit
int ldrVal = 0;               // defineer dewaarde 
int LedDicht = 13;             // poort waar de LED aan zit 
int LedOpen = 12;             // poort waar de LED aan zit 
int counter;
char Data = 'A';

void setup() {
  Serial.begin(9600);         
  pinMode(13, OUTPUT);        
  pinMode(12, OUTPUT);   
}

void blink(int ledPin){  
  counter =0;
  while(counter<6){
    digitalWrite(ledPin, HIGH);
    delay(1000);
    digitalWrite(ledPin, LOW);
    delay(1000);
    counter+=1;
  }
  
}



void loop() {
   
  ldrVal = analogRead(ldrPin);    
  Serial.println(ldrVal);       
  Data = Serial.read();  

  if(Serial.read() == 'H'){
    blink(LedDicht);
    Data = 'G';   
  }
  if(Serial.read() == 'D'){
    blink(LedOpen);
    Data = 'G';  
  }
  

  delay(100);                     // Pause 100ms
  
  
}

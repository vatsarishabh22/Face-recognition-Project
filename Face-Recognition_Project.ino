int data;
int led = 13;


void setup() {
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  digitalWrite(led,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available())
    {
      data = Serial.read();

      if(data == '1')
        {
          digitalWrite(led,HIGH);
        }
      if(data == '0')
      {
        digitalWrite(led,LOW);
      }
    }
  

}

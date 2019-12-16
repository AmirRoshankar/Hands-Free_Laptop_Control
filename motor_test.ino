// from left to right (0 1 2 3)(yellow wires to hbridge)
//left to right wire order
//black white grey purple

int leftEchoPin = 6;    // Echo
int leftTrigPin = 5;    // Trigger
int rightEchoPin = 3;    // Echo
int rightTrigPin = 2;    // Trigger
long leftDuration, rightDuration, leftCm, rightCm;

int pin8 = 8;
int pin9 = 9;
int pin10 = 10;
int pin11 = 11;

int currentState = 0;

void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(leftTrigPin, OUTPUT);
  pinMode(leftEchoPin, INPUT);
  pinMode(rightTrigPin, OUTPUT);
  pinMode(rightEchoPin, INPUT);

  pinMode(pin8, OUTPUT);
  pinMode(pin9, OUTPUT);
  pinMode(pin10, OUTPUT);
  pinMode(pin11, OUTPUT);
}

// set state of the 4 pins
void setState0() {
  digitalWrite(pin8, HIGH);
  digitalWrite(pin9, LOW);
  digitalWrite(pin10, LOW);
  digitalWrite(pin11, HIGH);
  currentState = 0;
  Serial.println(currentState);
}

void setState1() {
  digitalWrite(pin8, HIGH);
  digitalWrite(pin9, LOW);
  digitalWrite(pin10, HIGH);
  digitalWrite(pin11, LOW);
  currentState = 1;
  Serial.println(currentState);
}

void setState2() {
  digitalWrite(pin8, LOW);
  digitalWrite(pin9, HIGH);
  digitalWrite(pin10, HIGH);
  digitalWrite(pin11, LOW);
  currentState = 2;
  Serial.println(currentState);
}

void setState3() {
  digitalWrite(pin8, LOW);
  digitalWrite(pin9, HIGH);
  digitalWrite(pin10, LOW);
  digitalWrite(pin11, HIGH);
  currentState = 3;
  Serial.println(currentState);
}

int loopCount = 0;

void loop() {
  // put your main code here, to run repeatedly:
  if (loopCount % 500 == 0) {
    currentState = 3 - currentState;
    Serial.print(loopCount);
    delay(1000);
  }
  if ((loopCount % 1000) < 500)  {
    switch (currentState) {
      case 0:
        setState3();
        break;
      case 1:
        setState0();
        break;
      case 2:
        setState1();
        break;
      case 3:
        setState2();
    }
  } else {
    switch (currentState) {
      case 0:
        setState1();
        break;
      case 1:
        setState2();
        break;
      case 2:
        setState3();
        break;
      case 3:
        setState0();
    }
  }
  loopCount++;
  // delay(1);
}

// from left to right (0 1 2 3)(yellow wires to hbridge)


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
}

void setState1() {
    digitalWrite(pin8, HIGH);
    digitalWrite(pin9, LOW);
    digitalWrite(pin10, HIGH);
    digitalWrite(pin11, LOW);
    currentState = 1;
}

void setState2() {
    digitalWrite(pin8, LOW);
    digitalWrite(pin9, HIGH);
    digitalWrite(pin10, HIGH);
    digitalWrite(pin11, LOW);
    currentState = 2;
}

void setState3() {
    digitalWrite(pin8, LOW);
    digitalWrite(pin9, HIGH);
    digitalWrite(pin10, LOW);
    digitalWrite(pin11, HIGH);
    currentState = 3;
}

// main loop 
void loop() {
    // get data from left sensor 
    sum = 0;
    for (int i = 0; i < 10; i++)
    {
      digitalWrite(leftTrigPin, HIGH);
      delayMicroseconds(20);
      digitalWrite(leftTrigPin, LOW);

      leftDuration = pulseIn(leftEchoPin, HIGH);
      sum += (leftDuration/2) / 29.1;  
    }

    leftCm = sum /10.0;
       

    Serial.print("Left sensor: ");
    Serial.print(leftCm);
    Serial.print("cm");
    Serial.println();


    // get data from right sensor 
    sum = 0;
    for (int i = 0; i < 10; i++)
    {
      digitalWrite(rightTrigPin, HIGH);
      delayMicroseconds(20);
      digitalWrite(rightTrigPin, LOW);

      rightDuration = pulseIn(rightEchoPin, HIGH);
      sum += (rightDuration/2) / 29.1; 
    }
    
    rightCm = sum/10.0;   

    Serial.print("Right sensor: ");
    Serial.print(rightCm);
    Serial.print("cm");
    Serial.println();
  

    if (rightCm < 15 && leftCm > 15){
        // clockwise (0 - 1 - 2 - 3)
        switch (currentState) {
            case 0:
                setState1;
                break;
            case 1:
                setState2;
                break;
            case 2:
                setState3;
                break;
            case 3:
                setState0;
        }
    }  else if(rightCm > 15 && leftCm < 15) {
        // counterclockwise (3 - 2 - 1 - 0)
        switch (currentState) {
            case 0:
                setState3;
                break;
            case 1:
                setState0;
                break;
            case 2:
                setState1;
                break;
            case 3:
                setState2;
        }
    }
    else {
      // holds the rotor in place
        switch (currentState) {
            case 0:
                setState0();
                break;
            case 1:
                setState1();
                break;
            case 2:
                setState2();
                break;
            case 3:
                setState3();
        }
    }
    }
}

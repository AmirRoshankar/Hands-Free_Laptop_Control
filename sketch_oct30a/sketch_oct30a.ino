int leftEchoPin = 6;    // Echo
int leftTrigPin = 5;    // Trigger
int rightEchoPin = 11;    // Echo
int rightTrigPin = 10;    // Trigger
long leftDuration, rightDuration, leftCm, rightCm;
 
void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(leftTrigPin, OUTPUT);
  pinMode(leftEchoPin, INPUT);
  pinMode(rightTrigPin, OUTPUT);
  pinMode(rightEchoPin, INPUT);
}
 
void loop() {
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  //digitalWrite(leftTrigPin, LOW);
  //delayMicroseconds(5);
  digitalWrite(leftTrigPin, HIGH);
  delayMicroseconds(20);
  digitalWrite(leftTrigPin, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  //pinMode(leftEchoPin, INPUT);
  leftDuration = pulseIn(leftEchoPin, HIGH);
 
  // Convert the time into a distance
  leftCm = (leftDuration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343

  Serial.print("Sensor 1: ");
  Serial.print(leftCm);
  Serial.print("cm");
  Serial.println();

  delay(1000);

  //sensor 2

  //digitalWrite(rightTrigPin, LOW);
  //delayMicroseconds(5);
  digitalWrite(rightTrigPin, HIGH);
  delayMicroseconds(20);
  digitalWrite(rightTrigPin, LOW);
  //delay(250);

  //pinMode(rightEchoPin, INPUT);
  rightDuration = pulseIn(rightEchoPin, HIGH);

  rightCm = (rightDuration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  
  Serial.print("Sensor 2: ");
  Serial.print(rightCm);
  Serial.print("cm");
  Serial.println();

  delay(1000);
}

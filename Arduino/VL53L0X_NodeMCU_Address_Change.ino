#include <Wire.h> //Import wire library
#include <VL53L0X.h> //Import VL530X library

VL53L0X sensor1;
VL53L0X sensor2;

#define MAX_DIST 500          // Maximum distance for Valid Measurement
#define VALID_TIME_LIMIT 500  // Time to keep a minimum value in milliseconds
#define HEIGHT_FOR_MIN 100    // Number of mm for a min to be a min

int minDist1;
unsigned long minTime1;
int isValid1;

int minDist2;
unsigned long minTime2;
int isValid2;

void setup() {

  pinMode(D5, OUTPUT);
  pinMode(D6, OUTPUT);
  digitalWrite(D5, LOW);
  digitalWrite(D6, LOW);

  delay(500);
  Wire.begin();


  Serial.begin (115200);

  //SENSOR 1
  pinMode(D5, INPUT);
  delay(150);
  Serial.println("00");
  sensor1.init(true);
  Serial.println("01");
  delay(100);
  sensor1.setAddress((uint8_t)30);
  Serial.println("02");

  //SENSOR 2
  pinMode(D6, INPUT);
  delay(150);
  sensor2.init(true);
  Serial.println("03");
  delay(100);
  sensor2.setAddress((uint8_t)31);
  Serial.println("04");

  Serial.println("");
  Serial.println("addresses set");
  Serial.println("");
  Serial.println("");

  sensor1.setTimeout(500);
  sensor2.setTimeout(500);

  sensor1.startContinuous();
  sensor2.startContinuous();

  minDist1 = MAX_DIST + 1;
  minTime1 = 0;
  isValid1 = 0;

  minDist2 = MAX_DIST + 1;
  minTime2 = 0;
  isValid2 = 0;
}

void loop() {
  int distance1 = sensor1.readRangeSingleMillimeters();
  unsigned long time1 = millis();
  int distance2 = sensor2.readRangeSingleMillimeters();
  unsigned long time2 = millis();

//  Serial.printf("distance1 = % 5d, time1 = %12d, distance2 = % 5d, Time2 = %12d\n", distance1, time1, distance2, time2);

  // Check for a new minimum reading
  if (distance1 > 0 and distance1 < MAX_DIST and distance1 < minDist1) {
    minDist1 = distance1;
    minTime1 = time1;
    isValid1 = 0;
    //    Serial.println("New Min Reading");
  }


  // Check if found minimum
  if (distance1 > (minDist1 + HEIGHT_FOR_MIN) and (time1 - minTime1) < VALID_TIME_LIMIT) {
    isValid1 = 1;
    //    Serial.println("Found Minimum 1");
  }

  // Make Min invalid if too old
  if ((time1 - minTime1) > VALID_TIME_LIMIT) {
    minDist1 = MAX_DIST + 1;
    minTime1 = 0;
    isValid1 = 0;
    //    Serial.println("Min is stale");
  }

  // Check for a new minimum reading
  if (distance2 > 0 && distance2 < MAX_DIST && distance2 < minDist2) {
    minDist2 = distance2;
    minTime2 = time2;
    isValid2 = 0;
    //    Serial.println("New Min Reading");
  }

  // Check if found minimum
  if (distance2 > (minDist2 + HEIGHT_FOR_MIN) and (time2 - minTime2) < VALID_TIME_LIMIT) {
    isValid2 = 1;
    //    Serial.println("Found Minimum 2");
  }

  // Make Min invalid if too old
  if ((time2 - minTime2) > VALID_TIME_LIMIT) {
    minDist2 = MAX_DIST + 1;
    minTime2 = 0;
    isValid2 = 0;
    //    Serial.println("Min is stale");
  }

  //  Serial.printf("Min1 = % 5d, Time1 = %12d, Valid1 = % d, Min2 = % 5d, Time2 = %12d, Valid2 = % d\n", minDist1, minTime1, isValid1, minDist2, minTime2, isValid2);

  if (isValid1 && isValid2) {
    if (minTime1 < minTime2) {
      Serial.println("\nForward");
    }
    else {
      Serial.println("\nBackward");
    }
    minDist1 = MAX_DIST + 1;
    minTime1 = 0;
    isValid1 = 0;
    minDist2 = MAX_DIST + 1;
    minTime2 = 0;
    isValid2 = 0;
  }
}

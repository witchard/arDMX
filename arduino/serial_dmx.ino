#include <DmxSimple.h>

// After installing, switch to Serial Monitor and set the baud rate to 9600.
//
// Type commands in the box and hit 'Send'.
//
// <number>c : Select a DMX channel
// <number>v : Set DMX channel to new value

void setup() {
  Serial.begin(9600);
  Serial.print("SerialToDmx ready with ");
  Serial.print(DMX_SIZE);
  Serial.println(" channels");
  Serial.println();
  Serial.println("Syntax:");
  Serial.println(" 123c : use DMX channel 123");
  Serial.println(" 45w  : set current channel to value 45");
}

int value = 0;
int channel = 0;

void loop() {
  int c;

  while(!Serial.available());
  c = Serial.read();
  if ((c>='0') && (c<='9')) {
    value = 10*value + c - '0';
  } else {
    if (c=='c') {
      channel = value;
      //Serial.println("Got Channel");
    }
    else if (c=='w') {
      DmxSimple.write(channel, value);
      //Serial.print("Written value");
      Serial.println();
    }
    value = 0;
  }
}

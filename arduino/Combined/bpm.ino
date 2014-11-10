#include "headers.h"

/* Slightly adapted from: http://pulsesensor.myshopify.com/pages/code-and-guide */

//const int pin_pulse = 0;
//const int pin_blink = 13;
//const int pin_fade = 5;
//const int fadeRate = 0;
#define PIN_PULSE 14
//#define PIN_BLINK 13
//#define PIN_FADE 5
//#define FADE_RATE 0
int BPM;

volatile int Signal;
volatile int IBI = 600;
volatile boolean Pulse = false;
volatile boolean QS = false;

void setupBPM(){
  BPMInterruptSetup();
}

void readBPM(){
  if (QS == true){                      
    Serial.print("BPM;");
    Serial.print(BPM);
    Serial.print(";");
    Serial.println();
    QS = false;    
  }
}

volatile int rate[10];                    // array to hold last ten IBI values
volatile unsigned long sampleCounter = 0;          // used to determine pulse timing
volatile unsigned long lastBeatTime = 0;           // used to find IBI
volatile int P =512;                      // used to find peak in pulse wave, seeded
volatile int T = 512;                     // used to find trough in pulse wave, seeded
volatile int thresh = 512;                // used to find instant moment of heart beat, seeded
volatile int amp = 100;                   // used to hold amplitude of pulse waveform, seeded
volatile boolean firstBeat = true;        // used to seed rate array so we startup with reasonable BPM
volatile boolean secondBeat = false;      // used to seed rate array so we startup with reasonable BPM

//http://www.protostack.com/blog/2010/09/timer-interrupts-on-an-atmega168/
void BPMInterruptSetup(){     
  // Initializes Timer2 to throw an interrupt every 2mS.
//  TCCR2A = 0x02;     // DISABLE PWM ON DIGITAL PINS 3 AND 11, AND GO INTO CTC MODE (=_BV(WGM01))
//  TCCR2B = 0x06;     // DON'T FORCE COMPARE, 256 PRESCALER  (= _BV(CS01) | _BV(CS02)) (?means external clock source on T0 pin)
//  OCR2A = 0X7C;      // SET THE TOP OF THE COUNT TO 124 FOR 500Hz SAMPLE RATE
//  TIMSK2 = 0x02;     // ENABLE INTERRUPT ON MATCH BETWEEN TIMER2 AND OCR2A
  TCCR1A = _BV(WGM11);   //CTC-mode (PWM on pins 9 and 10 disabled)
  TCCR1B = _BV(CS00) | _BV(CS01);    //64 prescalar
  OCR1A = 500;          //value 500 (500/16000000*64 = .002)
  TIMSK1 = _BV(OCIE1A);  //enable A-timer
//  TCCR1C = _BV(FOC1A);  //Force compare
  sei();             // MAKE SURE GLOBAL INTERRUPTS ARE ENABLED      
} 


// THIS IS THE TIMER 2 INTERRUPT SERVICE ROUTINE. 
// Timer 2 makes sure that we take a reading every 2 miliseconds
unsigned int current_value = 0;
uint32_t previous_time = 0;
ISR(TIMER1_COMPA_vect){                         // triggered when Timer2 counts to 124

  //Serial.println(millis()-previous_time);
  //previous_time = millis();
  //uint32_t start_time = micros();
  //cli();                // disable interrupts while we do this

  ++current_value;
  current_value %= 1000;
  //digitalWrite(9, current_value > 500);
  //sei(); return;
  Signal = analogRead(PIN_PULSE);              // read the Pulse Sensor 
  return;
//  sei();return;
  sampleCounter += 2;                         // keep track of the time in mS with this variable
  int N = sampleCounter - lastBeatTime;       // monitor the time since the last beat to avoid noise

    //  find the peak and trough of the pulse wave
  if(Signal < thresh && N > (IBI/5)*3){       // avoid dichrotic noise by waiting 3/5 of last IBI
    if (Signal < T){                        // T is the trough
      T = Signal;                         // keep track of lowest point in pulse wave 
    }
  }

  if(Signal > thresh && Signal > P){          // thresh condition helps avoid noise
    P = Signal;                             // P is the peak
  }                                        // keep track of highest point in pulse wave

  //  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
  // signal surges up in value every time there is a pulse
  if (N > 250){                                   // avoid high frequency noise
    if ( (Signal > thresh) && (Pulse == false) && (N > (IBI/5)*3) ){        
      Pulse = true;                               // set the Pulse flag when we think there is a pulse
      //digitalWrite(pin_blink,HIGH);                // turn on pin 13 LED
      IBI = sampleCounter - lastBeatTime;         // measure time between beats in mS
      lastBeatTime = sampleCounter;               // keep track of time for next pulse

      if(secondBeat){                        // if this is the second beat, if secondBeat == TRUE
        secondBeat = false;                  // clear secondBeat flag
        for(int i=0; i<=9; i++){             // seed the running total to get a realisitic BPM at startup
          rate[i] = IBI;                      
        }
      }

      if(firstBeat){                         // if it's the first time we found a beat, if firstBeat == TRUE
        firstBeat = false;                   // clear firstBeat flag
        secondBeat = true;                   // set the second beat flag
        sei();                               // enable interrupts again
        return;                              // IBI value is unreliable so discard it
      }   


      // keep a running total of the last 10 IBI values
      word runningTotal = 0;                  // clear the runningTotal variable    

      for(int i=0; i<=8; i++){                // shift data in the rate array
        rate[i] = rate[i+1];                  // and drop the oldest IBI value 
        runningTotal += rate[i];              // add up the 9 oldest IBI values
      }

      rate[9] = IBI;                          // add the latest IBI to the rate array
      runningTotal += rate[9];                // add the latest IBI to runningTotal
      runningTotal /= 10;                     // average the last 10 IBI values 
      BPM = 60000/runningTotal;               // how many beats can fit into a minute? that's BPM!
      QS = true;                              // set Quantified Self flag 
      // QS FLAG IS NOT CLEARED INSIDE THIS ISR
    }                       
  }

  if (Signal < thresh && Pulse == true){   // when the values are going down, the beat is over
    //digitalWrite(pin_blink,LOW);            // turn off pin 13 LED
    Pulse = false;                         // reset the Pulse flag so we can do it again
    amp = P - T;                           // get amplitude of the pulse wave
    thresh = amp/2 + T;                    // set thresh at 50% of the amplitude
    P = thresh;                            // reset these for next time
    T = thresh;
  }

  if (N > 2500){                           // if 2.5 seconds go by without a beat
    thresh = 512;                          // set thresh default
    P = 512;                               // set P default
    T = 512;                               // set T default
    lastBeatTime = sampleCounter;          // bring the lastBeatTime up to date        
    firstBeat = true;                      // set these to avoid noise
    secondBeat = false;                    // when we get the heartbeat back
  }

  sei();   // enable interrupts when youre done!
  //Serial.print("current length: ");
  //Serial.println(micros()-start_time);
  //Serial.print("idle: ");
  //Serial.println(micros()-previous_time);
  //previous_time = micros();
  //Serial.print("one method: ");Serial.println(millis()-previous_time);
}// end isr




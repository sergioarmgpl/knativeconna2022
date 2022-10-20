import RPi.GPIO as GPIO
import time

PIN = 24;  #Infrared receiving pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN,GPIO.IN,GPIO.PUD_UP)

ledPin1 = 25  #define led pin1
ledPin2 = 23  #define led pin2
ledPin3 = 21  #running program led pin
GPIO.setup(ledPin1,GPIO.OUT)
GPIO.setup(ledPin2,GPIO.OUT)
GPIO.setup(ledPin3,GPIO.OUT)
GPIO.output(ledPin1,GPIO.LOW)
GPIO.output(ledPin2,GPIO.LOW)
print("irm test start...")
#GPIO.output(ledPin1,GPIO.HIGH)  #turn on led
GPIO.output(ledPin3,GPIO.HIGH)  #turn on led
#print("turn on red led")

def exec_cmd(key_val):
    if(key_val==0x16):
        print("Button 1")
    elif(key_val==0x19):
        print("Button 2")
    elif(key_val==0x4a):
        print("Button #")

try:
    print("inside while")
    while True:
        if GPIO.input(PIN) == 0:
            count = 0
            while GPIO.input(PIN) == 0 and count < 200:  # Wait for 9ms LOW level boot code and exit the loop if it exceeds 1.2ms
                count += 1
                time.sleep(0.00006)

            count = 0
            while GPIO.input(PIN) == 1 and count < 80:   # Wait for a 4.5ms HIGH level boot code and exit the loop if it exceeds 0.48ms
                count += 1
                time.sleep(0.00006)

            idx = 0  # byte count variable
            cnt = 0  #Variable per byte bit
            #There are 4 bytes in total. The first byte is the address code, the second is the address inverse code, 
            #the third is the control command data of the corresponding button, and the fourth is the control command inverse code
            data = [0,0,0,0]
            for i in range(0,32):  # Start receiving 32BITE data
                count = 0
                while GPIO.input(PIN) == 0 and count < 15:  # Wait for the LOW LOW level of 562.5US to pass and exit the loop if it exceeds 900US
                    count += 1
                    time.sleep(0.00006)

                count = 0
                while GPIO.input(PIN) == 1 and count < 40:  # waits for logical HIGH level to pass and exits the loop if it exceeds 2.4ms
                    count += 1
                    time.sleep(0.00006)
                
                # if count>8, that is, the logical time is greater than 0.54+0.562=1.12ms, that is, 
                #the period is greater than the logical 0 period, that is equivalent to receiving logical 1
                if count > 8:   
                    data[idx] |= 1<<cnt    #When idx=0 is the first data  data[idx] = data[idx] | 1<<cnt   00000001 <<1 == 0000 0010
                if cnt == 7:    #With 8 byte
                    cnt = 0     #Displacement qing 0
                    idx += 1    #Store the next data
                else:
                    cnt += 1   #The shift adds 1
            #Determine whether address code + address inverse code =0xff, control code + control inverse code = 0xFF
            if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  
                 print("Get the key: 0x%02x" %data[2])  #Data [2] is the control code we need
                 exec_cmd(data[2])
                 if data[2] == 0x19:
                     GPIO.output(ledPin1,GPIO.HIGH)  #turn on led
                     print("turn on red led")
                 elif data[2] == 0x1b:
                     GPIO.output(ledPin2,GPIO.HIGH)  #turn on led
                     print("turn on green led")                    
                 if(data[2] == 0x1f):
                     GPIO.output(ledPin1,GPIO.LOW)  #turn off red led
                     GPIO.output(ledPin2,GPIO.LOW)  #turn off green led
                     print("turn off leds")
except KeyboardInterrupt:
    GPIO.cleanup()


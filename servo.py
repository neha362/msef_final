import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, motor_config): 
        self.S1 = int(motor_config['s1'])
        self.S2 = int(motor_config['s2'])
        self.S3 = int(motor_config['s3']) #water
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.S1, GPIO.OUT)
        GPIO.setup(self.S2, GPIO.OUT)
        GPIO.setup(self.S3, GPIO.OUT)
        self.P1 = GPIO.PWM(self.S1, 50) # GPIO 15 for PWM with 50Hz
        self.P2 = GPIO.PWM(self.S2, 50)
        self.P3 = GPIO.PWM(self.S3, 50)
        
    def rotate(self, angle1, angle2):
        # extend or retract
        dutycycle = ((angle1/18.0) + 2.0)
        #print(str(dutycycle))
        self.P1.ChangeDutyCycle(dutycycle) #10
        dutycycle = ((angle2/18.0) + 2.0)
        #print(str(dutycycle))
        self.P2.ChangeDutyCycle(dutycycle) #5  
        #print('servo testing')
        
    def start(self): 
        self.P1.start(0)
        self.P2.start(0)

        
    def pause(self):
        self.P1.stop()
        self.P2.stop()
        self.P3.stop()
    
    def shut_down(self):
        self.pause()
        GPIO.cleanup() #check on this -- should be in main program
        
    def spray_water(self):
        print('Spraying water')
        self.P3.start(0)
        time.sleep(1)
        self.P3.ChangeDutyCycle(10.25)
        time.sleep(1) 
        self.P3.ChangeDutyCycle(3.25)
        time.sleep(3)
        self.P3.ChangeDutyCycle(0)
        
    def move_arm(self, ai, ae, bi, be, direction):
        i=ai
        j=bi
        self.P1.ChangeDutyCycle(ai)
        self.P2.ChangeDutyCycle(bi)
        while(i!=ae or j!=be):
            position_a = 1./18.*(i)+2
            position_b = 1./18.*(i)+2
            #print('1 up ' + str(ai+diffa))
            if (i != ae):
                self.P1.ChangeDutyCycle(position_a)
                i+=direction
            #print('2 up ' + str(bi+diffb))
            if (j != be):
                self.P2.ChangeDutyCycle(position_b)
                j+=direction
            time.sleep(0.05)

'''
d = {'s1': '15', 's2': '14', 's3': '21'}
s = Servo(d)
s.start()
#s.rotate(0,0)
s.spray_water(0,90,1)
time.sleep(1)
s.spray_water(90,0,-1)
time.sleep(2)

#s.move_arm(0,30,0,30,1)
print('extend')


#s.rotate(45,45)
print('retract')
#s.move_arm(30,0,30,0,-1)

#s.rotate(0,0)


print('shutdw')
s.shut_down()
'''
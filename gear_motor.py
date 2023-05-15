
import time
import math

import RPi.GPIO as GPIO

class GearMotor:
    def ticksCounterLeft(self, pin):
        #global tick_count_left
        self.tick_count_left += 1
        #print('in tick ' + str(self.tick_count_left) + ' ')

    def ticksCounterRight(self, pin):
        #global tick_count_right
        self.tick_count_right += 1
        
    def __init__(self, gear_motor_config):
        print('init motor')
        self.tick_count_left = 0
        self.tick_count_right = 0
        self.A1 = int(gear_motor_config['a1'])
        self.A2 = int(gear_motor_config['a2'])
        self.B1 = int(gear_motor_config['b1'])
        self.B2 = int(gear_motor_config['b2'])
        self.enA = int(gear_motor_config['ena'])
        self.enB = int(gear_motor_config['enb'])
        self.enAA = int(gear_motor_config['enaa'])
        self.enBB = int(gear_motor_config['enbb'])
        self.tickA = int(gear_motor_config['ticka'])
        self.tickB = int(gear_motor_config['tickb'])
        print(self.A1 , self.A2, self.B1, self.B2)
        # Setup GPIO5 to read left wheel encoder
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.tickA, GPIO.IN)
        GPIO.add_event_detect(self.tickA, GPIO.BOTH, callback=self.ticksCounterRight)

        # Setup GPIO12 to read right wheel encoder
        GPIO.setup(self.tickB, GPIO.IN)
        GPIO.add_event_detect(self.tickB, GPIO.BOTH, callback=self.ticksCounterLeft)

        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.A2, GPIO.OUT)
        GPIO.setup(self.B1, GPIO.OUT)
        GPIO.setup(self.B2, GPIO.OUT)
        GPIO.setup(self.enA,GPIO.OUT)
        GPIO.setup(self.enB,GPIO.OUT)
        GPIO.setup(self.enAA,GPIO.OUT)
        GPIO.setup(self.enBB,GPIO.OUT)
        GPIO.output(self.enA,GPIO.LOW)
        GPIO.output(self.enB,GPIO.LOW)
        GPIO.output(self.enAA,GPIO.LOW)
        GPIO.output(self.enBB,GPIO.LOW)
        self.pA=GPIO.PWM(self.enA,100)
        self.pB=GPIO.PWM(self.enB,100)
        self.pAA=GPIO.PWM(self.enAA,100)
        self.pBB=GPIO.PWM(self.enBB,100)
        self.pA.start(50) #30
        self.pB.start(50)
        self.pAA.start(50) #30
        self.pBB.start(50)

    def go_straight(self, required_rotations):
        #global tick_count_left
        #global tick_count_right
        num_rotations = 0
        self.tick_count_left = 0
        self.tick_count_right = 0
        while True:
            #print(str(self.tick_count_right) + ':' + str(num_rotations))
            if (self.tick_count_right >= 180):
            # Calculate the delta for ticks since last read
                num_rotations += 1
                self.tick_count_left = 0
                self.tick_count_right = 0
                if (num_rotations >= required_rotations):
                    return

    def start_motor(self):
        print('in start motor')
        GPIO.output(self.A1,GPIO.HIGH)
        GPIO.output(self.B1,GPIO.HIGH)

    def stop_motor(self):
        print('in stop motor')
        GPIO.output(self.A1,GPIO.LOW)
        GPIO.output(self.B1,GPIO.LOW)

    def initialize_motor(self):
        self.gpio_setup(0,0,0,0)
    
    def gpio_setup(self, a1, a2, b1, b2):
        GPIO.output(self.A1, a1)
        GPIO.output(self.A2, a2)
        GPIO.output(self.B2, b2) 
        time.sleep(0.001)

    def LEFT_TURN(self, deg):
        #global tick_count_left
        #global tick_count_right
        self.tick_count_left = 0
        self.tick_count_right = 0
        self.pA.ChangeDutyCycle(15)
        self.pB.ChangeDutyCycle(15)
        self.pAA.ChangeDutyCycle(15)
        self.pBB.ChangeDutyCycle(15)
        full_circle = 180.0
        degree = full_circle/360*deg
    
        while self.tick_count_left <= degree:
            #print(str(self.tick_count_left) + "  /  " + str(degree))
            self.gpio_setup(1, 0, 0, 0) #A stop, B foward
        self.tick_count_left = 0
        self.tick_count_right = 0
        time.sleep(1)
        self.pA.ChangeDutyCycle(30)
        self.pB.ChangeDutyCycle(30)
        self.pAA.ChangeDutyCycle(30)
        self.pBB.ChangeDutyCycle(30)
        self.gpio_setup(1, 0, 1, 0)
        
    def RIGHT_TURN(self, deg):
        #global tick_count_left
        #global tick_count_right
        
        self.pA.ChangeDutyCycle(100)
        self.pB.ChangeDutyCycle(15)
        self.pAA.ChangeDutyCycle(100)
        self.pBB.ChangeDutyCycle(15)#10(45deg) 20()
        GPIO.output(self.A1,GPIO.HIGH)
        GPIO.output(self.B2,GPIO.HIGH)
        GPIO.output(self.B1,GPIO.LOW)

        full_circle = 200.0 #160 (good)#180
        degree = full_circle/360*deg
        self.tick_count_left = 0
        self.tick_count_right = 0

        time.sleep(1) #1
        while self.tick_count_right <= degree:
            continue
            #print(str(self.tick_count_right) + "  /  " + str(degree))
            #self.gpio_setup(0, 0, 1, 0) #A forward, B stop
        self.tick_count_left = 0
        self.tick_count_right = 0
        time.sleep(1) #1
        self.pA.ChangeDutyCycle(50)#30
        self.pB.ChangeDutyCycle(50)
        self.pAA.ChangeDutyCycle(50)#30
        self.pBB.ChangeDutyCycle(50)
        #self.gpio_setup(1, 0, 1, 0)
        GPIO.output(self.B1,GPIO.HIGH)
        GPIO.output(self.B2,GPIO.LOW)

    def shutdown(self):
        self.initialize_motor()
        GPIO.cleanup() #check on this -- should be in main program

'''
time.sleep(10)
d= {'a1': '24', 'a2': '23', 'b1': '22', 'b2': '27', 'ena': '25', 'enaa': '6', 'enb': '17', 'enbb': '19', 'ticka': '26', 'tickb': '13'}
m = GearMotor(d)

print('sta')
m.start_motor()

#m.go_straight(3)
print('sto')
m.stop_motor()

print('sta')
m.start_motor()
print('str')

m.go_straight(.1)
print('sto')
m.stop_motor()
print('sta')

print('sta')
m.start_motor()

#m.go_straight(3)
print('sto')
m.stop_motor()

m.start_motor()
print('rt')
m.RIGHT_TURN(90)
m.RIGHT_TURN(90)

m.stop_motor()

m.shutdown()
'''
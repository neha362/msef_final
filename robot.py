import configparser
from gear_motor import GearMotor
from servo import Servo
from camera import Camera
import time
from datetime import datetime

'''
Robot class handles the following
1. read hardware config such as motor GPIOs, MPU pins etc
2. read the farm coordinates and whether the run is for testing fertility or moisture
3. generate a route map ie., the robot's path
4. save results of the robot's field testing
'''

class Robot:
    ROBOT_HARDWARE = '/home/pi/Desktop/pgms/msef/robot_hardware.ini'
    FARM_CONFIG = '/home/pi/Desktop/pgms/msef/farm.ini'
    gear_motor_config = {}
    servo_motor_config = {}
    farm_info = {}
    wheel_config = {}
    
    
    def __init__(self):
        print('Initializing Robot')
        self.read_config()
        self.robot_path = self.plan_robot_path()
        self.gear_motor = GearMotor(self.gear_motor_config)
        self.servo = Servo(self.servo_motor_config)
        now = datetime.now()
        self.current_time = now.strftime("%H%M")
        self.test_mode = self.farm_info['test_mode']
        
        print(self.gear_motor_config)

    def read_config(self):
        print('Reading all config')
        config = configparser.ConfigParser()
        config.read('robot_hardware.ini')
        for key in config.options('gear_motors'):
            self.gear_motor_config[key] = config['gear_motors'][key]
        print(self.gear_motor_config)
        for key in config.options('servo_motors'):
            self.servo_motor_config[key] = config['servo_motors'][key]
        print(self.servo_motor_config)
        for key in config.options('wheel'):
            self.wheel_config[key] = config['wheel'][key]
        print(self.wheel_config)
        
        config.read('farm.ini')
        for key in config.options('farm'):
            self.farm_info[key] = config['farm'][key]
        print(self.farm_info)

    def test_and_record(self, coordinates):
        print('Testing at coordinates: '+ coordinates)
        self.servo.spray_water()
        self.servo.rotate(0,0)
        time.sleep(1)
        self.servo.move_arm(0, 30, 0, 30, 1)
        self.camera = Camera(self.current_time, self.test_mode)
        self.camera.get_reading(coordinates)
        self.servo.move_arm(30, 0, 30, 0, -1)
        time.sleep(1)
        self.servo.rotate(0,0)


    def run(self):
        print("Robot's field trip : begin")
        
        self.servo.start()
        for op_mode in self.robot_path:
            self.gear_motor.start_motor()
            if (op_mode['angle'] == 0):
                if (op_mode['rotations'] == 0):
                    #test and take picture of tester
                    print('Robot testing')
                    self.gear_motor.stop_motor()
                    self.test_and_record(op_mode['position'])
                    time.sleep(3)
                else:
                    #Go Straight with n rotations
                    print('Robot going straight')
                    self.gear_motor.go_straight(op_mode['rotations'])
                    self.gear_motor.stop_motor()
            else:
                if(op_mode['angle'] == 1):
                    #Turn right
                    print('Robot turning right')      
                    self.gear_motor.RIGHT_TURN(90)
                    self.gear_motor.RIGHT_TURN(90)
                    self.gear_motor.stop_motor()
                else:
                    #Turn left
                    print('Robot turning left')
                    self.gear_motor.LEFT_TURN(90)
                    self.gear_motor.stop_motor()
            
        print("Robot's field trip : end")     

    def plan_robot_path(self):        
        print("Ground coverage is {0}m X {1}m".format(self.farm_info['length'], self.farm_info['breadth'] ))
        print("Robot's starting position is bottom left")
        print('Generating Robot test positions for Robot')
        length = float(self.farm_info['length'])
        breadth = float(self.farm_info['breadth'])
        diameter_cm = int(self.wheel_config['diameter_cm'])
        test_mode = self.farm_info['test_mode']
        test_interval_m = int(self.farm_info['test_interval_m'])
        PI = 3.14
        TEST = 0
        STRAIGHT = 0
        RIGHT_TURN = 1
        LEFT_TURN = 2
        rotations_per_m = 1000/(PI * diameter_cm)
        path_matrix = [{'rotations': 0, 'angle': TEST, 'position': '0_0' },
                       {'rotations': length/rotations_per_m, 'angle': STRAIGHT, 'position': ''},
                       {'rotations': 0, 'angle': TEST, 'position': '0_{}'.format(length) },
                       {'rotations': 0, 'angle': RIGHT_TURN, 'position': ''},
                       {'rotations': breadth/rotations_per_m, 'angle': STRAIGHT},
                       {'rotations': 0, 'angle': TEST, 'position': '{}_{}'.format(breadth, length) },
                       {'rotations': 0, 'angle': RIGHT_TURN, 'position': ''},
                       {'rotations': length/rotations_per_m, 'angle': STRAIGHT},
                       {'rotations': 0, 'angle': TEST, 'position': '{}_0'.format(breadth) },
                       {'rotations': 0, 'angle': RIGHT_TURN, 'position': ''},
                       {'rotations': breadth/rotations_per_m, 'angle': STRAIGHT}]
        return path_matrix


    def shutdown(self):
        print('Shutdown robot')
        self.gear_motor.shutdown()




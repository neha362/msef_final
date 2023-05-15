'''
This is the main program for the robot
'''
import time
from robot import Robot

'''
Initialize the robot and run 
'''
def main():
    try:
        #time.sleep(60)
        farm_robot = Robot()
        farm_robot.run()
        #pass
    except Exception:
        print('Error completing mission')
        farm_robot.shutdown()
    finally:
        farm_robot.shutdown()
        exit(1)

if __name__ == '__main__':
    #time.sleep(30)
    main()

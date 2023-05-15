import os
from datetime import date, datetime
import time

class Camera:
    def __init__(self, current_time, test_mode):
        self.current_time = current_time
        self.test_mode = test_mode
        
    def get_reading(self, coordinates):
        today = date.today()
        parent_dir = '/home/pi/Desktop/reports'
        path = os.path.join(parent_dir, str(today))
        print(path)
        try:
            os.mkdir(path)
        except OSError as error:
            print('Directory {} exists '.format(path))   
        file_name = path + '/{0}-{1}-image_{2}.jpg'.format(self.current_time, self.test_mode, coordinates)
        print(file_name)
        #command = "libcamera-still -o {}".format(file_name) #command to be executed
        command = "libcamera-jpeg -n --flush --width 300 --height 300 -o {}".format(file_name) #command to be executed
        print(command)
        res = os.system(command)
        time.sleep(.5)
        print('Report saved successfully at {}'.format(file_name))

'''
coordinates = '0_0'
camera = Camera('0910','M')
camera.get_reading('img_{}'.format(coordinates))
'''

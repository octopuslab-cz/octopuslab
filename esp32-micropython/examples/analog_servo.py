# octopusLAB simple example

from time import sleep
from components.analog import Analog
# from utils.octopus_lib import map
from components.servo import Servo

an2 = Analog(35)
s1 = Servo(16)

s1.set_degree(0)

# 0-150
amin = 0
amax = 150

while True:
    data =  an2.get_adc_aver(2)
    sleep(0.05)
    angle = map(data, 0, 4000, amin, amax)
    print(data,angle)
    s1.set_degree(angle)


"""Module providing a function FactpryController"""
from iotdemo import FactoryController

ctrl = FactoryController('/dev/ttyACM0')
while True:
    user_input = int(input('input : '))
    if user_input == 1:
        ctrl.system_start()
    elif user_input == 2:
        ctrl.system_stop()
    elif user_input == 3:
        ctrl.red = ctrl.red
    elif user_input == 4:
        ctrl.orange = ctrl.orange
    elif user_input == 5:
        ctrl.green = ctrl.green
    elif user_input == 6:
        ctrl.conveyor = ctrl.conveyor
    elif user_input == 7:
        ctrl.push_actuator(1)
    elif user_input == 8:
        ctrl.push_actuator(2)
ctrl.close()
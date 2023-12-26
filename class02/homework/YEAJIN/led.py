"""This comment is for correcting, missing-module-docstring / C0114 warning."""
from iotdemo import FactoryController

ctrl = FactoryController('/dev/ttyACM0')


while True:
    BtnInput = input('enter input : ')


    if BtnInput == '1':
        ctrl.system_start()

    elif BtnInput == '2':
        ctrl.system_stop()

    elif BtnInput == '3':
        ctrl.red = ctrl.red

    elif BtnInput == '4':
        ctrl.orange = ctrl.orange

    elif BtnInput == '5':
        ctrl.green = ctrl.green

    elif BtnInput == '6':
        ctrl.conveyor = ctrl.conveyor

    elif BtnInput == '7':
        ctrl.push_actuator(1)

    elif BtnInput == '9':
        ctrl.push_actuator(2)

    elif BtnInput == '0':
        break  

ctrl.close()

from iotdemo import FactoryController

ctrl = FactoryController('/dev/ttyACM0')

while True:
    inputing = input('enter input : ')

    if inputing == '0':
        ctrl.system_start()

    elif inputing == '1':
        ctrl.system_stop()

    elif inputing == '2':
        ctrl.red = ctrl.red

    elif inputing == '3':
        ctrl.orange = ctrl.orange

    elif inputing == '4':
        ctrl.green = ctrl.green

    elif inputing == '6':
        ctrl.push_actuator(1)

    elif inputing == '7':
        ctrl.push_actuator(2)

    elif inputing == '9':
        ctrl.conveyor = ctrl.conveyor
ctrl.close()

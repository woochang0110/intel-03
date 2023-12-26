
from iotdemo import FactoryController
	
ctrl = FactoryController('/dev/ttyACM0')

while True:
    
    API_num = "Enter number(1~8) : "
    input_num = input(API_num)

    if input_num == '1':
        ctrl.system_start()
        print("> start system")

    elif input_num == '2':
        ctrl.system_stop()
        print("> stop system")

    elif input_num == '3':
        ctrl.red = ctrl.red
        print("> red on/off")

    elif input_num == '4':
        ctrl.orange = ctrl.orange
        print("> orange on/off")

    elif input_num == '5':
        ctrl.green = ctrl.green
        print("> green on/off")

    elif input_num == '6':
        ctrl.conveyor = ctrl.conveyor
        print("> conveyor on/off")

    elif input_num == '7':
        ctrl.push_actuator(1)
        print("> actuator 1 on")

    elif input_num == '8':
        ctrl.push_actuator(2)
        print("> actuator 2 on")

    elif input_num.lower() in ('q'):
    	print("> exit")
    break

ctrl.close()

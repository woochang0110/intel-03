from iotdemo import FactoryController



ctrl = FactoryController('/dev/ttyACM0')

while True:
    user_input = input('enter input : ')

    if user_input == '1':
        ctrl.system_start()
        print("system start : red on green off")

    elif user_input == '2':
        ctrl.system_stop()
        print("system stop : red off green on")

    elif user_input == '3':
        ctrl.red = ctrl.red
        print("red on/off")

    elif user_input == '4':
        ctrl.orange = ctrl.orange
        print("orange on/off")

    elif user_input == '5':
        ctrl.green = ctrl.green
        print("green on/off")

    elif user_input == '6':
        ctrl.conveyor = ctrl.conveyor
        print("conveyor")

    elif user_input == '7':
        ctrl.push_actuator(1)
        print("act1")

    elif user_input == '8':
        ctrl.push_actuator(2)
        print("act2")

    elif user_input.lower() in ('q', '0'):
        break  # 'q' 혹은 '0'을 입력 할 경우 반복문을 빠져나온다
    else:
    	print("Please press 1 to 8 or the q button")

ctrl.close()

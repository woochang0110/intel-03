from iotdemo import FactoryController
ctrl = FactoryController('/dev/ttyACM0')

while True:
    user_input = input('enter input : ')

    if user_input == '1':
        ctrl.system_start()
        print("start!!")

    elif user_input == '2':
        ctrl.system_stop()
        print("stop!!")

    elif user_input == '3':
        ctrl.red = ctrl.red
        print("red")

    elif user_input == '4':
        ctrl.orange = ctrl.orange
        print("orange")

    elif user_input == '5':
        ctrl.green = ctrl.green
        print("green")

    elif user_input == '6':
        ctrl.conveyor = ctrl.conveyor
        print("conveyor")

    elif user_input == '7':
        ctrl.push_actuator(1)
        print("actu1")

    elif user_input == '8':
        ctrl.push_actuator(2)
        print("actu2")

    elif user_input.lower() in ('q', 'quit', 'exit'):
        break  # 입력이 'q', 'quit', 'exit'일 경우 반복문 탈출

ctrl.close()
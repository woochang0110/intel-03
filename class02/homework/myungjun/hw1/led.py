from iotdemo import FactoryController


def simulate_factory() -> None:
    """ Smart factory simulation control function """
    # Initialize FactoryController object
    ctrl = FactoryController('/dev/ttyACM0')

    while True:
        # Accept user input (numbers 1 ~ 8)
        menu = "Enter a digit between 1 ~ 8.\n \
            1 to start the system.\n \
            2 to stop the system.\n"
        entry = input(menu)

        # Call corresponding method
        if entry == '1':
            ctrl.system_start()
        elif entry == '2':
            ctrl.system_stop()
            ctrl.close()
            break
        elif entry == '3':
            if ctrl.red:
                ctrl.red = ctrl.DEV_OFF
            else:
                ctrl.red = ctrl.DEV_ON
        elif entry == '4':
            if ctrl.orange:
                ctrl.orange = ctrl.DEV_OFF
            else:
                ctrl.orange = ctrl.DEV_ON
        elif entry == '5':
            if ctrl.green:
                ctrl.green = ctrl.DEV_OFF
            else:
                ctrl.green = ctrl.DEV_ON
        elif entry == '6':
            if ctrl.conveyor:
                ctrl.conveyor = ctrl.DEV_OFF
            else:
                ctrl.conveyor = ctrl.DEV_ON
        elif entry == '7':
            ctrl.push_actuator(1)
        elif entry == '8':
            ctrl.push_actuator(2)


if __name__ == "__main__":
    simulate_factory()

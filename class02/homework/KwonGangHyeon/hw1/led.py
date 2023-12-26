"""
이 파일은 12월 21일 홈워크 제출을 위해 생성된 파일입니다.
"""
from iotdemo.factory_controller import FactoryController


def control_arduino():
    """
    desc: 이 함수를 통해 쉘 커맨드라인 숫자 입력으로 led를 제어합니다.
    """
    ctrl = FactoryController('/dev/ttyACM0')

    try:
        while True:
            input_cmd = int(input('숫자입력 : '))

            if input_cmd == 1:
                ctrl.system_start()
            elif input_cmd == 2:
                ctrl.system_stop()
            elif input_cmd == 3:
                ctrl.red = ctrl.red
            elif input_cmd == 4:
                ctrl.orange = ctrl.orange
            elif input_cmd == 5:
                ctrl.green = ctrl.green
            elif input_cmd == 6:
                ctrl.conveyor = ctrl.conveyor
            elif input_cmd == 7:
                ctrl.push_actuator(1)
            elif input_cmd == 8:
                ctrl.push_actuator(2)
            else:
                pass

    except KeyboardInterrupt:
        print('\n키보드 인터럽트 발생')

    finally:
        ctrl.close()


if __name__ == "__main__":
    control_arduino()

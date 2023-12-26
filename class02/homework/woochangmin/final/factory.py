#!/usr/bin/env python3

# system library
import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

# open source library
import cv2
import numpy as np
import openvino as ov

# user made library
from iotdemo import ColorDetector, FactoryController, MotionDetector

FORCE_STOP = False


def thread_cam1(q):
    """
    병뚜껑에 대해 detecting 을 하고 detected가 된 정보를 가지고 inferencing 하여
    actuator를 동작시킨다.
    """
    # MotionDetector
    det = MotionDetector()
    det.load_preset('./resources/motion.cfg', 'default')

    # Load and initialize OpenVINO
    core = ov.Core()
    model = core.read_model(model='./resources/openvino.xml')

    # HW2 Open video clip resources/conveyor.mp4 instead of camera device.
    cap = cv2.VideoCapture('resources/conveyor.mp4')

    start_flag = True
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break
        """
            https://docs.openvino.ai/2023.2/
            openvino_inference_engine_ie_bridges_python_sample_hello_classification_README.html
        """
        # HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(("VIDEO:Cam1 live", frame))

        # Motion detect
        detected = det.detect(frame)
        if detected is None:
            continue

        # Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO:Cam1 detected", detected))

        # Inference OpenVINO
        if start_flag:
            input_tensor = np.expand_dims(detected, 0)
            ppp = ov.preprocess.PrePostProcessor(model)

            ppp.input().tensor() \
                .set_shape(input_tensor.shape) \
                .set_element_type(ov.Type.u8) \
                .set_layout(ov.Layout('NHWC'))  # noqa: ECE001, N400
            ppp.input().preprocess() \
                .resize(ov.preprocess.ResizeAlgorithm.RESIZE_LINEAR)
            ppp.input().model().set_layout(ov.Layout('NCHW'))
            ppp.output().tensor().set_element_type(ov.Type.f32)
            model = ppp.build()
            compiled_model = core.compile_model(model=model, device_name="CPU")
            start_flag = False

        results = compiled_model.infer_new_request({0: input_tensor})
        predictions = next(iter(results.values()))
        probs = predictions.reshape(-1)

        # Calculate ratios
        probs *= 100
        print(f'nok: {probs[0]:.2f}, ok: {probs[1]:.2f}')

        # in queue for moving the actuator 1
        if probs[0] > 95:
            q.put(("PUSH", 1))

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    """
    desc: 병뚜껑의 움직임을 인식하여 영상 1장을 캡쳐하고,
            해당 영상에 대해 흰색/파란색을 판별하는 영상처리 알고리즘을 돌리고,
            각종 정보를 Queue에 저장합니다.
    """
    # MotionDetector
    det = MotionDetector()
    det.load_preset('./resources/motion.cfg', 'default')

    # ColorDetector
    color = ColorDetector()
    color.load_preset('./resources/color.cfg', 'default')

    # HW2 Open "resources/conveyor.mp4" video clip
    cap = cv2.VideoCapture('resources/conveyor.mp4')

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(("VIDEO:Cam2 live", frame))

        # Detect motion
        detected = det.detect(frame)
        if detected is None:
            continue

        # Enqueue "VIDEO:Cam2 detected", detected info.
        q.put(("VIDEO:Cam2 detected", detected))

        # Detect color
        predict = color.detect(detected)

        # Compute ratio
        name, ratio = predict[0]
        ratio *= 100
        print(f"{name}: {ratio:.2f}%")

        # Enqueue to handle actuator 2
        if name == 'blue' and int(ratio) > 50:
            q.put(("PUSH", 2))

    cap.release()
    q.put(('DONE', None))
    exit()


def imshow(title, frame, pos=None):
    """opencv를 통해 영상 프레임을 GUI창에 show합니다"""
    cv2.namedWindow(title)
    if pos:
        cv2.moveWindow(title, pos[0], pos[1])
    cv2.imshow(title, frame)


def main():
    """
    desc: thread1, thread2가 Queue에 저장한 정보를 바탕으로,
            메인 스레드의 동작을 실행합니다.
    """
    global FORCE_STOP

    parser = ArgumentParser(prog='python3 factory.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    # HW2 Create a Queue
    q = Queue()

    # HW2 Create thread_cam1 and thread_cam2 threads and start them.
    thread1 = threading.Thread(target=thread_cam1, args=(q,), daemon=True)
    thread2 = threading.Thread(target=thread_cam2, args=(q,), daemon=True)

    thread1.start()
    thread2.start()

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                FORCE_STOP = True
                break

            # HW2 get an item from the queue.
            # You might need to properly handle exceptions.
            # de-queue name and data
            try:
                (name, data) = q.get_nowait()
            except Empty:
                continue

            # HW2 show videos with titles of
            # 'Cam1 live' and 'Cam2 live' respectively.
            if name[:6] == 'VIDEO:':
                imshow(name[6:], data)
            elif name == 'PUSH':  # Control actuator, name == 'PUSH'
                ctrl.push_actuator(data)
            elif name == 'DONE':
                FORCE_STOP = True

            q.task_done()

    thread1.join()
    thread2.join()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()

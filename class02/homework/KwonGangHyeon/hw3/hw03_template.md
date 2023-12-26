# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```bash
(.otx) kengwon@ken:~/workspace/otx-bottlecap/classification-via-EfficientNet-V2-S$ ds_count ./splitted_dataset 2
./splitted_dataset:	400
./splitted_dataset/train:	320
./splitted_dataset/train/nok:	152
./splitted_dataset/train/ok:	168
./splitted_dataset/val:	80
./splitted_dataset/val/nok:	37
./splitted_dataset/val/ok:	43
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other hyper-prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0|49.48|0:01:36.125414|64|0.0071| |
|EfficientNet-B0|1.0|139.59|0:00:26.104382|64|0.0049| |
|DeiT-Tiny|1.0|52.59|0:00:21.839591|64|0.0001| | 
|MobileNet-V3-large-1x|1.0 |209.96|0:00:12.601386|64|0.0058| |


## FPS 측정 방법
- 실습 폴더 상태
- test_data.jpg는 불량품 이미지(class1: NOK)
```bash
(.otx) kengwon@ken:~/workspace/otx-bottlecap$ tree -L 1
.
├── classification-via-DeiT-Tiny
├── classification-via-EfficientNet-B0
├── classification-via-EfficientNet-V2-S
├── classification-via-MobileNet-V3-large-1x
├── hello_classification.py
└── test_data.jpg
```

- hello_classification.py 파일 내부를 수정
```python
...
"""@kenGwon add"""
import time 

def main():
    ...
    # Step 1. Initialize OpenVINO Runtime Core 
    ...
    # Step 2. Read a model 
    ...
    # Step 3. Set up input
    ...
    # Step 4. Apply preprocessing
    ...
    # Step 5. Loading model to the device
    ...
    # Step 6. Create infer request and do inference synchronously
    """@kenGwon add"""
    inference_start_time = time.time()
    ...
    # Step 7. Process output
    ...
    """@kenGwon add"""
    inference_time = time.time() - inference_start_time
    fps = 1 / inference_time # 단 한장의 사진에 대해서 inference 돌린 것으로 FPS 뽑기
    log.info(f'FPS: {fps:.2f}')
    ...
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
```
- (결과) MobileNet-V3-large-1x 모델에 대한 FPS 계산 출력 예시 ... 
```bash
(.otx) kengwon@ken:~/workspace/otx-bottlecap$ python ./hello_classification.py classification-via-MobileNet-V3-large-1x/outputs/20231223_143625_export/openvino/openvino.xml ./test_data.jpg "CPU"
[ INFO ] Creating OpenVINO Runtime Core
[ INFO ] Reading the model: classification-via-MobileNet-V3-large-1x/outputs/20231223_143625_export/openvino/openvino.xml
[ INFO ] Loading the model to the plugin
[ INFO ] Starting inference in synchronous mode
[ INFO ] Image path: ./test_data.jpg
[ INFO ] Top 10 results: 
[ INFO ] class_id probability
[ INFO ] --------------------
[ INFO ] 0        2.6192770
[ INFO ] 1        -3.0767803
[ INFO ] 
[ INFO ] FPS: 201.30
[ INFO ] This sample is an API example, for any performance measurements please use the dedicated benchmark_app tool
```

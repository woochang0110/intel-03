# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset/: 100
./splitted_dataset/train: 80
./splitted_dataset/train/nok: 40
./splitted_dataset/train/ok: 40
./splitted_dataset/val: 20
./splitted_dataset/val/nok: 10
./splitted_dataset/val/ok: 10
```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other hyper-prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0|4583.94|0:01:16.723391|64|0.0071| |
|EfficientNet-B0|1.0|4410.41|0:00:18.208778|64|0.0049| |
|DeiT-Tiny|1.0|4804.47|0:00:15.872581|64|0.0001| |
|MobileNet-V3-large-1x|1.0|5412.01|0:00:09.836774|64|0.0058| |


## FPS 측정 방법
import time

# ADD Step 6
inference_start_time = time.time()

# ADD Step 7
inference_time = time.time() - inference_start_time
fps = 1 / inference_time
log.info(f'FPS : {fps:.2f}')

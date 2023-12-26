# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
./splitted_dataset/:	125
./splitted_dataset/val:	25
./splitted_dataset/val/nok:	11
./splitted_dataset/val/ok:	14
./splitted_dataset/train:	100
./splitted_dataset/train/nok:	48
./splitted_dataset/train/ok:	52

```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other hyper-prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0|65.09|0:01:20.822735|64|0.0071||
|EfficientNet-B0|1.0|201.64|0:00:09.233415|64|0.0058||
|DeiT-Tiny|1.0|47.03|0:00:16.711883|64|0.0001||
|MobileNet-V3-large-1x|1.0|200.97|0:00:09.073849|64|0.0058|


## FPS 측정 방법
hello_classification.py 파일의 코드를 수정하여 출력하도록 함

Step 6  \
inference_start_time = time.time() 

Step 7  \
inference_time = time.time() - inference_start_time \
fps = 1 / inference_time \
log.info(f'FPS : {fps:.2f}')

```예) DeiT-Tiny 모델을 사용하여 hello_classification.py를 실행한 결과```
![Alt text](image.png)
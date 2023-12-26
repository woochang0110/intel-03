# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset/: 108
./splitted_dataset/train: 86
./splitted_dataset/train/<OK>: 44​
./splitted_dataset/train/<NOT_OK>: 42​
./splitted_dataset/val: 22
./splitted_dataset/train/<OK>: 10​
./splitted_dataset/train/<NOT_OK>: 12
```

## Training 결과
|Classification model	|Accuracy	|FPS(GPU / CPU)	|Training time	|Batch size	|Learning rate	|Other hyper-prams	|
|-----------------------|-----------|---------------|---------------|-----------|---------------|-------------------|
|	EfficientNet-V2-S	|	1.0		|	30	/  50	|0:01:18.817406	|	64		|	0.00355		|		----		|
|	EfficientNet-B0 	|	1.0		|	X	/  150	|0:00:18.494986	|	64		|	0.00245		|		----		|
|		DeiT-Tiny		|	1.0		|	X	/  52	|0:00:16.258080	|	64		|	5e-05		|		----		|
|MobileNet-V3-large-1x	|	1.0		|	200 /  215	|0:00:13.059633	|	64		|	2.900e-03	|		----		|


## FPS 측정 방법
Inference 할 때의 FPS를 측정
Inference 는 hello_classification.py 파일로 진행
Inference 할 Device 는 GPU
CPU 또는 GPU 에 모델이 이미 Load 되었다고 가정 (미리 warm up이 되어있다.)

FPS 측정은 step.7 에 해당하는 Process output 부분에 대해서 측정한다.

```
# FPS 측정을 위한 초기화
fps_start_time = time.time()

# 반복문을 통해 100번 반복 후 fps 측정
for count in range(101):
	# FPS 계산
	fps_end_time = time.time()
	fps = 1 / (fps_end_time - fps_start_time)
	
fps = fps / count
```

이미지를 100번 로드하고 Inference 한다.

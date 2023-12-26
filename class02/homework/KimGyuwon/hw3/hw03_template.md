# Homework03
Smart factory 불량 분류모델 training 결과

## Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 2
./splitted_dataset:	69
./splitted_dataset/train:	55
./splitted_dataset/train/o:	32
./splitted_dataset/train/x:	23
./splitted_dataset/val:	14
./splitted_dataset/val/o:	8
./splitted_dataset/val/x:	6

```

## Training 결과
|Classification model|Accuracy|FPS|Training time|Batch size|Learning rate|Other hyper-prams|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|1.0000 |60.85 |0:01:21.425371|32|0.01
|EfficientNet-B0|1.0000|171.82|0:00:36.248356|32|0.01
|DeiT-Tiny|1.0000|46.90|0:00:09.273216|32|0.01
|MobileNet-V3-large-1x|1.0000|224.64|0:00:13.062987|32|0.01



## FPS 측정 방법
```
 --------------------------- Step 6. Create infer request and do inference synchronously -----------------------------
    log.info('Starting inference in synchronous mode')
    prev_time = time.time()
    results = compiled_model.infer_new_request({0: input_tensor})
    
 --------------------------- Step 7. Process output ------------------------------------------------------------------
    predictions = next(iter(results.values()))

    sec = time.time() - prev_time
    fps = 1/(sec)
    log.info(f"FPS: {fps:.2f}")

```
# using rknn_model_zoo example

https://github.com/airockchip/rknn_model_zoo/blob/main/examples/yolo11/python/convert.py

## download proper model (other models do not work with this examples)

https://ftrg.zbox.filez.com/v2/delivery/data/95f00b0fc900458ba134f8b180b3f7a1/examples/yolo11/yolo11n.onnx

## run following commands from `rknn_model_zoo/examples/yolo11/python`

```
python convert.py /home/orangepi/sambashare/YoloTest/yolo11n.onnx rk3566 i8 /home/orangepi/sambashare/YoloTest/yolo11n.rknn
```

## test 
```
python yolo11.py --model_path /home/orangepi/sambashare/YoloTest/yolo11n.rknn --target rk3566 --img_show
```

# Troubleshooting

sudo apt-get install libgl1

## fix for "Invalid RKNN model version 6"
replace/add librknnrt.so in /usr/lib (or /usr/lib64) with version from this directory (taken from https://github.com/airockchip/rknn-toolkit2/blob/master/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so)



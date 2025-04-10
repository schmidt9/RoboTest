from ultralytics import YOLO

# Load the exported RKNN model
rknn_model = YOLO("yolo11n_rknn_model/yolo11n-rk3566.rknn", task='detect')

# Run inference
results = rknn_model("https://ultralytics.com/images/bus.jpg")

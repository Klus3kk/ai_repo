from ultralytics import YOLO

model = YOLO("yolo11x.pt")

train_results = model.train(
    data="coco8.yaml",
    epochs=100,
    imgsz=640,
    device="cpu",
)

# Evaluate model performance on the validation set
metrics = model.val()

results = model("ladybug.jpg")
results[0].show()

path = model.export(format="onnx") 
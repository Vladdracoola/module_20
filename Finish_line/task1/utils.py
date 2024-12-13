import onnxruntime as ort
import numpy as np
import cv2
from .models import ImageFeed, DetectedObject
from django.core.files.base import ContentFile

YOLO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'TV', 'laptop',
    'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
    'hair drier', 'toothbrush'
]


def process_image(image_feed_id):
    try:
        image_feed = ImageFeed.objects.get(id=image_feed_id)
        image_path = image_feed.image.path

        model_path = 'task1/yolov5s-seg.onnx'
        session = ort.InferenceSession(model_path)

        img = cv2.imread(image_path)
        if img is None:
            print("Failed to load image")
            return False

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (640, 640), swapRB=True, crop=False)

        detections = session.run(None, {"images": blob})[0]

        for detection in detections:
            confidence = float(detection[4][0])
            if confidence > 0.6:
                scores = detection[5:]
                class_id = np.argmax(scores)


                if class_id < len(YOLO_CLASSES):
                    class_label = YOLO_CLASSES[class_id]
                    confidence = scores[class_id]


                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")
                    startX, startY = int(centerX - width / 2), int(centerY - height / 2)
                    endX, endY = int(centerX + width / 2), int(centerY + height / 2)


                    cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    label = f"{class_label}: {confidence:.2f}"
                    cv2.putText(img, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


                    DetectedObject.objects.create(
                        image_feed=image_feed,
                        object_type=class_label,
                        location=f"{startX},{startY},{endX},{endY}",
                        confidence=confidence
                    )
                else:
                    print(f"Class ID {class_id} is out of range for the available classes.")

        result, encoded_img = cv2.imencode('.jpg', img)
        if result:
            content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
            image_feed.processed_image.save(content.name, content, save=True)

        return True

    except ImageFeed.DoesNotExist:
        print("ImageFeed not found.")
        return False

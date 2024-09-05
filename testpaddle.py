import paddle
from paddleocr import PaddleOCR

print(paddle.utils.run_check())
gpu_available = paddle.device.is_compiled_with_cuda()
print("GPU available:", gpu_available)
if gpu_available:
    place = paddle.CUDAPlace(0)  # Use the first GPU
    print("Using GPU:", place)
else:
    print("Not using GPU")

import cv2
import paddle
import time

# Initialize PaddleOCR
# ocr = paddleocr.OCR(use_gpu=True)
ocr = PaddleOCR(use_angle_cls=False, lang="ch", use_gpu=True)
# Read the image using OpenCV
image_path = 'a.png'
image = cv2.imread(image_path)

# Convert the image to RGB (PaddleOCR expects RGB images)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run PaddleOCR 10 times and measure the time taken
total_time = 0
result = None
for i in range(10):
    start_time = time.time()
    result = ocr.ocr(image_rgb, det=True,
                     rec=True,
                     cls=False)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    total_time += elapsed_time
    print(f"Run {i + 1}: {elapsed_time:.2f} ms")

# Calculate and print the average time
average_time = total_time / 10
print(f"Average time per OCR: {average_time:.2f} ms")

# Check if PaddlePaddle is using the GPU
if paddle.device.is_compiled_with_cuda():
    print("PaddlePaddle is using the GPU.")
else:
    print("PaddlePaddle is not using the GPU.")

print(result)

import time

import adbutils
import cv2
import numpy

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
for info in adb.list():
    print(info.serial, info.state)
    # <serial> <device|offline>

d = adb.device()
start = time.time()
png_bytes = d.shell("screencap -p", encoding=None)
print(f"screencap: {time.time() - start}")
image_data = numpy.frombuffer(png_bytes, dtype=numpy.uint8)
image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
print(f"imdecode: {time.time() - start}")
cv2.imwrite("images/test_adb_cap.jpg", image)

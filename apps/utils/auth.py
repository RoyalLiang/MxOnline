import cv2
import uuid
import os

from MxOnline import settings


def get_video_pic(name):
    cap = cv2.VideoCapture(name)
    cap.set(0, int(cap.get(7) / 2))  # 取它的中间帧
    rval, frame = cap.read()  # 如果rval为False表示这个视频有问题，为True则正常
    img_name = str(uuid.uuid4()) + '.jpg'
    img_url = os.path.join(settings.MEDIA_ROOT, 'video_image')
    if not os.path.isdir(img_url):
        os.mkdir(img_url)
    img_url = os.path.join(img_url, img_name)

    if rval:
        cv2.imwrite(img_url, frame)  # 存储为图像
    cap.release()
    return img_name

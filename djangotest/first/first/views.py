from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import random
# Create your views here.

def index(request):
    context={
    }
    return render(request, 'first/index.html',context)

def select(request):
    context ={}
    return render(request, 'first/select.html',context)


def result(request):
    chosen = int(request.GET['number'])

    results =[]
    if chosen >= 1 and chosen <= 45:
        results.append(chosen)

    box = []
    for i in range(0,45):
        if chosen != i+1:
            box.append(i+1)
    
    random.shuffle(box)

    while len(results) < 6:
        results.append(box.pop())

    context = {
        'numbers': results
    }
    return render(request, 'first/result.html',context)

def home(request):
    context = {}

    return render(request,'home.html',context)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

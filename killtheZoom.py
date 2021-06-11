from PIL import ImageGrab
from pytesseract import *
import re
import psutil

pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR/tesseract.exe"

userwidth,userheight = map(int,input("모니터 해상도를 입력하여주세요 : ").split())

width_left = int(userwidth / 1.2)
width_up = int(userheight / 54)
width_right = int(userwidth / 1.03783)
width_down = int(userheight / 12.7)

def readDigitFromScreen():
    img = ImageGrab.grab()
    croppedImage = img.crop((width_left, width_up, width_right, width_down))
    digit=''
    try:
        text = image_to_string(croppedImage, lang='kor')
        numlist = re.findall("\d",text)
        if not numlist:
            return 404
        else:
            for num in numlist:
                digit+=num
            return int(digit)
    except TesseractNotFoundError:
        print("you need to install Tesseract-OCR on your system")

def scanPeopleNum():
    if(readDigitFromScreen()< 15):
        killzoom()
    elif readDigitFromScreen() >=15 and readDigitFromScreen() <=50:
        print("아직 인원이 %d명입니다"%readDigitFromScreen())
    elif readDigitFromScreen() == 404:
        print("숫자를 인식할 수 없습니다")

def killzoom():
    for proc in psutil.process_iter():
        try:
            # 프로세스 이름, PID값 가져오기
            processName = proc.name()
            processID = proc.pid

            if processName == "Zoom.exe":
                parent_pid = processID  # PID
                parent = psutil.Process(parent_pid)  # PID 찾기
                for child in parent.children(recursive=True):  # 자식-부모 종료
                    child.kill()
                parent.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):  # 예외처리
            pass

while True:
    scanPeopleNum()













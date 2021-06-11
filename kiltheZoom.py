from PIL import ImageGrab
from pytesseract import *
import re
import psutil

pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR/tesseract.exe"

def readDigitFromScreen():
    img = ImageGrab.grab()
    # print(img.size)
    croppedImage = img.crop((3200, 40, 3700, 170))
    # print("잘려진 사진 크기 :", croppedImage.size)
    # croppedImage.save("croppedImage.png")

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
    if(readDigitFromScreen()< 30):
        killzoom()
        # kill_zoom_process()
    elif readDigitFromScreen() >=30 and readDigitFromScreen() <=50:
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













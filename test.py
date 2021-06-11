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

        for num in numlist:
            digit+=num
    except TesseractNotFoundError:
        print("you need to install Tesseract-OCR on your system")
    return int(digit)



def scanPeopleNum():
    if(readDigitFromScreen()< 30):
        killzoom()
    elif readDigitFromScreen() >=30:
        print("아직 인원이 %d명입니다"%readDigitFromScreen())

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
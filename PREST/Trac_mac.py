import mediapipe as mp
import cv2
import pyautogui
import subprocess
import time
import os
import re


class Trac():
    def __init__(self):
        self.static_image_mode = False
        self.max_hands = 1
        self.model_complexity = 1
        self.detection_confidence = 0.5
        self.track_confidence = 0.5

        self.mp = mp.solutions.hands
        self.handtrac_library = self.mp.Hands(self.static_image_mode, self.max_hands, self.model_complexity,
                                                    self.detection_confidence, self.track_confidence)
        self.drawing = mp.solutions.drawing_utils

    def tracking(self,draw, img, drawing_img):
        landmark = []

        landmarks = self.handtrac_library.process(img)
        if landmarks.multi_hand_landmarks:
            for all_landmark in landmarks.multi_hand_landmarks:
                if draw:
                    self.drawing.draw_landmarks(drawing_img, all_landmark, self.mp.HAND_CONNECTIONS)
                for id, lm in enumerate(all_landmark.landmark):
                    hight, width, channel = img.shape
                    x, y = int(lm.x * width), int(lm.y * hight)
                    landmark.append([id, x, y])

        return landmark


def notify(title, text):
    os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title))


def first():
    global first_time

    return first_time


def reset():
    os.remove('settings.prt')


def setting_read():
    global key,setting_list,enable_cap,cap_name

    return key,setting_list,enable_cap,cap_name

def setting(show_performance, camera_number, move_key, back_key, finish_key, default_hunds):
    global settings_file_path, setting_list, key

    key = []

    new_settings = ["PREST SETTINGS FILE\n", "\n","show performance = " + str(show_performance) + "\n", "camera number = " + str(camera_number) + "\n",
                            "move key = " + str(move_key) + "\n", "back key = " + str(back_key) + "\n",
                            "finish key = " + str(finish_key) + "\n", "default hunds =" + str(default_hunds) + "\n"]

    settings_file = open(settings_file_path,"w")
    settings_file.writelines(new_settings)
    settings_file.close()

    settings_file = open(settings_file_path,"r")
    settings_file = settings_file.readlines()
    setting_list = []
    for i in range(2):
        settings_file.pop(0)
    for i in range(len(settings_file)):
        setting_list.append(re.sub(r"\D", "", settings_file[i]))

    key.append(move_key)
    key.append(back_key)
    key.append(finish_key)
    key.append(default_hunds)


def cap_set():
    global cap, setting_list, screen_width, screen_height, first_time

    cap =  cv2.VideoCapture(int(setting_list[1]))

    #mov_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #mov_height = mov_width / screen_width * screen_height
    cap.set(cv2.CAP_PROP_FPS, 30)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, mov_width)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(mov_height))


def prest(fin):
    global difference_time, draw, finger_tips, move, back, cap, trac, first_prest, status, key

    if first_prest:
        first_prest = False
        notify("開始", "プレゼンテーションを開始してください。")
        cap_set()

    roop = True
    dominant_hand = "none"
    finger_status = []

    success, img = cap.read()
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    flipRGBimg = cv2.flip(RGBimg, 1)
    flipimg = cv2.flip(img, 1)

    landmark = trac.tracking(draw[0], flipRGBimg, flipimg)

    standard_time = time.time()
    fps = 1/(standard_time-difference_time)
    difference_time = standard_time

    if len(landmark) != 0:
        if landmark[finger_tips[1]][1] < landmark[finger_tips[4]][1]:
            dominant_hand = "right"
        elif landmark[finger_tips[1]][1] > landmark[finger_tips[4]][1]:
            dominant_hand = "left"
        else :
            dominant_hand = "error"

        if dominant_hand == "right":
            if landmark[finger_tips[0]][1] < landmark[finger_tips[0] - 1][1]:
                finger_status.append(1)
            else :
                finger_status.append(0)
        elif dominant_hand == "left":
            if landmark[finger_tips[0]][1] > landmark[finger_tips[0] - 1][1]:
                finger_status.append(1)
            else :
                finger_status.append(0)
        elif dominant_hand == "error":
            pass


        for i in range(1, 5):
            if dominant_hand == "error":
                break
            elif landmark[finger_tips[i]][2] < landmark[finger_tips[i] - 2][2]:
                finger_status.append(1)
            else:
                finger_status.append(0)

        if finger_status == key[0]:
            if move == 0:
                pyautogui.press('right')
                move = 1

        elif finger_status == key[1]:
            if back == 0:
                pyautogui.press('left')
                back = 1

        else:
            move = 0
            back = 0

    elif fin:
        roop = False
        notify("終了", "プログラムが終了しました。")

        finger_status = "fin"
        dominant_hand = "fin"

        cap.release()


    status = f'fps:{int(fps)}  {dominant_hand}:{finger_status}'

    #cv2.imshow("Image", flipimg)
    cv2.waitKey(1)
    return roop, status


settings_file_path = "./settings.prt"
setting_number = [1, 0]
key = [[0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]
settings = ["PREST SETTINGS FILE\n", "\n", "show performance = " + str(setting_number[0]) + "\n", "camera number = " + str(setting_number[1]) + "\n",
                    "move key = " + str(key[0]) + "\n", "back key = " + str(key[1]) + "\n",
                    "finish key = " + str(key[2]) + "\n", "default hunds =" + str(key[3]) + "\n"]

try:
    settings_file = open(settings_file_path,"r")
    settings_file = settings_file.readlines()
    setting_list = []
    move_key = []
    back_key = []
    finish_key = []
    default_hunds = []
    key = []

    for i in range(2):
        settings_file.pop(0)
    for i in range(len(settings_file)):
        setting_list.append(re.sub(r"\D", "", settings_file[i]))

    for i in range(len(setting_list)-2):
        if i == 0:
            move__key = list(setting_list[i + 2])
            for j in range(5):
                move_key.append(int(move__key[j]))
            key.append(move_key)
        elif i == 1:
            back__key = list(setting_list[i + 2])
            for j in range(5):
                back_key.append(int(back__key[j]))
            key.append(back_key)
        elif i == 2:
            finish__key = list(setting_list[i + 2])
            for j in range(5):
                finish_key.append(int(finish__key[j]))
            key.append(finish_key)
        elif i == 3:
            default__hunds = list(setting_list[i + 2])
            for j in range(5):
                default_hunds.append(int(default__hunds[j]))
            key.append(default_hunds)

    first_time = False

except FileNotFoundError:
    settings_file = open(settings_file_path,"w")
    settings_file.writelines(settings)
    settings_file.close()
    setting_list = setting_number
    first_time = True

enable_cap = []
cap_name =[]
cap_name_all = []
cap_quantity = []

for i in range(0, 10):
    test_cap = cv2.VideoCapture(i)
    if test_cap.isOpened():
        enable_cap.append(i)
    test_cap.release()

origin_cam = subprocess.run("system_profiler SPCameraDataType",stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
origin_cam_name = origin_cam.stdout.decode("utf8").split("\n")
while True:
    try:
        origin_cam_name.remove('')
    except ValueError:
        break
for i in origin_cam_name:
   cap_name_all.append(i.replace(' ', ''))

for i in range(len(cap_name_all)):
    if cap_name_all[i].startswith("ModelID:"):
        cap_quantity.append(i)

if len(enable_cap) == len(cap_quantity):
    for i in cap_quantity:
        cap_name.append(cap_name_all[i-1])
else:
    irregular_cam = len(enable_cap) - len(cap_quantity)
    for i in range(int(irregular_cam)):
        irregular_cam_name = "カメラ:"
        cap_name.append(irregular_cam_name)
    for i in cap_quantity:
        cap_name.append(cap_name_all[i-1])

trac = Trac()

first_prest = True
cap = 0
status = 0
#screenshot = pyautogui.screenshot()
#screenshot.save('screen_size.png')
#screen_size=cv2.imread('screen_size.png')
#screen_height, screen_width, channel = screen_size.shape
#os.remove('screen_size.png')

difference_time = 0
draw = [True, False]
finger_tips = [4, 8, 12, 16, 20]
move = 0
back = 0
fin = False

if __name__ == '__main__':
    while True:
        prest(fin)
        pass
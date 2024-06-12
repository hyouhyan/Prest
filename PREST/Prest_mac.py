VER = "1.6.4"
print("Version=" + str(VER))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import japanize_kivy
import Trac_mac as prest
import re
from kivy.clock import Clock


round = 1
finger = [1, 1, 1, 1, 1]
self2 = ''
m_self = ''

reshow = False

cam_num = -1
cam_show = []

roop = True
#move_key = [0, 0, 0, 0, 0]
#back_key = [0, 0, 0, 0, 0]
finish_key = [2, 2, 2, 2, 2]
default_hands = [2, 2, 2, 2, 2]
fin = False
all_keys = []
show_performance = 1
camera_number = -1

setting_file_exist = prest.first() == False
#検出させない
#setting_file_exist = False

#読み取るプログラム
tmp_key, setting_list, tmp_cam_num, tmp_cam_name = prest.setting_read()
move_key = tmp_key[0]
back_key = tmp_key[1]
finish_key = tmp_key[2]

for i in range(len(tmp_cam_num)):
    cam_show.append(str(tmp_cam_name[i]) + str(tmp_cam_num[i]))


def setfinger(self):
    global finger

    if finger[0] == 1:
        self.ids.finger01.source = './image/hand/01.png'
    else:
        self.ids.finger01.source = './image/none.png'
    if finger[1] == 1:
        self.ids.finger02.source = './image/hand/02.png'
    else:
        self.ids.finger02.source = './image/none.png'
    if finger[2] == 1:
        self.ids.finger03.source = './image/hand/03.png'
    else:
        self.ids.finger03.source = './image/none.png'
    if finger[3] == 1:
        self.ids.finger04.source = './image/hand/04.png'
    else:
        self.ids.finger04.source = './image/none.png'
    if finger[4] == 1:
        self.ids.finger05.source = './image/hand/05.png'
    else:
        self.ids.finger05.source = './image/none.png'

def setfinger_r(self, key):
    if key[0] == 1:
        self.ids.finger_r01.source = './image/hand/01.png'
    else:
        self.ids.finger_r01.source = './image/none.png'
    if key[1] == 1:
        self.ids.finger_r02.source = './image/hand/02.png'
    else:
        self.ids.finger_r02.source = './image/none.png'
    if key[2] == 1:
        self.ids.finger_r03.source = './image/hand/03.png'
    else:
        self.ids.finger_r03.source = './image/none.png'
    if key[3] == 1:
        self.ids.finger_r04.source = './image/hand/04.png'
    else:
        self.ids.finger_r04.source = './image/none.png'
    if key[4] == 1:
        self.ids.finger_r05.source = './image/hand/05.png'
    else:
        self.ids.finger_r05.source = './image/none.png'

def setfinger_l(self, key):
    if key[0] == 1:
        self.ids.finger_l01.source = './image/hand/01.png'
    else:
        self.ids.finger_l01.source = './image/none.png'
    if key[1] == 1:
        self.ids.finger_l02.source = './image/hand/02.png'
    else:
        self.ids.finger_l02.source = './image/none.png'
    if key[2] == 1:
        self.ids.finger_l03.source = './image/hand/03.png'
    else:
        self.ids.finger_l03.source = './image/none.png'
    if key[3] == 1:
        self.ids.finger_l04.source = './image/hand/04.png'
    else:
        self.ids.finger_l04.source = './image/none.png'
    if key[4] == 1:
        self.ids.finger_l05.source = './image/hand/05.png'
    else:
        self.ids.finger_l05.source = './image/none.png'


def clearfinger(self):
    global finger
    finger = [1, 1, 1, 1, 1]

    self.ids.finger01.source = './image/none.png'
    self.ids.finger02.source = './image/none.png'
    self.ids.finger03.source = './image/none.png'
    self.ids.finger04.source = './image/none.png'
    self.ids.finger05.source = './image/none.png'

class FingerSelector(FloatLayout):
    def press(self, pos):
        global self2, m_self
        self2 = self

        if finger[pos] == 0:
            finger[pos] = 1
        else:
            finger[pos] = 0

        setfinger(m_self)

#back = 0
#next = 1
def change_scene(self, backornext):
    global round, checkboclayout, finger, self2, move_key, back_key, finish_key, roop, camera_number, show_performance, default_hands, setting_file_exist, tmp_cam_num, cam_show, reshow, all_keys, setting_list
    if backornext == 1 and round < 50:

        #nextの処理
        scene = round + 1
        self.ids.image_next.source = './image/next_gr.png'

        #この場合のみYesボタンの機能を持つ
        if round == 10:
            save_file = True

    if backornext == 0 and round < 50:
        #backの処理
        scene = round - 1
        self.ids.image_back.source = './image/back_gr.png'

        #設定ファイル→ようこそ
        if setting_file_exist and round == 6:
            scene = 2
        if setting_file_exist and round == 5:
            scene = 1

        if scene == 3:
            scene = round - 2

        #この場合のみNoボタンの機能を持つ
        if round == 10:
            save_file = False
            #この時のみnextと同じくsceneを次に進める
            scene = round + 1


    if scene == 0:
        if prest.first():
            prest.reset()
        exit()

    if scene == 1 :
        self.ids.main_label.text = "ようこそ、最先端へ"
        self.ids.main_spinner.background_color = (0, 0, 0, 0)
        self.ids.main_spinner.values = ''

    if scene == 2 :
        global m_self
        m_self = self
        #print(setting_file_exist)
        if setting_file_exist:
            self.ids.main_label.text = "設定が見つかりました、内容を表示します"
            self.ids.sub_label.text = ""
            all_keys.append(finish_key)
            all_keys.append(move_key)
            all_keys.append(back_key)
            self.ids.right_image.source = './image/none.png'
            self.ids.left_image.source = './image/none.png'
            self.ids.main_image.source ='./image/logo.png'
            setfinger_l(self, [0, 0, 0, 0, 0])
            setfinger_r(self, [0, 0, 0, 0, 0])
        elif tmp_cam_num == []:
            scene = 52
        else:
            self.ids.main_label.text = "利用するカメラを選んでください"
            self.ids.main_spinner.background_color = (0.5, 0.5, 0.5, 1)
            self.ids.main_spinner.values = cam_show
        


    if scene == 3 :
        self.ids.main_spinner.background_color = (0, 0, 0, 0)

        for i in range(len(tmp_cam_num)):
            if str(cam_show[i]) == str(self.ids.main_spinner.text):
                camera_number = tmp_cam_num[i]            

        if camera_number == -1:
            self.ids.main_label.text = f'カメラ未選択、{cam_show[0]}を使用します'
            camera_number = 0
        elif round != (scene + 1):
            scene = 4

    if scene == 4:
        self.ids.main_label.text = "次に、機能に対応するジェスチャを決めましょう"
        self.ids.main_image.source ='./image/logo.png'
        if round == scene + 1 and setting_file_exist == False:
            self.ids.sub_label.text = ""
            self.ids.main_float.remove_widget(self2)
            clearfinger(self)

        self.ids.main_spinner.values = ''
    
    if scene == 5:
        self.ids.main_label.text = "その1「進むキー」"
        self.ids.sub_label.text = "チェックボックスを押してジェスチャを決めます"
        self.ids.image_back.source = './image/back_gr.png'
        self.ids.main_image.source = './image/hand/base.png'
        setfinger(self)
        if round == scene - 1:
            self.ids.main_float.add_widget(FingerSelector())
        #finish key

    if scene == 6:
        
        if setting_file_exist == True:
            self.ids.main_image.source = './image/none.png'
            clearfinger(self)
            self.ids.right_image.source = './image/hand/base.png'
            self.ids.left_image.source = './image/hand/base.png'
            setfinger_r(self, move_key)
            setfinger_l(self, back_key)
            self.ids.main_label.text = ""
            self.ids.left_label.text = "「戻るキー」"
            #self.ids.left_label.text = str(back_key)
            self.ids.right_label.text = "「進むキー」"
            #self.ids.right_label.text = str(move_key)
            self.ids.sub_label.text = str(cam_show[int(setting_list[1])])
        else:
            self.ids.main_label.text = "その2「戻るキー」"
            for i in range(5):
                move_key[i] = int(finger[i])
            all_keys.append(move_key)
            #print("Finish Key =" + str(finger))
            self.ids.main_image.source = './image/hand/base.png'
            if round == scene + 1:
                self.ids.main_float.add_widget(FingerSelector())
                setfinger(self)



    if scene == 7:
        self.ids.main_label.text = "準備が整いました、始めましょう"
        self.ids.main_image.source = './image/logo.png'
        self.ids.left_label.text = ""
        self.ids.right_label.text = ""
        self.ids.sub_label.text = ""
        self.ids.right_image.source = './image/none.png'
        self.ids.left_image.source = './image/none.png'
        setfinger_l(self, [0, 0, 0, 0, 0])
        setfinger_r(self, [0, 0, 0, 0, 0])
        #print("Back Key =" + str(back_key))
        if setting_file_exist == False:
            for i in range(5):
                back_key[i] = int(finger[i])
            all_keys.append(back_key)
            prest.setting(show_performance, camera_number, move_key, back_key, finish_key, default_hands)
            clearfinger(self)
            self.ids.main_float.remove_widget(self2)

        for i in range(2):
            for j in range(2):
                if i != j and all_keys[i] == all_keys[j]:
                    scene = 51

    if scene == 8:
        self.ids.main_label.text = "PRESTシステムを起動中..."
        self.ids.image_next.source = './image/none.png'
        self.ids.image_back.source = './image/none.png'
        self.ids.main_image.source = './image/hand/base.png'
        Clock.schedule_interval(self.update, 0.01)
        scene = 9

    if scene == 10:
        scene = 50
        
    if scene == 11:
        if save_file:
            self.ids.main_label.text = "設定を保存しました、ボタンを押して終了します"
        else:
            self.ids.main_label.text = "設定を破棄しました、ボタンを押して終了します"
            prest.reset()
        self.ids.image_center.source = './image/center_gr.png'
        self.ids.image_next.source = './image/none.png'
        self.ids.image_back.source = './image/none.png'

    #以下エラー構文
    if scene >= 50:
        self.ids.image_next.source = './image/none.png'
        self.ids.image_back.source = './image/none.png'
        self.ids.image_center.source = './image/center_gr.png'
        print("エラー番号: " + str(scene))

    if scene == 50:
        self.ids.main_label.text = "想定外のエラーです"
    if scene == 51:
        self.ids.main_label.text = "重複する指の設定はできません"
    if scene == 52:
        self.ids.main_label.text = "カメラへのアクセスを許可してください"

    if scene == 2 and setting_file_exist:
        round = 5
    elif reshow == True :
        reshow = False
    else:
        round = scene

    #print(round)

class MainScreen(BoxLayout):
    def button_clicked_n(self):
        global round
        if round < 8 or round == 10:
            change_scene(self, 1)

    def button_clicked_b(self):
        global round
        if round < 8 or round == 10:
            change_scene(self, 0)
    def button_clicked_c(self):
        global round, fin
        if round >= 50:
            prest.reset()
        if round > 10:
            exit()
        if round == 9:
            self.ids.main_label.text = "PRESTシステムを終了中..."
            fin = True

    def button_ch_n(self):
        global round
        if round < 8:
            self.ids.image_next.source = './image/next.png'
        if round == 10:
            #Yesの画像を挿入
            self.ids.image_next.source = './image/yes.png'
    def button_ch_b(self):
        global round
        if round < 8:
            self.ids.image_back.source = './image/back.png'
        if round == 10:
            #Noの画像を挿入
            self.ids.image_back.source = './image/no.png'
    def button_ch_c(self):
        global round
        if round > 8:
            self.ids.image_center.source = './image/center.png'

        #エラー時用
        if round > 50:
            self.ids.image_center.source = './image/center.png'

    def update(self, dt):
            global roop, finger, round, back_key, move_key, finish_key, fin
            if roop:
                roop, status = prest.prest(fin)

                self.ids.image_center.source = './image/center_gr.png'
                #print(status)
                tmp_finger = int(re.sub(r"\D", "", status))
                i = 4
                while i >= 0:
                    finger[i] = tmp_finger%10
                    tmp_finger//=10
                    i-=1
                if ('none' in status and fin == False):
                    self.ids.main_label.text = "カメラに手を向けてください"
                    finger = [1, 1, 1, 1, 1]
                else:
                    if move_key == finger:
                        self.ids.main_label.text = "「進む」"
                    elif back_key == finger:
                        self.ids.main_label.text = "「戻る」"
                    elif ('fin' in status):
                        round += 1
                        last_set(self)
                    elif ("right" in status or "left" in status):
                        self.ids.main_label.text = "手を認識しました、ジェスチャを利用できます"

                #指の状態を画面に反映
                if round < 10:
                    setfinger(self)
            else :
                pass

def last_set(self):
    #scene = 10
    clearfinger(self)    
    self.ids.main_image.source = './image/logo.png'

    #任意保存
    self.ids.main_label.text = "お疲れ様でした、設定を保存しますか？"
    self.ids.image_center.source = ''
    self.ids.image_next.source = './image/yes.png'
    self.ids.image_back.source = './image/no.png'



class Prest_Kivy(App):
    title = "Prest"
    def build(self):
        root = MainScreen()
        return root

Prest_Kivy().run()
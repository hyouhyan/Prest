# Prest

## 概要
PCに搭載されているWebカメラ等を利用し、手を認識・トラッキングすることでPCの遠隔操作を可能にしています。  
Prestでは、プレゼンテーション時の操作を遠隔で行うことを目的で開発されました。  
PRESTフォルダ内の"Trac_mac.py"を利用することでプレゼンテーション以外でも利用することができます。  
### 対応OS : MacOS

## 事前準備
### pythonのインストール
python3.9をインストールしてください。3.9以外のバージョンの動作確認はしていません。
### pythonライブラリのインストール
<pre>
pip install mediapipe
pip install opencv-python
pip install pyautogui
pip install playsound
pip install kivy
pip install japanize-kivy
        OR
pip install -r requirements.txt
</pre>

## 使用方法
<pre>
python3 Prest_mac.py
        OR
python Prest_mac.py
</pre>
"Prest_mac.py"を実行後、カメラ、アクセシビリティへのアクセスの許可が求められた場合許可をしてください。  
### 操作方法
1. 利用するカメラを選択してください
2. ジェスチャーを各指に対応するチェックボックスから選択し、設定してください。
3. カメラの前に手をかざし、操作を開始してください。
4. 終了後、設定を保存するか選択してください。
### 設定リセット方法
PRESTフォルダ内の"settings.prt"ファイルを削除してください。  
"settings.prt"が存在しない場合、設定が保存されていない可能性があります。

## Contributor
- System [@KlTUNE](https://github.com/KlTUNE)
- GUI [@Hyouhyan](https://github.com/hyouhyan)
- WEB [@]()
- Designer [@]()

###### ©︎ Prest 2021

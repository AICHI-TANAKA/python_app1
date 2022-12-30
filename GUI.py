import tkinter
import os
from PIL import Image, ImageTk
# import mysql.connector
# from mysql.connector import errorcode
# from sshtunnel import SSHTunnelForwarder
import urllib.request
import json
import base64
import time
from itertools import cycle
import asyncio
# from concurrrent.futures import ProcessPoolExecutor

# 質問クラス
class Question(tkinter.Frame):
  # ラジオボタン選択結果格納用配列
  selectedNumList = []
  animeList =[]

  def __init__(self, master = None):
    super().__init__(master)
    # ラジオボタンの値初期化(checked?)
    self.radio_value = tkinter.IntVar(value = 0)


  def radio_clickTest(self):
    # # ラジオボタンの値を取得
    value = self.radio_value.get()
    # print(f"ラジオボタン")
    self.selectedNumList.append(value)

  def button_click(self):
    try:
      # 既存のボタンの削除
      self.radio0.forget()
      self.radio1.forget()
      self.radio2.forget()
      self.button.forget()

      # アニメDB検索処理
      # json形式の対応表を用いて、選択値と文字列の変換を行う(tkinterのラジオボタンは数字しか渡せないため)
      with open("animeIndex_forAPI.json") as animeIndex:
        genreName = json.load(animeIndex)
        selectedIndex = str(self.selectedNumList[0])
        # APIに情報を渡し、検索結果を取得
        self.animeList = self.animelist_fetch(genreName[selectedIndex])
        # 検索結果を表示
        self.result_display(self)
        return True
    except Exception as e:
      print(e)


  # 取得結果を表示する
  def result_display(self, master):
    result = False #初期値
    for cnt, data in cycle(enumerate(self.animeList)):
      if result:
        result.destroy()

      result = tkinter.Label(self.master,
                            text=self.animeList[cnt]['title'],
                            bg="white",
                            fg="black")
      self.after(3000, result.pack())
      self.update()
      self.update_idletasks()



  def ButtonMake(self, master):
    # ラジオボタンの作成
    self.radio0 = tkinter.Radiobutton(self.master,
                                      text = "バトル系",
                                      command = self.radio_clickTest,
                                      variable = self.radio_value,
                                      value = 1
                                      )

    self.radio1 = tkinter.Radiobutton(self.master,
                                      text = "恋愛系",
                                      command = self.radio_clickTest,
                                      variable = self.radio_value,
                                      value = 10
                                      )

    self.radio2 = tkinter.Radiobutton(self.master,
                                      text = "ロボット系",
                                      command = self.radio_clickTest,
                                      variable = self.radio_value,
                                      value = 6
                                      )

    # ボタンの作成
    self.button = tkinter.Button(self.master,
                                  text = "検索",
                                  command = self.button_click
                                  )

    self.radio0.pack()
    self.radio1.pack()
    self.radio2.pack()
    self.button.pack()

  # 今は使用していないが今後使用予定
  def ButtonMake2(self, master):
    # 既存のボタンの削除
    self.radio0.forget()
    self.radio1.forget()
    self.radio2.forget()
    self.button.forget()

    # ラジオボタンの作成
    self.radio0 = tkinter.Radiobutton(self.master,
                                      text = "ラジオボタン3",
                                      command = self.radio_clickTest,
                                      variable = self.radio_value,
                                      value = 0,
                                      )

    self.radio1 = tkinter.Radiobutton(self.master,
                                        text = "ラジオボタン4",
                                        command = self.radio_clickTest,
                                        variable = self.radio_value,
                                        value = 1
                                        )

    self.radio2 = tkinter.Radiobutton(self.master,
                                        text = "ラジオボタン5",
                                        command = self.radio_clickTest,
                                        variable = self.radio_value,
                                        value = 2
                                        )

    # ボタンの作成
    self.button = tkinter.Button(self.master,
                                  text = "次へ",
                                  command = self.button_click
                                  )

    self.radio0.pack()
    self.radio1.pack()
    self.radio2.pack()
    self.button.pack()


  # おすすめアニメ抽出処理
  def animelist_fetch(self, genre):
    # APIへリクエストを送り、結果をjsondで取得
    user = 'a'
    password = 'a'
    basic_auth = base64.b64encode('{}:{}'.format(user, password).encode('utf-8'))
    url = 'http://rqsaicbartlo.sakura.ne.jp/WebAPI/DBAccess.php?genre='+genre

    request = urllib.request.Request(url,
                                    headers={'Content-Type': 'application/json',
                                            'Authorization': 'Basic ' + basic_auth.decode('utf-8')})

    try:
      with urllib.request.urlopen(request) as response:
        body = json.loads(response.read())
    except urllib.error.URLError as e:
      print(e.reason)

    return body



# 回答クラス
# class Answer():
# def
if __name__ == '__main__':
  # ウィンドウ作成
  root = tkinter.Tk()
  # ウィンドウを最前面に表示
  root.attributes('-topmost', True)
  # サイズ指定
  root.minsize(width=300, height=400)
  # フレーム作成
  frame = tkinter.Frame(root, width=300, height=400)
  # フレームのサイズを固定する（配下ウィジェットに押し出されないように）
  frame.propagate(False)
  # ウィジェットの配置方法を指定
  frame.pack()


  # # ナナチの画像配置
  img = Image.open('./nanachi.png')
  img_resize = img.resize((230,230))
  nanachi_png = ImageTk.PhotoImage(img_resize)
  image = tkinter.Label(frame, image=nanachi_png, bg='black')
  image.pack()

  obj = Question(master = frame)
  obj.ButtonMake(master = frame)

  root.mainloop()
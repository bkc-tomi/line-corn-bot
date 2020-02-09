#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 21:47:49 2020

@author: matsumuratomiakira
"""

import os
from flask import Flask, request, abort
import sys
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent,
                            TextMessage, TextSendMessage)
from pathlib import Path

sys.path.append(os.getcwd() + "/module")
from predict import predict_corn


app = Flask(__name__)
line_bot_api = LineBotApi("CrHpg+og8J+/2FoLvlslEosmuMASGBix3ybhzOf2dIllvD6MBoI\
QbTlUwLfvs865BgQWrcCNHAIeYDxZAhVJ9p293V6UgOfVnTVeaDdN7n29zw6BnLfdSnW\
y5NIctWXk5T2w3+eMc81ZsCRx8040IgdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("63b40d26ce6fd97fdcb3756e21186a12")

SRC_IMAGE_PATH = os.getcwd() + "/{}_src.jpg"
MAIN_IMAGE_PATH = os.getcwd() + "/{}_main.jpg"
PREVIEW_IMAGE_PATH = os.getcwd() + "/{}_preview.jpg"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event.message.text = "画像を送ってね！"
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id

    src_image_path = Path(SRC_IMAGE_PATH.format(message_id)).absolute()
    main_image_path = MAIN_IMAGE_PATH.format(message_id)
    preview_image_path = PREVIEW_IMAGE_PATH.format(message_id)

    # 画像を保存
    save_image(message_id, src_image_path)

    # 画像の加工、保存
    print(src_image_path)
    print(str(src_image_path))
    try:
        msg = predict_corn(str(src_image_path))
    except:
        msg = "‪ごめん、エラーが出たみたい。"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

    # 画像を削除する
    src_image_path.unlink()

def save_image(message_id: str, save_path: str) -> None:
    """保存"""
    message_content = line_bot_api.get_message_content(message_id)
    with open(save_path, "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

if __name__ == "__main__":
    app.run()
# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('OVdUEq7/slwzuZHhsZBca4gTeQr4uOLAv4l9q+UV9j+kProl3sn0rCvENZ+DFybFwBM+VDTyEcEW5mSKAdVa7bzSccKvRygtuUgqnLwO89J8nA0IElpeNpv6jnerVy6sEkyuBdwNBjYI6CW6z6W0MAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('17edfdad94a4460c9ffb7bac5349247e')

line_bot_api.push_message('U63844831444e54a4fe98280c905fa6e6', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        confirm_template_message = TemplateSendMessage(
            alt_text='這是TemplateSendMessage',
            template=ConfirmTemplate(
                text='你喜歡韓國嗎？',
                actions=[
                    PostbackAction(
                        label='喜歡',
                        display_text='超喜歡',
                        data='action=其實不喜歡'
                    ),
                    MessageAction(
                        label='讚',
                        text='讚讚'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

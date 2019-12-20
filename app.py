import os
import glob
from utils.csvFinder import csvFinder


from flask import Flask, request, abort

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_storage_path = os.path.join(base_dir,"CSVs")
csv_files = [f for f in os.listdir(csv_storage_path) if f.endswith('.csv')]


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('tdW2cT7Rxu4MWnV3Z9nEy9EWIbsy3fFX8De+lX6xIiL5OU0YYLr5BugLvT3qZVNEtK9itMtnFcxkh0MFbisLCtmlHXWJHG43919vEHti6RnWPKJ6Cs3WfouwVwGntNL/zXhRSv3OTiefzpzXjUwsKQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('da180eac5e665afbfc0a40232d524049')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text_from_user = event.message.text
    reply_token = event.reply_token

    CSV = csvFinder(csvPath=os.path.join(csv_storage_path,csv_files[0]))
    res = CSV.find_row(val=text_from_user,limit=3)

    string_to_reply_1 = "🧐🧐keyword ที่ค้นหา🧐🧐\n➖➖➖➖➖➖➖➖➖\n         {}\n➖➖➖➖➖➖➖➖➖\n".format(text_from_user)
    string_to_reply_1 += "ทำการค้นหาเรียบร้อยคะ"
    string_to_reply_1 += "\nส้มพบข้อมูลที่ใกล้เคียง\nทั้งหมด {} รายการคะ  \n".format(len(res))
    string_to_reply_2 = ""

    for num,i in enumerate(res ,start=1):
        
        string_to_reply_2 += "➖➖➖🔴 รายการที่ {}➖➖➖  \n".format(num)

        for key,val in i["result"].items():
            string_to_reply_2 += "\n ➖{} \n        > {} ".format(key,val)
        
        string_to_reply_2 += "\n\n"

    text_1 = TextSendMessage(text=string_to_reply_1)
    text_2 = TextSendMessage(text=string_to_reply_2)



    line_bot_api.reply_message(
        event.reply_token,
        messages=[text_1,text_2]
        )


if __name__ == "__main__":
    app.run(port=8000,debug=True)



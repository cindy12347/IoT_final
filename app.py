from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='dOBtG5dEqkb/JWk1UrLxfpeXWH44gdDUj0yW/8labLdLY3+1s1DxhTOQ+FM6u/DSh7bVatXM6SgikLni/98A7aCMiiefbFZ790FbIqHl7FG47vgsDBJBqo49IXfhnx1Y6AUzXzFnpysZq/qtmKXOfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c38f9d5ed556c8ebae0d0103dc89a738')


app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        logging.error(f"Error in callback: {e}")
        return 'Internal Server Error', 500

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    reply_text = f"You said: {message_text}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    reply_text = f"Thank you for following! Your user ID is {user_id}."
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

# New API endpoint
@app.route("/new_api", methods=['GET'])
def new_api():
    # Example of making a request to another API (https://smart-campus.kits.tw/)
    api_url = "https://smart-campus.kits.tw/"
    try:
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            data = {"message": "This is a new API endpoint!", "status": "success", "api_data": response.text}
        else:
            data = {"message": "Error accessing the external API", "status": "error"}
    except Exception as e:
        logging.error(f"Error in making API request: {e}")
        data = {"message": "Error accessing the external API", "status": "error"}

    return jsonify(data)

if __name__ == "__main__":
    app.run()

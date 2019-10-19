#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

import os
import urllib.request


app = Flask(__name__)

ACCESS_TOKEN = 'EAAiZCfSvRvfYBANMBt3E5EqDckFrPEG1BvRQeJ8emrh9mmHbGYQjFVmgdln9jZBcZAtZBNo2bqsZCobmZBzFLTVzWSmNPZBK12WPlWS3ZAiKx1DWAB5wZCLeamA8yqZCjs7763EY9S0PeRN1lNrHx0CM3ZBO5gIfD9J6K8ccYFYo9w77zhbRJGATJbtMV0EzY1jlOYZD'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'Salam'   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)



def load_model():

    with open(model.json, 'r') as model_file:
        model_json = model_file.read()

    model = model_from_json(model_json)

    model.load_weights('model.h5')
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model



def predict_class(model, image_path):

    image = image.load_img(image_path, target_size=(64, 64))
    image = image.img_to_array(test_image)
    image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    
    max_pred, max_class = 0, 0

    for i in range(len(result)):
        if pred > max_pred:
            max_pred = pred
            max_class = i

    if max_class == 0:
        return 'other'
    elif max_class == 1:
        return 'wild_fire'
    else:
        return 'residential_fire'


model = load_model()


#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = 'Please send media file showing fire accident'
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = 'Thanks for informing us. We will make feedback as soon as possible'
                    image_url = message['message'].get('attachments')[0].payload.url
                    urllib.request.urlretrieve(image_url, "image.jpg")
                    image_class = predict_class(model, 'image.jpg')
                    send_message(recipient_id, image_class)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template ,request,jsonify,url_for,send_file
from func.Speak.SpeakOffline2 import Speak
from llm.ChatGpt import ChatGpt
from os import getcwd

app = Flask(__name__)

import os
import pygame

def Speak(data):
    command = f'edge-tts --voice "en-CA-LiamNeural" --pitch=+5Hz --rate=+22% --text "{data}" --write-media "temp/data.mp3" '
    os.system(command)
    #pygame.init()
    #pygame.mixer.init()
    #pygame.mixer.music.load(r"temp/data.mp3")
    #pygame.mixer.music.play()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/postdata', methods=['POST'])
def post_data():
    if request.method == 'POST':
        # Check if the content type is JSON
        if request.is_json:
            data = request.get_json()  # Get the JSON data from the request
            # Perform operations with the received JSON data (example: print it)
            print("Received JSON data:", data)
            Q=data["text"]
            reply=ChatGpt(f"{Q} ***reply like tony stark jarvis in less words and don't write code***")
            Speak(reply)
            new = f"{getcwd()}\\temp\\data.mp3"
            return send_file(new, as_attachment=True)
        else:
            return jsonify({'error': 'Invalid Content-Type. Expected application/json'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4444)

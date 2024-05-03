from func.Osrc.Chat import Chat
from func.Speak.SpeakOffline2 import Speak
from func.Listen.ListenJs import Listen
from func.Osrc.DataOnline import Online_Scraper
from func.XTRA.ExecCode import ExecCode
from func.Social.News import News
from func.Ocr.OcrOffline import Ocr
from func.XTRA.Clap import MainClapExe
from func.Jukebox.YouTube import MusicPlayer

from llm.Filter import Filter
from llm.ChatGpt import ChatGpt,messages as gms
from llm.Mistral2 import Mistral7B,messages as mms

from buildin import GoodMsg
from buildin import KnowApps

from autofunc.youtube import GetTranscript
from Powerpointer.app import get_bot_response

from Genration_Of_Images import *


from colorama import Fore, Back, Style
import pyperclip as pi
from mtranslate import translate
import random
import pygetwindow as gw
import keyboard
import time
from os import startfile,getcwd

# from auth.FaceAuth import FaceAuth

# MainClapExe()
# Speak("Face Id required.")
# ID=FaceAuth()
# Speak(f"Login with Face Id of {ID}")

#init
gms.append({"role":"system","content":f"todays news are\n{News()}"})
mms.append({"role":"system","content":f"todays news are\n{News()}"})



if __name__=="__main__":
    while 1:
        Q=Listen()
        Q = translate(Q, 'en', 'auto')
        QL=Q.lower()
        LQ=len(Q.split(" "))
        SQ=Q.split(" ")[0]
        EQ=Q.split(" ")[-1]
        NQ=QL.removeprefix("jarvis")
        CURRENT_APP=""
        try:
            CURRENT_APP = gw.getActiveWindowTitle()
        except :
            CURRENT_APP = ""
        #CURRENT_APP NAME
        CURRENT_APP_NAME=CURRENT_APP.split(" - ")[-1]

        if (SQ=="click" or (SQ=="double" and "click" in Q)) and LQ<7:
            QL=QL.replace("click","")
            QL=QL.replace("on","")
            QL=QL.replace("jarvis","")
            QL=QL.replace("double","")
            QL=QL.replace("button","")
            A=Ocr(QL.strip())
            Speak(A)
        
        elif NQ in ["optimize this code","write code for this","optimise this code","jarvis optimise this code"]:
            keyboard.press_and_release("ctrl + c")
            time.sleep(1)
            clipboard_data = pi.paste()
            r=ChatGpt(f"{clipboard_data} **{NQ}**")
            r=Filter(r)
            if r==None:
                Speak("i can't do that sir")
            else:
                pi.copy(r)
                keyboard.press_and_release("ctrl + v")
                Speak(random.choice(GoodMsg))
        elif "powerpoint"in QL and NQ.split(" ")[0].lower()=="create":
            path=get_bot_response(Q)
            startfile(fr"{getcwd()}\{path}")
            Speak("done sir")
            Speak(random.choice(GoodMsg))
        
        elif QL.find("read my selection")==0 or QL.find("read my selected text")==0:
            Speak("Sure sir reading your selected data")
            keyboard.press_and_release("ctrl + c")
            time.sleep(1)
            clipboard_data = pi.paste()
            Speak(clipboard_data)

        elif "read data from my clipboard" in QL or "read my clipboard" in QL or "read clipboard" in QL or "copy data from my clipboard" in QL:
            QL = QL.replace("read data from my clipboard", "")
            QL = QL.replace("read my clipboard", "")
            QL = QL.replace("read clipboard", "")
            keyboard.press_and_release("ctrl + c")
            Speak("ok just give me a second")
            jo = pi.paste()
            gms.append({"role": "user", "content": jo})
            Speak("data copied")

        elif ("summarize" in NQ or "transcribe" in NQ or "translate") and "video" in NQ and LQ<10:
            transcript=GetTranscript()
            if transcript == None:
                Speak("No sir, i can't do that")
            else:
                responce = ChatGpt(transcript+f" **{NQ.replace('video','text')}**")
                Speak(responce)

        elif "jarvis"==SQ.lower():
            responce = ChatGpt(f"{Q} ***use python programing language. just write complete code nothing else, also don't dare to use input function*** **you can use the module that i provided if required**")
            code = Filter(responce)
            if code!=None:
                if "from Genration_Of_Images import" in code or "import" not in code:
                    exec(code)
                elif "from func.Jukebox.YouTube import MusicPlayer" in code:
                    exec(code)
                else:
                    Done=ExecCode(code)
                    print(Done)
                    if Done:
                        Speak(random.choice(GoodMsg))
                    else:
                        for i in range(3):
                            with open(r"error.log", "r") as f:
                                res = f.read()
                                if res != "":
                                    ChatGpt(f"{res} /n" + "**fix this and write full code again. with different approach**")
                                    code = Filter(code)
                                    if code==None:
                                        break
                                    Done=ExecCode(code)
                                    if Done==True:
                                        break
                                else:
                                    break
                        Speak("Sorry sir i Can't Do that")
            else:
                Speak(responce)

        elif CURRENT_APP_NAME in KnowApps:
            
            Func_=KnowApps[CURRENT_APP_NAME]
            Output = Func_(QL)
            if Output != False:
                keyboard.press_and_release(Output)

            else :
                    web=Online_Scraper(Q)
                    if web!=None:
                        Speak(web)
                    elif Chat(QL)[1]>0.99:
                        Speak(Chat(QL)[0])
                    else:
                        gms.append({"role": "user", "content": Q})
                        reply=Mistral7B(Q+" ***reply like tony stark jarvis in less words and don't write code***")
                        Speak(reply)
        else :
            web=Online_Scraper(Q)
            if web!=None:
                Speak(web)
            elif Chat(QL)[1]>0.99:
                Speak(Chat(QL)[0])
            else:
                gms.append({"role": "user", "content": Q})
                reply=Mistral7B(Q+" ***reply like tony stark jarvis in less words and don't write code***")
                Speak(reply)









#5x + 7 = 11
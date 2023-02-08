import os
from pyChatGPT import ChatGPT
from .cookieDecode import get_cookie_from_chrome
from voice2Text import getVoiceInput
import winsound as ws

"""
    this module use pyChatGPT(a python wapper) to post request
    to openai server and can successfully interact with chatGPT without 
    go through robot detection.
"""

def getInput():
    user_input = input("input your words (use 'quit' to exit):\n")
    return user_input

def getTokenByUser():
    token = input("Copy your token from ChatGPT and press Enter \n")
    return token

def getAPI_Obj():

    session_token = getTokenByUser() #get token by user input

    api = ChatGPT(session_token) #get api obj
    return api


def getAPI_Obj_Chrome():
    session_token = get_cookie_from_chrome()
    api = ChatGPT(session_token)
    return api


def sendRequestByW(question,api)-> ChatGPT:
    """
        send req to openai server by user write
    """
    reqMsg = question

    if reqMsg == '再见':
        # ws.PlaySound(r'.\output_sound\saybye.wav',flags=ws.SND_FILENAME)
        return "quit"

    res = api.send_message(reqMsg) #send message to openai and get respone

    message = res["message"].replace('\n','') #get message

    return message

def sendRequestByVoc(api) -> ChatGPT:
    """
        send req to openai server by user voice
    """
    reqMsg = getVoiceInput()

    if reqMsg == "再见":
        # ws.PlaySound(r'.\output_sound\saybye.wav',flags=ws.SND_FILENAME)
        return "quit"

    res = api.send_message(reqMsg) #send message to openai and get respone

    message = res["message"].replace('\n','') #get message

    return message

def sendReqByChoice(question,choice,api):
    if choice == "1": #choice voice input
        message = sendRequestByVoc(api)
    else: #default:w
        message = sendRequestByW(question,api)

    return message
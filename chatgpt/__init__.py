from pyChatGPT import ChatGPT
from voice2Text import getVoiceInput

"""
    this module use pyChatGPT(a python wapper) to post request
    to openai server and can successfully interact with chatGPT without 
    go through robot detection.
"""

class ChatGPTHolder(ChatGPT):

    def __init__(self, api: ChatGPT = None, session_token: str = None, isfirstReq: bool = True):
        self.api = api
        self.session_token = session_token
        self.isfirstReq = isfirstReq

    @staticmethod
    def GetInput():
        user_input = input("input your words (use 'quit' to exit):\n")
        return user_input

    @staticmethod
    def GetTokenByUser():
        token = input("Copy your token from ChatGPT and press Enter \n")
        return token

    def GetAPI_Obj(self):

        session_token = ChatGPTHolder.GetTokenByUser() #get token by user input

        self.api = ChatGPT(session_token) #get api obj

    def GetAPI_Obj_Chrome(self):
        api = ChatGPT(self.session_token)
        self.api = api

    def SendRequestByW(self,question)-> ChatGPT:
        """
            send req to openai server by user write
        """
        reqMsg = question

        if reqMsg == '再见':
            # ws.PlaySound(r'.\output_sound\saybye.wav',flags=ws.SND_FILENAME)
            return "quit"

        res = self.api.send_message(reqMsg) #send message to openai and get respone

        message = res["message"].replace('\n','') #get message

        return message

    def SendRequestByVoc(self) -> ChatGPT:
        """
            send req to openai server by user voice
        """
        reqMsg = getVoiceInput()

        if reqMsg == "再见":
            # ws.PlaySound(r'.\output_sound\saybye.wav',flags=ws.SND_FILENAME)
            return "quit"

        res = self.api.send_message(reqMsg) #send message to openai and get respone

        message = res["message"].replace('\n','') #get message

        return message

    def SendReqByChoice(self,question,choice):
        if choice == "1": #choice voice input
            message = self.SendRequestByVoc()
        else: #default:w
            message = self.SendRequestByW(question)

        return message

    def InitChatGPT(self):
        if self.isfirstReq:
            with open("./chatgpt/init_chatgpt.txt",encoding='utf-8') as textfile: #read init text file
                initChatgptText =  textfile.read()
            self.api.send_message(initChatgptText) #send init message
            self.isfirstReq = False
            return True
        else:
            return False
    
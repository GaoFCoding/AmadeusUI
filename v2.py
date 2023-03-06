import chatgpt
from langdetect import detect
from chatgpt import translate
from socket_server import SocketClient
from TTS_model import SoundGenerator
from voice2Text import getVoiceInput,loadVoiceModel
from pydub import AudioSegment
import logging

numba_logger = logging.getLogger('numba') #初始化日志 
numba_logger.setLevel(logging.WARNING) #设置日志级别

chatgpt.InitChatGPT()

clienter = SocketClient() #实例化SocketClient对象

model = loadVoiceModel() #实例化V2T模型对象

print("********************************\n welcome to Amadeus v2.3\n********************************")        

def main():

    clienter.SocketServerKeeper() #socket连接

    choice = clienter.RecData() #inputMethod: Keyboard/Voice
    if choice == -1: #连接中断处理
        return

    choice = int(choice)

    while True:  #keep_alive

    #***************获取用户问题*****************#
        if choice == 0:
            question = clienter.RecData()
            if question == -1: #连接中断处理
                return

        elif choice == 1:
            question = getVoiceInput(model).replace(" ","")
            if question == "":
                continue

            isClient = clienter.SendData(question) #向客户端发送问题
            if isClient == -1: #连接中断处理
                return

            getQues = clienter.RecData() #阻塞直到客户端收到question
            print(getQues)
            if getQues == -1:
                return
            
        print("Question Received: " + question)

    #***************获取回复*****************#

        message = chatgpt.SendRequest(question)

        print("Amadeus:\n",message,"\n...end")

        if message == "quit":
            isClient = clienter.SendData(message) #发送退出信号给客户端
            if isClient == -1:
                return
            clienter.RemoveFromPool() #删除连接池中的连接
            print("exit from Amadeus System")
            return
        
        lanType = detect(message) #输出语言判断
        if lanType != "ja": #chatgpt回复判断，确保输入到模型的语料是Ja
            message = translate.TranslateByBaidu(message, toLang="jp") #纠正输出，将其他语言的输出转换为日文
            """
            isClient = clienter.SendData("retry")
            if isClient == -1:
                return
            print("\nthe resp was not in Ja, please retry\n")
            continue
            """        
        # make sound file
        SoundGenerator(message)

        src = "./output_sound/output.wav"
        dst = "./game/audio/output.ogg"

        sound = AudioSegment.from_wav(file=src)
        sound.export(dst, format="ogg") #将生成的音频转换成ogg格式并放到rpy的audio目录

        translateRes = translate.TranslateByBaidu(message) #通过翻译将输出的日文译为中文

        isClient = clienter.SendData(translateRes) #将译文传给客户端
        if isClient == -1:
            return

        msg = clienter.RecData() #在此阻塞直到客户端播放完成
        if msg == -1:
            return
        print(msg) 

if __name__ == "__main__":

    while True:
        main() #主线程,与chatgptholder并行
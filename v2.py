import os
import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #添加项目目录路径到path列表中
# sys.path.append(BASE_DIR)
# print(sys.path)
import torch
from TTS_proj import commons
from TTS_proj import utils
from TTS_proj.models import SynthesizerTrn
from TTS_proj.text.symbols import symbols
from TTS_proj.text import text_to_sequence
import winsound as ws
from scipy.io.wavfile import write
from langdetect import detect
import chatgpt
from chatgpt import translate_Bidu
import logging
from socket_server import SendData,RecData,SocketServerKeeper
from socket_server import RemoveFromPool
from voice2Text import getVoiceInput
from pydub import AudioSegment


numba_logger = logging.getLogger('numba')
numba_logger.setLevel(logging.WARNING)

def get_text(text, hps):  #输入文本处理
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file("./TTS_model/configs/steins_gate_base.json") #获取模型input参数配置文件

net_g = SynthesizerTrn( #生成语音合成器
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model)
_ = net_g.eval()

_ = utils.load_checkpoint("./TTS_model/G_265000.pth", net_g, None) #获取TTS模型


def SoundGenerator(content):
  """
    语音生成器，向模型中输入预处理的文本信号，输出语音并保存为.wav文件
  """
  stn_tst = get_text(content, hps)
  with torch.no_grad():
      x_tst = stn_tst.unsqueeze(0)
      x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
      audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.float().numpy()
      write("./output_sound/output.wav", hps.data.sampling_rate, audio) #写入语音文件(.wav)到output_sound文件夹
      print("generate sound success")


def main():

    SocketServerKeeper() #socket连接

    print("********************************\n welcome to Amadeus v2.0\n********************************")
        
    try:
        api = chatgpt.getAPI_Obj_Chrome() #获取pychatgpt的api对象
    except:
        raise ValueError("please check your network !!!")
        

    with open("./chatgpt/init_chatgpt.txt",encoding='utf-8') as textfile: #读取初始化chatgpt设定的文本
       initChatgptText =  textfile.read()
    api.send_message(initChatgptText) #输入初始化设定

    isClient = SendData("chatgpt and v2 server is ready")  #发送完成服务端与chatgpt初始化的信息
    if isClient == -1: #连接中断处理
        return
    print("已发送消息")

    
    choice = RecData() #inputMethod: Keyboard/Voice
    if choice == -1: #连接中断处理
        return

    choice = int(choice)

    while True:  #keep_alive

    #***************获取用户问题*****************#
        if choice == 0:
            # total_data = bytes()
            # while True:
            #     data = client.recv(1024)
            #     total_data += data
            #     if len(data) < 1024:
            #         break
            question = RecData()
            if question == -1: #连接中断处理
                return

        elif choice == 1:
            question = getVoiceInput()
            isClient = SendData(question)
            if isClient == -1: #连接中断处理
                return

        print("Question Received: " + question)

    #***************获取回复*****************#


        message = chatgpt.sendReqByChoice(question,choice,api)

        print("Amadeus:\n",message,"\n...end")

        if message == "quit":
            isClient = SendData(message) #发送退出信号给客户端
            if isClient == -1:
                return
            RemoveFromPool() #删除连接池中的连接
            print("exit from Amadeus v2.0")
            return
        
        lanType = detect(message)

        if lanType != "ja": #chatgpt回复判断，确保输入到模型的语料是Ja
            isClient = SendData("retry")
            if isClient == -1:
                return
            print("\nthe resp was not in Ja, please retry\n")
            continue
        
        # make sound file
        SoundGenerator(message)

        src = "./output_sound/output.wav"
        dst = "./game/audio/output.ogg"

        sound = AudioSegment.from_wav(file=src)
        sound.export(dst, format="ogg") #将生成的音频转换成ogg格式并放到rpy的audio目录

        translateRes = translate_Bidu.baiduTranslate(message) #通过百度翻译将输出的日文译为中文

        isClient = SendData(translateRes) #将译文传给客户端
        if isClient == -1:
            return

        msg = RecData() #在此阻塞直到客户端播放完成
        if msg == -1:
            return
        print(msg) 
        # ws.PlaySound(r'.\output_sound\output.wav',flags=ws.SND_FILENAME) #播报生成的语音
        

if __name__ == "__main__":

    while True:
        main() #主线程
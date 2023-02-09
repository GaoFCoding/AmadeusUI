import torch
from TTS_proj import commons
from TTS_proj import utils
from TTS_proj.models import SynthesizerTrn
from TTS_proj.text.symbols import symbols
from TTS_proj.text import text_to_sequence
from scipy.io.wavfile import write

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


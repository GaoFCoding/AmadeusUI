import os
os.system('cd monotonic_align && python setup.py build_ext --inplace && cd ..')
import gradio as gr

import matplotlib.pyplot as plt
import IPython.display as ipd

import os
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
import logging

numba_logger = logging.getLogger('numba')
numba_logger.setLevel(logging.WARNING)
import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file("configs/steins_gate_base.json")

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model)
_ = net_g.eval()

_ = utils.load_checkpoint("G_265000.pth", net_g, None)

def syn(content):
  stn_tst = get_text(content, hps)
  with torch.no_grad():
      x_tst = stn_tst.unsqueeze(0)
      x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
      audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.float().numpy()
  return (hps.data.sampling_rate,audio)
  #ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate))


app = gr.Blocks()
with app:
    with gr.Tabs():
        with gr.TabItem("Basic"):
            input1 = gr.Textbox()
            submit = gr.Button("Convert", variant="primary")
            output1 = gr.Audio(label="Output Audio")
        submit.click(syn,input1,output1)
        
app.launch()
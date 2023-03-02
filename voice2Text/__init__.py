import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def loadVoiceModel():
    model = Model("./voice2Text/vosk-model-cn-0.15") #实例化Model
    return model

def getVoiceInput(model):

    device_info = sd.query_devices(None, "input")
    samplerate = int(device_info["default_samplerate"])
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None,
            dtype="int16", channels=1, callback=callback):
            
            rec = KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                # print("listening...")
                if rec.AcceptWaveform(data):
                    resData = rec.Result()
                    msg = eval(resData)
                    # print("output...")
                    return msg["text"]

    except KeyboardInterrupt:
        print("\nDone")
        ...
    except Exception as e:
        print(e)
        ...

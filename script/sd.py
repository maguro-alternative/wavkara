import sounddevice as sd
import soundfile as sf
import numpy as np

def sdf(duration):
    # duration = 3  # 3秒間録音する

    # デバイス情報関連
    # sd.default.device = [3, 7] # Input, Outputデバイス指定
    input_device_info = sd.query_devices(device=sd.default.device[1])
    sr_in = int(input_device_info["default_samplerate"])

    # 録音
    myrecording = sd.rec(int(duration * sr_in), samplerate=sr_in, channels=2)
    # sd.wait() # 録音終了待ち

    print(myrecording.shape) #=> (duration * sr_in, channels)

    # 録音信号のNumPy配列をwav形式で保存
    sf.write("../wav/myrecording.wav", myrecording, sr_in)

# sdf(9)
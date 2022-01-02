import pyaudio
import wave
import sys
from pydub import AudioSegment

import discord
import time

TOKEN = 'ODU0MDA1NDQ4MTg1MzQ4MDk3.YMdojQ.a1Vr_3lqSJ9URCMul3VA9v3mQ9s'

client = discord.Client()

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

# サンプリングレート
RATE = 44100

# 録音時間を入力
# print("録音時間(second)を入力")
# RECORD_SECONDS = int(input())
def myaud():
    base_sound = AudioSegment.from_file("../wav/sample_music.wav", format="wav")
    RECORD_SECONDS = base_sound.duration_seconds

    # print("wavファイル名を入力")
    # RECORD_FILE = str(input())

    RECORD_FILE = "sample_voice.wav"

    if RECORD_FILE.endswith(".wav")==False:
        sys.exit(1)

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=chunk
    )

    start = time.time()

    all = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        all.append(data)
        # client.run(TOKEN)

    stream.close()
    p.terminate()

    data = b''.join(all)

    # 保存するファイル名、wは書き込みモード
    out = wave.open("../wav/"+RECORD_FILE, 'w')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(RATE)
    out.writeframes(data)
    out.close()
    
    end = time.time()
    # 処理時間表示
    print("Total elapsed time : {}[sec]".format(round(end - start, 4)))
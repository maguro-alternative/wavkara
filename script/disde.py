import asyncio
import discord
from discord.channel import VoiceChannel
from discord.ext import tasks
import sounddevice as sd
import soundfile as sf

from autes import myaud
from sd import sdf
from wavcomp import wavsecond2
import time

TOKEN = 'ODU0MDA1NDQ4MTg1MzQ4MDk3.YMdojQ.a1Vr_3lqSJ9URCMul3VA9v3mQ9s'

client = discord.Client()

@client.event
async def on_message(message:discord.Message):
    msg=message.content.split()
    # print(message.author.voice.channel.id)
    if message.content.startswith('.test'):
        # try文でエラーが出る部分を例外処理
        if len(msg[1]) > 0 and message.author.voice is not None:
            voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
            source = discord.FFmpegPCMAudio("../wav/sample_music.wav")
            trans=discord.PCMVolumeTransformer(source,volume=0.5)
            voiceChannel.play(trans, after=check_error)
            # await message.channel.send("録音中...")
            print("録音中.....")
            duration = wavsecond2("../wav/sample_music.wav")

            input_device_info = sd.query_devices(device=sd.default.device[1])
            sr_in = int(input_device_info["default_samplerate"])

            myrecording = sd.rec(int(duration * sr_in), samplerate=sr_in, channels=2)

            await asyncio.sleep(duration)
            print(myrecording.shape) #=> (duration * sr_in, channels)
            # 録音信号のNumPy配列をwav形式で保存
            sf.write("../wav/myrecording.wav", myrecording, sr_in)
            # await VoiceChannel.disconnect()
            # guild = message.guild.voice_client
            # await guild.disconnect()
        elif message.author.voice is None:
            await message.channel.send("ボイスチャンネルに接続してください。")
    # myloop.start()


    # sdf(wavsecond2("../wav/sample_music.wav"))

def check_error(er):
    print('Error check: '+ str(er))

client.run(TOKEN)
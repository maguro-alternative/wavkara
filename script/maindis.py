import discord
from discord.channel import VoiceChannel
import sounddevice as sd
import soundfile as sf

import youtube_dl
import asyncio

from youdl import you
from wavcomp import wavmain
from wavcomp import wavsecond2

TOKEN = ''

client = discord.Client()

@client.event
async def on_message(message:discord.Message):
    msg=message.content.split()
    # print(message.author.voice.channel.id)
    if message.content.startswith('.txt'):
        voice_client = message.guild.voice_client
        # try文でエラーが出る部分を例外処理
        try:
            if len(msg[1]) > 0 and msg[1].startswith("https://www.youtube.com/watch?v=") and message.author.voice is not None:
                await message.channel.send("ダウンロード中...")
                you(msg[1])
                print(msg[1])
                # wavsecond("../wav/sample_music.wav")
                # voiceChannel = await VoiceChannel.connect(timeout=check_error,cls=message.author.voice.channel)
                voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
                source = discord.FFmpegPCMAudio("../wav/sample_music.wav")
                trans=discord.PCMVolumeTransformer(source,volume=0.5)
                voiceChannel.play(trans, after=check_error)
                await message.channel.send("ダウンロード完了！録音中...")
                print("録音中.....")
                duration = wavsecond2("../wav/sample_music.wav")

                input_device_info = sd.query_devices(device=sd.default.device[1])
                sr_in = int(input_device_info["default_samplerate"])

                myrecording = sd.rec(int(duration * sr_in), samplerate=sr_in, channels=2)

                await asyncio.sleep(duration)
                print(myrecording.shape) #=> (duration * sr_in, channels)
                # 録音信号のNumPy配列をwav形式で保存
                sf.write("../wav/sample_voice.wav", myrecording, sr_in)
                guild = message.guild.voice_client
                await guild.disconnect()
                await message.channel.send("録音終了！採点中、、、、")
                ten=wavmain()
                await message.channel.send('点数'+str(ten)+'点です。')
            elif len(msg[1]) > 0:
                print(message.channel)
                await message.channel.send('YouTubeのURLを指定してください。')
            elif message.author.voice is None:
                await message.channel.send("ボイスチャンネルに接続してください。")

        # エラーが出た時の対処
        except youtube_dl.utils.DownloadError:
            await message.channel.send('存在しない動画です。')

        except IndexError:
            await message.channel.send('YouTubeのURLを指定してください。')

        """except Exception as e:
            print("errorDAAAAAAAAAAAAA")
            print(e)
            await message.channel.send('何らかのエラーが発生しました。詳しくはエラーログをご覧ください。')"""

def check_error(er):
    print('Error check: '+ str(er))

client.run(TOKEN)

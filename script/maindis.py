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
async def on_ready():
    activity=discord.Game(name="リモートカラオケ")
    await client.change_presence(activity=activity)

async def on_message(message:discord.Message):
    msg=message.content.split()
    if message.content.startswith('.txt'):
        # try文でエラーが出る部分を例外処理
        try:
            if len(msg[1]) > 0 and msg[1].startswith("https://www.youtube.com/watch?v=") and message.author.voice is not None:
                await message.channel.send("ダウンロード中...")
                you(msg[1]) # youtube-dlでダウンロード開始
                print(msg[1])
                await message.channel.send("ダウンロード完了！.txt singで採点を始めます。")

            elif message.author.voice is None:
                await message.channel.send("ボイスチャンネルに接続してください。")

            elif len(msg[1]) > 0 and msg[1].startswith("sing") and message.author.voice is not None:
                voiceChannel = await VoiceChannel.connect(message.author.voice.channel) # コマンド入力者のボイスチャンネルに接続
                source = discord.FFmpegPCMAudio("../wav/sample_music.wav")              # ダウンロードしたwavファイルをDiscordで流せるように変換
                trans=discord.PCMVolumeTransformer(source,volume=0.5)                   # 音量調整(1/2にする)
                voiceChannel.play(trans, after=check_error)                             # wavファイル再生
                await message.channel.send("録音中...")
                print("録音中.....")
                duration = wavsecond2("../wav/sample_music.wav")                        # wavファイルの秒数を計算

                input_device_info = sd.query_devices(device=sd.default.device[1])
                sr_in = int(input_device_info["default_samplerate"])

                # 録音開始(非同期処理)
                myrecording = sd.rec(int(duration * sr_in), samplerate=sr_in, channels=2)

                # 録音終了まで待機(asyncio.sleepで待機させないとbotが落ちるので注意！！)
                await asyncio.sleep(duration)
                print(myrecording.shape)
                # 録音信号のNumPy配列をwav形式で保存
                sf.write("../wav/sample_voice.wav", myrecording, sr_in)
                guild = message.guild.voice_client
                # ボイスチャンネルから切断
                await guild.disconnect()
                await message.channel.send("録音終了！採点中、、、、")
                # 採点(DTWで誤差を計算)
                ten=wavmain()
                await message.channel.send('点数'+str(ten)+'点です。')
            elif len(msg[1]) > 0:
                print(message.channel)
                await message.channel.send('YouTubeのURLを指定してください。')

        # エラーが出た時の対処
        except youtube_dl.utils.DownloadError:
            await message.channel.send('存在しない動画です。')

        except IndexError:
            await message.channel.send('YouTubeのURLを指定してください。')

def check_error(er):
    print('Error check: '+ str(er))

client.run(TOKEN)
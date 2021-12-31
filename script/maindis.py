import discord
from youdl import you
from mypyaud import myaud
from wavcomp import wavmain

TOKEN = ''

client = discord.Client()

@client.event
async def on_message(message:discord.Message):
    msg=message.content.split()
    if message.content.startswith('.txt'):
        print(message)
        # try文でエラーが出る部分を例外処理
        try:
            if len(msg[1]) > 0 and msg[1].startswith("https://www.youtube.com/watch?v="):
                await message.channel.send("ダウンロード中...")
                you(msg[1])
                print(msg[1])
                await message.channel.send("ダウンロード完了！録音中...")
                print("録音中.....")
                myaud()
                ten=wavmain()
                await message.channel.send('点数'+str(ten)+'点です。')
            elif len(msg[1]) > 0:
                print(message.channel)
                await message.channel.send(message.channel)

        # エラーが出た時の対処
        except:
            print("errorDAAAAAAAAAAAAA")
            # await message.channel.send(f':thinking: ,{message.author.mention} チャンネル名を入力してください。')
client.run(TOKEN)
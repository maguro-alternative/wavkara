import gc
import time
from enum import Enum

import librosa
import numpy as np
import wave
from pydub import AudioSegment
import PySimpleGUI as sg
import sys

def onewav():
    """layout = [
        [sg.Text("原曲wavファイル　　"), sg.InputText(), sg.FileBrowse(key="file1")],
        [sg.Text("比較するwavファイル"), sg.InputText(), sg.FileBrowse(key="file2")],
        [sg.Submit("比較"), sg.Cancel("キャンセル")],
    ]

    window = sg.Window("リモートカラオケ", layout)

    event, values = window.read()
    for v in range(2):
        print(values[v])
    
    if event=="キャンセル":
        print("キャンセルされました。")
        sys.exit(1)

    if values[0].endswith('.wav')==False or values[1].endswith('.wav')==False:
        print("wav以外のファイルが指定されました。")
        sys.exit(1)

    window.close()"""

    values=[]
    values.append("../wav/sample_music.wav")
    values.append("../wav/sample_voice.wav")

    base_sound = AudioSegment.from_file(values[0], format="wav")
    time = base_sound.duration_seconds

    base_sound2 = AudioSegment.from_file(values[1], format="wav")
    time2 = base_sound2.duration_seconds

    if time>=60 and time2>=60:
        speed = time/60
        speed2 = time2/60

        print("原曲は加速する.....")
        base_sound = base_sound.speedup(playback_speed=speed, crossfade=0)
        print("比較は加速する.....")
        base_sound2 = base_sound2.speedup(playback_speed=speed2, crossfade=0)

    base_sound.export("one.wav", format="wav")
    base_sound2.export("two.wav", format="wav")

def wavcomp():

    # 特徴量の種類
    class Feature_Types(Enum):
        SPECTRUM = 1
        SPECTRUM_CENTROID = 2
        MFCC = 3

    # 使用する特徴量の種類
    feature_type = Feature_Types.SPECTRUM_CENTROID
    # feature_type = Feature_Types.MFCC

    # 処理時間計測開始
    start = time.time()

    # (1) wavファイル読み込み
    print("#1 [Wav files read]")

    path_list=[]
    path_list.append("one.wav")
    path_list.append("two.wav")

    # 各wavファイルの振幅データ列とサンプリング周波数を取得し、リストに格納
    x_and_fs_list = []
    for path in path_list:
        x, fs = librosa.load(path, getSamplingFrequency(path))
        x_and_fs_list.append((x, fs))
        print(path+" サンプリング周波数 "+str(getSamplingFrequency(path))+"Hz")

    # 読み込んだwavファイルのパスを一覧表示
    print("> | {} : {}".format("Index", "Path"))
    for index in range(len(path_list)):
        print("> | {} : {}".format(index + 1, path_list[index]))

    print("")

    # (2) 特徴抽出
    print("#2 [Feature extraction]")

    # 使用する特徴量を表示
    print("> Selected feature type : {}".format(feature_type.name))

    # 使用する特徴量を抽出し、リストに格納
    feature_list = []
    for x_and_fs in x_and_fs_list:
        x = x_and_fs[0]
        fs = x_and_fs[1]
        if feature_type == Feature_Types.SPECTRUM:
            feature = np.abs(librosa.stft(x))
        elif feature_type == Feature_Types.SPECTRUM_CENTROID:
            feature = librosa.feature.spectral_centroid(x, fs)
        elif feature_type == Feature_Types.MFCC:
            feature = librosa.feature.mfcc(x, fs)
        feature_list.append(feature)

    del x_and_fs_list
    gc.collect()

    print("")

    # (3) 類似度計算
    print("#3 [Evaluation]")

    # 比較の基準とする特徴量
    reference_index = 0
    reference_feature = feature_list[reference_index]
    print("> Reference : {} ({})".format(reference_index + 1, path_list[reference_index]))

    del path_list
    gc.collect()

    # 類似度を計算し、リストに格納
    eval_list = []
    for target_feature in feature_list[1::2]:
        ac, wp = librosa.sequence.dtw(reference_feature, target_feature)
        # -1で一番最後の要素を取得
        eval = 1 - (ac[-1][-1] / np.array(ac).max())
        eval_list.append(eval)

    # 類似度を一覧表示
    print("> | {} , {} : {}".format("Reference", "Target", "Score"))
    for target_index in range(len(eval_list)):
        eval = eval_list[target_index]
        print("> | {} , {} : {}".format(reference_index + 1, target_index + 1, round(eval, 4)))

    print("")

    # 処理時間計測終了
    end = time.time()
    # 処理時間表示
    print("Total elapsed time : {}[sec]".format(round(end - start, 4)))
    return eval*100

def getSamplingFrequency(path):
    wr = wave.open(path, "r")
    fs = wr.getframerate()
    wr.close()
    return fs

def wavmain():
    onewav()
    eval=wavcomp()
    return round(eval, 4)

if __name__ == "__main__":
    wavmain()
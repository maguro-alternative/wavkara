import PySimpleGUI as sg

"""filename,neme = sg.popup_get_file('処理したいファイルを入力してください')
sg.popup('入力した', filename)"""
layout = [
   [sg.Text("wavファイル1"), sg.InputText(), sg.FileBrowse(key="file1")],
   [sg.Text("wavファイル2"), sg.InputText(), sg.FileBrowse(key="file2")],
   [sg.Submit(), sg.Cancel()],
]

window = sg.Window("ファイル選択", layout)

event, values = window.read()
print(event)
print(type(values))
for v in range(2):
    print(values[v])
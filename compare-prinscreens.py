import pyautogui
import tkinter as tk
from io import BytesIO
import win32clipboard
from PIL import ImageGrab
from functools import partial

import winsound
import time

# Necessário se você estiver usando múltiplas telas
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Tocar um som. '440' é o LA, 
# e o segundo parâmetro são os milissegundos de som
def playSound(so='win'):
    if so == 'win':
        winsound.Beep(440, 200)

# Usado para mandar algo para a área de transferência (ctrl-C)
# Chamada: send_to_clipboard(win32clipboard.CF_DIB, data)    
def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def acha_mouse():
    print(pyautogui.position())

# Pegando o screenshot. Customize a região.
# Para determinar a região use a função acha_mouse
def takeScreenshot(ini_x=1400, ini_y=190, tam_x=1300, tam_y=730):    
    myScreenshot = pyautogui.screenshot(region=(ini_x, ini_y, tam_x, tam_y))
    output = BytesIO()
    myScreenshot.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    return data    
    
# determina se uma imagem é diferente da outra
# através de um método 'preguiçoso': compara distância byte a byte do bitmap
def ruido(old, mudanca_byte=10, perc_diferenca=0.08):
    lenold = len(old)
    # print('o tamanho das imagens é: ' + str(lenold))
    new = takeScreenshot()
    contador = 0
    for n in range(lenold):
        if abs(old[n] - new[n]) > mudanca_byte:
            contador += 1
    # print('o ruído para limite ' + str(limite) + ' é de : ' + str(round(contador/lenold, 2)))
    if contador/lenold > perc_diferenca:
        send_to_clipboard(win32clipboard.CF_DIB, new)
        print('-- É um novo slide. Cole agora !')
        playSound(so='win')
        return new
    else:
        print('A taxa de mudança é de ' + str(round(contador/lenold, 2)))
        return old 

# código principal, loop infinito executado a cada 5s
old = takeScreenshot()
send_to_clipboard(win32clipboard.CF_DIB, old)
playSound(so='win')
print('-- inicio --') 
while True:
    time.sleep(5)
    old = ruido(old, mudanca_byte=10)





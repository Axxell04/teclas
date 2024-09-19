from pynput import mouse
import win32gui

def on_click(x, y, button, pressed):
    if button == mouse.Button.middle and pressed:
        #print("Clic con la rueda del ratón detectado")
        hwnd = win32gui.GetForegroundWindow()
        print(hwnd)
        
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

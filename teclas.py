from kivy.config import Config
Config.set('graphics', 'resizable', False)


from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFlatButton

import win32gui
import win32con
import win32api
import pyautogui

from pynput import mouse

from threading import Thread
import time

## Establecer el programa encima de todo
def set_super(hwnd: int):
    time.sleep(1)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 300, 200, 0)

class App(MDApp):
    btn_color = [0, 0, 0, .1]
    
    def build(self):
        self.HWND = win32gui.GetForegroundWindow()
        self.TARGET_HWND = 0
        #print(self.HWND)
        win32gui.SetWindowPos(self.HWND, win32con.HWND_TOPMOST, 100, 100, 300, 200, 0)
        
        thread_set_super = Thread(target=set_super, args=(self.HWND,), daemon=True)
        thread_set_super.start()
        
        self.start_listener()
        
        ## WINDOW
        self.title = "Teclas"
        self.theme_cls.theme_style = "Dark"
        
        ## SCREEN
        self.screen = MDScreen()


        ## GRID
        self.container_grid = MDGridLayout()
        self.container_grid.cols = 3
        self.container_grid.adaptive_height = True
        self.container_grid.adaptive_size = True
        self.container_grid.adaptive_width = True
        
        ## BUTTON SELECTED
        self.btn_selected = None
        
        ## BUTTON ESC
        self.btn_esc = MDFlatButton()
        self.btn_esc.text = "Esc"
        self.btn_esc.on_release = self.on_press_esc
        self.btn_esc.md_bg_color = self.btn_color


        ## BUTTON CTRL
        self.btn_ctrl = MDFlatButton()
        self.btn_ctrl.text = "Ctrl"
        self.btn_ctrl.on_release = self.on_press_ctrl
        self.btn_ctrl.md_bg_color = self.btn_color
        
        ## BUTTON WIN
        self.btn_win = MDFlatButton()
        self.btn_win.text = "Win"
        self.btn_win.on_release = self.on_press_win
        self.btn_win.md_bg_color = self.btn_color
        
        
        
        ## LISTA DE BOTONES
        
        self.list_btns = [
            self.btn_esc,
            self.btn_ctrl,
            self.btn_win
        ]
         
        ## AÑADIENDO LOS BOTONES
        self.add_widgets(self.container_grid, self.list_btns)

        self.ajust_window_size()
        
        ## AÑADIENDO EL CONTENIDO        
        self.screen.add_widget(self.container_grid)
        
        return self.screen
    
    def add_widgets(self, parent, childrens):
        for children in childrens:
            parent.add_widget(children)
    
    def ajust_window_size(self):
        ## RECALCULANDO LAS MEDIDAS DEL COMPONENTE
        self.container_grid.do_layout()
        width, height = self.container_grid.size
        Window.size = (width, height)
        
    ## FUNCIONES DE LOS BOTONES 
    def on_press_esc(self):
        self.update_btn_selected(self.btn_esc)
        
    def on_press_ctrl(self):
        self.update_btn_selected(self.btn_ctrl)
        
    def on_press_win(self):
        self.update_btn_selected(self.btn_win)
        
    ## Actualiza el botón seleccionado
    def update_btn_selected(self, btn):
        for b in self.list_btns:
            b.md_bg_color = [0, 0, 0, .1]
        
        self.btn_selected = btn
        self.btn_color = [0, 0, 1, 1]
        btn.md_bg_color = self.btn_color

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.middle:
            if pressed:
                if self.btn_selected == self.btn_ctrl:
                    pyautogui.keyDown("ctrl")
                elif self.btn_selected == self.btn_esc:
                    pyautogui.keyDown("esc")
                elif self.btn_selected == self.btn_win:
                    pyautogui.keyDown("win")
            else:
                if self.btn_selected == self.btn_ctrl:
                    pyautogui.keyUp("ctrl")
                elif self.btn_selected == self.btn_esc:
                    pyautogui.keyUp("esc")
                elif self.btn_selected == self.btn_win:
                    pyautogui.keyUp("win")
                               
    def set_listener(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
    
    def start_listener(self):
        thread = Thread(target=self.set_listener, daemon=True)
        thread.start()        
        


try:
    App().run()
except:
    pass

##PREVENCIÓN DE ERRORES
pyautogui.keyUp("ctrl")
pyautogui.keyUp("esc")
pyautogui.keyUp("win")
import tkinter as tk
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import time
import threading

# import autoclicker as ac

DEFAULT_START_MACRO : str = "z"
DEFAULT_STOP_MACRO  : str = "x"
DEFAULT_DELAY       : str = "0.1"

class AutoClicker(threading.Thread):
    def __init__(self, mouse : Controller, delay, button):
        self.delay = delay
        self.button = button
        self.clicking = False
        self.active = True
        self.mouse = mouse
    
    def start_click(self):
        self.pressed = True
    
    def stop_click(self):
        self.pressed = False
    
    def exit(self):
        self.stop_click()
        self.active = False
    
    def run(self):
        while self.active:
            while self.pressed:
                self.mouse.click(self.button)
                time.sleep(self.delay)

class App(tk.Tk):
    def __init__(self):
        self.root             : tk.Tk            = tk.Tk()
        self.mouse            : Controller       = Controller()
        self.active           : bool             = False
        self.clicking         : bool             = True
        self.clicking_thread  : threading.Thread = threading.Thread(target=self.autoclicker)
        self.listening_thread : threading.Thread = threading.Thread(target=self.open_listening)
        self.start_macro      : KeyCode
        self.stop_macro       : KeyCode
        self.listener         : Listener

        # Start/Stop Macro Input Columns
        for i in range(4):
            self.root.columnconfigure(index = i, weight = 1)
        # Delay Column
        self.root.columnconfigure(index = 2, weight = 3)

        for i in range(2):
            self.root.rowconfigure(index=i, weight=1)

        self.start_label : tk.Label = tk.Label(self.root, text = "Start Key:")
        self.start_macro_var : tk.StringVar = tk.StringVar(self.root, value=DEFAULT_START_MACRO)
        self.start_macro_entry : tk.Entry = tk.Entry(self.root, textvariable=self.start_macro_var)
        self.stop_label : tk.Label = tk.Label(self.root, text = "Stop Key:")
        self.stop_macro_var : tk.StringVar = tk.StringVar(self.root, value=DEFAULT_STOP_MACRO)
        self.stop_macro_entry : tk.Entry = tk.Entry(self.root, textvariable=self.stop_macro_var)

        self.delay_label : tk.Label = tk.Label(self.root, text="Delay:")
        self.delay_label.grid(column=0, row=1)
        self.delay_var : tk.StringVar = tk.StringVar(self.root, value=DEFAULT_DELAY)
        self.delay_entry : tk.Entry = tk.Entry(self.root, textvariable=self.delay_var)
        self.delay_entry.grid(column=1, row=1)

        self.active_label : tk.Label = tk.Label(self.root, text="Active:")
        self.active_label.grid(column=2, row=1, sticky="E")
        self.active_var : tk.BooleanVar = tk.BooleanVar(self.root, self.active)
        self.active_box : tk.Checkbutton = tk.Checkbutton(self.root, variable=self.active_var, command=self.toggle_autoclicker)
        self.active_box.grid(column=3, row=1)

        for i, widget in enumerate([self.start_label, self.start_macro_entry, self.stop_label, self.stop_macro_entry]):
            widget.grid(column = i, row = 0)

        self.update_title()
        self.root.mainloop()
    
    def update_title(self) -> None:
        if self.active_var.get():
            self.root.title("AutoClicker (ACTIVE)")
        else:
            self.root.title("AutoClicker (INACTIVE)")
    
    def autoclicker(self):
        try:
            delay : float = float(self.delay_var.get())
            while self.clicking:
                self.mouse.click(Button.left)
                time.sleep(delay)
        except:
            self.safe_close()
            self.root.destroy()
    
    def toggle_autoclicker(self) -> None:
        if self.active_var.get() == True:
            self.activate()
        else:
            self.deactivate()

    def activate(self) -> None:
        self.listening = True
        self.update_title()
        for entry in (self.start_macro_entry, self.stop_macro_entry, self.delay_entry):
            entry.config(state="disabled")
        self.start_macro = KeyCode(char=self.start_macro_entry.get())
        self.stop_macro = KeyCode(char=self.stop_macro_entry.get())
        print("Listening thread started.")
        self.listening_thread.start()
    
    def deactivate(self) -> None:
        self.listening = False
        self.update_title()
        for entry in (self.start_macro_entry, self.stop_macro_entry, self.delay_entry):
            entry.config(state="normal")
        if self.listener:
            self.listener.stop()
            self.listening_thread.join()
            print("Listening thread terminated.")
            self.listening_thread = threading.Thread(target=self.open_listening)
    
    def start_clicking(self) -> None:
        self.clicking = True
        self.clicking_thread = threading.Thread(target=self.autoclicker)
        print("AutoClicking active!")
        self.clicking_thread.start()
    
    def stop_clicking(self) -> None:
        self.clicking = False
        print("AutoClicking inactive!")
        self.clicking_thread.join()
    
    def toggle_event(self, key) -> None:
        if key == self.start_macro:
            self.clicking = True
            self.start_clicking()
            print("Clicking initiated.")
        elif key == self.stop_macro:
            self.clicking = False
            self.stop_clicking()
            print("Clicking ended.")
    
    def open_listening(self) -> None:
        print("Listening for inputs.")
        with Listener(on_press=self.toggle_event) as listener:
            self.listener = listener
            listener.join()
        print("Stopped listening for inputs.")
    
    def safe_close(self) -> None:
        print("Initiating safe close...")
        if self.clicking_thread.is_alive():
            print("Clicking thread active, stopping...")
            self.clicking = False
            self.clicking_thread.join()
            print("Clicking thread stopped!")
        if self.listening_thread.is_alive():
            print("Listening thread active, stopping...")
            self.listener.stop()
            self.listening_thread.join()
            print("Listening thread stopped!")
        print("Safe close was successful. Thank you for using this software!")

if __name__ == "__main__":
    window : App = App()
    window.safe_close()
    pass
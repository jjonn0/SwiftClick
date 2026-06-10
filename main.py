from autoclicker import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from pynput.keyboard import Listener, KeyCode

DEFAULT_START_MACRO : str   = "z"
DEFAULT_STOP_MACRO  : str   = "x"
DEFAULT_DELAY       : float = 0.1

class DebugConsole(ScrolledText):
    def __init__(self, master):
        super().__init__(master)
        self.current_index = 1
    
    def ping(self, message : str, sender) -> None:
        self.insert(
            index=f"{self.current_index}.0",
            chars=f"[{sender}]: {message}"
            )
        self.current_index += 1

class KeybindFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.start_key_var   : tk.StringVar = tk.StringVar(self, value=DEFAULT_START_MACRO)
        self.stop_key_var    : tk.StringVar = tk.StringVar(self, value=DEFAULT_STOP_MACRO)
        self.toggle_mode_var : tk.BooleanVar = tk.BooleanVar(self, value=False)

        self.start_key_label   : tk.Label = tk.Label(self, text="Start Key")
        self.stop_key_label    : tk.Label = tk.Label(self, text="Stop Key")
        self.toggle_mode_label : tk.Label = tk.Label(self, text="Toggle Mode")

        self.start_key_entry : tk.Entry = tk.Entry(self, textvariable=self.start_key_var, width=5)
        self.stop_key_entry  : tk.Entry = tk.Entry(self, textvariable=self.stop_key_var, width=5)
        self.toggle_mode_box : tk.Checkbutton = tk.Checkbutton(self, variable=self.toggle_mode_var, command=self.update_visual)

        self.toggle_mode_off : list[list[tk.Widget]] = [[self.start_key_label, self.start_key_entry], [self.stop_key_label, self.stop_key_entry], [self.toggle_mode_label, self.toggle_mode_box]]
        self.toggle_mode_on  : list[list[tk.Widget]] = [[self.start_key_label, self.start_key_entry], [self.toggle_mode_label, self.toggle_mode_box]]
        self.disable_list : list = [self.start_key_entry, self.stop_key_entry, self.toggle_mode_box]

        self.update_visual()
    
    def update_visual(self) -> None:
        display_list : list[list[tk.Widget]] = []
        remove_list  : list[list[tk.Widget]] = []
        if self.toggle_mode_var.get():
            display_list = self.toggle_mode_on
            remove_list = self.toggle_mode_off
            self.start_key_label.config(text="Toggle Key")
        else:
            display_list = self.toggle_mode_off
            remove_list = self.toggle_mode_on
            self.start_key_label.config(text="Start Key")
        for group in remove_list:
            for widget in group:
                widget.grid_forget()
        
        for a, group in enumerate(display_list):
            self.rowconfigure(index=a, weight=1)
            for b, widget in enumerate(group):
                self.columnconfigure(index=b, weight=1)
                widget.grid(row=a, column=b, sticky="e")

    def get_start_key(self) -> str:
        return self.start_key_var.get()
    def get_stop_key(self) -> str:
        if self.toggle_mode_var.get():
            return self.start_key_var.get()
        else:
            return self.stop_key_var.get()
    def get_toggle_value(self) -> bool:
        return self.toggle_mode_var.get()

    def disable(self) -> None:
        for widget in self.disable_list:
            widget.config(state="disabled")
    
    def enable(self) -> None:
        for widget in self.disable_list:
            widget.config(state="normal")

class DelayFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.delay_var : tk.DoubleVar = tk.DoubleVar(self, value=DEFAULT_DELAY)

        self.delay_label : tk.Label = tk.Label(self, text="Delay")
        self.delay_entry : tk.Entry = tk.Entry(self, textvariable=self.delay_var)

        for a, group in enumerate([
            [self.delay_label, self.delay_entry]
        ]):
            self.rowconfigure(index=a, weight=1)
            for b, widget in enumerate(group):
                self.columnconfigure(index=b, weight=1)
                widget.grid(column=b, row=a)
        
        self.disable_list : list = [self.delay_entry]
    
    def get_delay_value(self) -> float:
        return self.delay_var.get()

    def disable(self) -> None:
        for widget in self.disable_list:
            widget.config(state="disabled")
    
    def enable(self) -> None:
        for widget in self.disable_list:
            widget.config(state="normal")

class ButtonFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.button_var : tk.StringVar = tk.StringVar(self, "Left")
        self.buttons_strings = ("Left", "Middle", "Right")

        self.press_var : tk.StringVar = tk.StringVar(self, "Press")
        self.press_strings = ("Press", "Hold Release", "Hold")

        self.button_label : tk.Label = tk.Label(self, text="Mouse Button:")
        self.button_options : tk.OptionMenu = tk.OptionMenu(self, self.button_var, self.buttons_strings[0], *self.buttons_strings[1:3])

        self.press_label : tk.Label = tk.Label(self, text="Press Mode:")
        self.press_options : tk.OptionMenu = tk.OptionMenu(self, self.press_var, self.press_strings[0], *self.press_strings[1:3])

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=2, minsize=90.0)

        self.button_label.grid(column=0, row=0, padx=5.0, sticky="E")
        self.button_options.grid(column=1, row=0, sticky="WE")

        self.press_label.grid(column=0, row=1, sticky="E")
        self.press_options.grid(column=1, row=1, sticky="WE")

        self.disable_list : list = [self.button_options, self.press_options]

        # for a, group in enumerate([
        #     [self.button_label, self.button_options]
        # ]):
        #     self.rowconfigure(index=a, weight=1)
        #     for b, widget in enumerate(group):
        #         self.columnconfigure(index=b, weight=1)
        #         widget.grid(column=b, row=a)
    
    def get_button_value(self) -> str:
        return self.button_var.get()

    def get_press_mode(self) -> str:
        return self.press_var.get()

    def disable(self) -> None:
        for widget in self.disable_list:
            widget.config(state="disabled")
    
    def enable(self) -> None:
        for widget in self.disable_list:
            widget.config(state="normal")

class ActivationFrame(tk.Frame):
    def __init__(self, master, method_call):
        super().__init__(master)

        self.active_var : tk.BooleanVar = tk.BooleanVar(self, value = False)

        self.active_label : tk.Label = tk.Label(self, text="Active")
        self.active_box : tk.Checkbutton = tk.Checkbutton(self, variable=self.active_var, command=method_call)

        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=2)

        self.active_label.grid(column=0, row=0)
        self.active_box.grid(column=1, row=0)
    
    def get_active_value(self) -> bool:
        return self.active_var.get()

class App(tk.Tk):
    def __init__(self):
        self.root      : tk.Tk   = tk.Tk()
        self.listening : bool    = False
        self.active    : bool    = False
        self.start_key : KeyCode
        self.stop_key  : KeyCode
        self.autoclicker : MacroRunner = MacroRunner((Macro(ActionType.SINGLE_PRESS, Button.left, 0.1),))
        self.listener : Listener = Listener()

        self.root.title("SwiftClick v.0.2")
        self.root.resizable(False, False)

        self.keybind_frame : KeybindFrame    = KeybindFrame(self.root)
        self.delay_frame   : DelayFrame      = DelayFrame(self.root)
        self.button_frame  : ButtonFrame     = ButtonFrame(self.root)
        self.active_frame  : ActivationFrame = ActivationFrame(self.root, self.toggle_state)
        
        for a, group in enumerate([
            [self.keybind_frame, self.delay_frame],
            [self.button_frame, self.active_frame]
        ]):
            for b, widget in enumerate(group):
                widget.grid(column=b, row=a, padx=15.0)

        self.root.mainloop()
    
    def toggle_state(self) -> None:
        if self.listening:
            self.listening = False
            self.keybind_frame.enable()
            self.delay_frame.enable()
            self.button_frame.enable()

            if self.listener.is_alive():
                self.listener.stop()
        else:
            self.listening = True
            self.keybind_frame.disable()
            self.delay_frame.disable()
            self.button_frame.disable()

            self.listener_thread : Thread = Thread(target=self.begin_listening)
            self.listener_thread.start()
    
    def keypress_event(self, key) -> None:
        if (key == KeyCode(char=self.keybind_frame.get_start_key()) and not self.keybind_frame.get_toggle_value()) or (self.keybind_frame.get_toggle_value() and self.active == False):
            self.active = True
            button_value = self.button_frame.get_button_value()
            press_mode = self.button_frame.get_press_mode()
            key_type : Button
            macro_list : tuple

            if button_value == "Left":
                key_type = Button.left
            elif button_value == "Middle":
                key_type = Button.middle
            else:
                key_type = Button.right
            
            if press_mode == "Press":
                macro_list = (Macro(ActionType.SINGLE_PRESS, key_type, self.delay_frame.get_delay_value()),)
            elif press_mode == "Hold Release":
                macro_list = (Macro(ActionType.HOLD_PRESS, key_type, self.delay_frame.get_delay_value()), Macro(ActionType.RELEASE_PRESS, key_type, 0.1))
            else:
                macro_list = (Macro(ActionType.HOLD_PRESS, key_type, -1),)
            
            self.autoclicker = MacroRunner(macro_list)
            self.autoclicker.start()
        elif (key == KeyCode(char=self.keybind_frame.get_stop_key()) and not self.keybind_frame.get_toggle_value()) or (self.keybind_frame.get_toggle_value() and self.active == True):
            self.active = False
            self.autoclicker.stop()
    
    def begin_listening(self) -> None:
        print("Listener active...")
        with Listener(on_press=self.keypress_event) as listener:
            self.listener = listener
            listener.join()
        print("Listener inactive.")
    
    def safe_close(self) -> None:
        print("Initiating safe close...")
        if self.listener.is_alive():
                print("Listener thread is live, stopping...")
                self.listener.stop()
                self.listener.join()
                print("Listener thread stopped!")
        if self.autoclicker.running:
                print("Autoclicking thread is live, stopping...")
                self.autoclicker.stop()
                self.autoclicker.join()
                print("Autoclicker thread stopped!")
        print("Safe close finished! Thank you for using the software!")

if __name__ == "__main__":
    app = App()
    app.safe_close()
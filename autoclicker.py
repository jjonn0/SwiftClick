from threading import Thread
import time
from pynput.mouse import Button, Controller
from enum import Enum

MOUSE_BUTTONS : tuple = (Button.left, Button.middle, Button.right)

class ActionType(Enum):
    SINGLE_PRESS = 1
    HOLD_PRESS = 2
    RELEASE_PRESS = 3

class Macro():
    def __init__(self, action : ActionType, key : Button, sleep_time : float):
        self.action = action
        self.key = key
        self.sleep_time = sleep_time

class MacroRunner():
    ## Takes in an action tuple, where each entry is a dictionary that contains the "action" to perform on a "key", and a "delay" until the next action.
    def __init__(self, macro_list : tuple[Macro]):
        self._send_status_msg("Instantiating...")
        self.macro_list = macro_list
        self.mouse = Controller()
        self.running = False
        self.holding = False
        
        self._autoclicking_thread : Thread
        self._send_status_msg("Instantiation finished!")
    
    def _send_status_msg(self, message : str) -> None:
        print(f"[{self}]: {message}")
    
    def start(self) -> None:
        self._send_status_msg("Macro active.")
        self.running = True
        self._autoclicking_thread = Thread(target=self.script)
        self._autoclicking_thread.start()
    
    def stop(self) -> None:
        self._send_status_msg("Macro stopped.")
        self.running = False
        self._autoclicking_thread.join()
    
    def restart(self) -> None:
        self._send_status_msg("Restarting...")
        self.stop()
        self.start()
    
    def script(self) -> None:
        while self.running:
            for macro in self.macro_list:
                if macro.action == ActionType.SINGLE_PRESS:
                    self.mouse.click(macro.key)
                elif macro.action == ActionType.HOLD_PRESS and not self.holding:
                    self.mouse.press(macro.key)
                    self.holding = True
                elif macro.action == ActionType.RELEASE_PRESS:
                    self.mouse.release(macro.key)
                    self.holding = False
                if macro.sleep_time > 0.0:
                    time.sleep(macro.sleep_time)
        self.holding = False
    
    def join(self) -> None:
        self._autoclicking_thread.join()
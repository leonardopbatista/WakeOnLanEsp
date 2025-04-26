from threading import Thread
import tkinter as tk

def thread(func):
    def wrapper_func(*args, **kwargs):
        if not hasattr(args[0], '_busy'):
            args[0]._busy = False
        
        if args[0]._busy:
            return
        class Temp(Thread):
            def run(self):
                args[0]._busy = True
                try:
                    func(*args, **kwargs)
                finally:
                    args[0]._busy = False
        Temp().start()
    return wrapper_func

def center_window(window: tk.Tk | tk.Toplevel, offset_x: int = 0, offset_y: int = 0) -> None:
    window.update_idletasks()
    width = window.winfo_reqwidth()
    height = window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2) + offset_x
    y = (screen_height // 2) - (height // 2) + offset_y

    window.geometry(f"+{x}+{y}")
from tkinter import Misc
from tkinter.scrolledtext import ScrolledText

class HighLevelLog(ScrolledText):
    def __init__(self, master: Misc | None = None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.tag_config('orange', lmargin1=5, lmargin2=5, foreground='#ff8000')
        self.tag_config('red', lmargin1=5, lmargin2=5, foreground='#ff0000')
        self.tag_config('green', lmargin1=5, lmargin2=5, foreground='#00aa00')
        self.tag_config('gray', lmargin1=5, lmargin2=5, foreground='#888')
        self.tag_config('black', lmargin1=5, lmargin2=5, foreground='#000')
        self.fixed_warnings: list[tuple[str,str]] = []

        self.configure(background="#e0e0e0", borderwidth=2, height=6, highlightbackground="#aaaaaa", highlightcolor="#aaaaaa", 
                       highlightthickness=2, relief="flat", selectborderwidth=0, state="disabled", font=("Arial", 8))

    def add_fixed_warning(self, warning_message: str, format_color: str):
        self["state"] = "normal"
        self.insert(f"{len(self.fixed_warnings)+1}.0", warning_message+"\n", format_color)
        self.fixed_warnings.append((warning_message, format_color))
        self["state"] = "disabled"

    def _prepare_to_write(self, clean_old_log: bool):
        self["state"] = "normal"
        if clean_old_log: 
            self.delete(1.0, "end")
            self.write_list(self.fixed_warnings, False)
            self["state"] = "normal"
        elif self.get(1.0, "end") not in ["", "\n"]:
            self.insert("end", "\n")
    
    def clear(self):
        self["state"] = "normal"
        self.delete(1.0, "end")
        self.fixed_warnings = []
        self["state"] = "disabled"

    def write(self, message: str, format_color: str = "black", clean_old_log: bool = True):
        self._prepare_to_write(clean_old_log)
        self.insert("end", message, format_color)
        self.see("end")
        self["state"] = "disabled"

    def write_list(self, message_list: list[tuple[str,str]], clean_old_log: bool = True):
        self._prepare_to_write(clean_old_log)
            
        for message in message_list:
            self.insert("end", message[0]+"\n", message[1])
        
        self.see("end")
        self["state"] = "disabled"
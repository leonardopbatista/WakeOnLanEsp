import ctypes
import time
from tkinter import Button, Tk, Label

from custom_widgets.log import HighLevelLog
from utils.utils import resource_path
from utils.tkutils import thread, center_window

from core.listener import check_connection
from core.sender import send_wol_command

ctypes.windll.shcore.SetProcessDpiAwareness(2)

MQTT_BROKERS = ["mqtt.eclipseprojects.io", "broker.emqx.io", "broker.hivemq.com"]
TOPIC_COMMAND = "exampleWakeOnLan/wol"
TOPIC_PING = "exampleWakeOnLan/ping"
TOPIC_FEEDBACK = "exampleWakeOnLan/feedback"

class App(Tk):
    def __init__(self):
        super().__init__()
        self.start_ui()
        self.broker = None

    @thread
    def check_conection(self):
        self.log.write("-Verificando a conexão do ESP...", "gray")
        while not (broker := check_connection(MQTT_BROKERS, TOPIC_PING)):
            self.log.write("-ESP não está online! Verificando novamente em 5 segundos...", "red", False)
            time.sleep(5)
        self.log.write(f'-ESP está conectado no broker: "{broker}"!', "green")
        self.broker = broker
        self.wake_button["state"] = "normal"

    def start_ui(self):
        self.withdraw()
        self.title("WakeOnLan v1.0")
        self.wm_iconbitmap(resource_path("assets\\PC-Mini.ico"))

        Label(self, text='Log:').grid(row=0, column=0, padx="10 5", pady="10 0", sticky="w")
        self.log = HighLevelLog(self, width=53)
        self.log.grid(row=1, column=0, columnspan=5, ipady=0, padx=10, pady=5, sticky="e")

        self.wake_button = Button(self, text='Ligar PC', command=self.on_wake_button_click, state="disabled")
        self.wake_button.grid(row=2, column=2, columnspan=1, padx="0 15", pady="10 10")

        center_window(self, offset_y=-100)
        
        self.resizable(False, False)
        self.deiconify()

        self.check_conection()

    @thread
    def on_wake_button_click(self):
        self.log.write("-Enviando MagicPacket...", "gray")
        result = send_wol_command(self.broker, TOPIC_COMMAND, TOPIC_FEEDBACK)

        if result == True:
            self.log.write("-MagicPacket enviado com sucesso!", "green")
        else:
            self.log.write("-Falha ao enviar o MagicPacket!", "red")

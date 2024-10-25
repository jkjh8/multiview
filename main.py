import sys, vlc, threading
from PySide6 import QtWidgets
from socket_server import TCPServer

from player import Player

def tcp_callback(data):
    try:
        data = data.decode("utf-8")
        key, value = data.split(" ")
        if key == "play":
            if not value:
                value = 0
            player.play(int(value))
        elif key == "stop":
            if not value:
                value = 0
            player.stop(int(value))
        elif key == "fullscreen":
            if not value:
                value = True
            player.set_fullscreen(value)
        elif key == "layout":
            if value == "9":
                player.set_layout_9()
            elif value == "4":
                player.set_layout_4()
            
    except Exception as e:
        print(e)        

if __name__ == "__main__":
    # tcp server
    tcp_server = TCPServer("", 20004, tcp_callback)
    server = threading.Thread(target=tcp_server.start).start()
    # ui
    app = QtWidgets.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    player.set_layout_9()
    player.play(0)
    sys.exit(app.exec_())

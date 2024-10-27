import sys, vlc, threading
from PySide6 import QtWidgets
from socket_server import TCPServer
from db import Database

from player import Player

port = 20004

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
    # db
    db = Database("player.db")
    doc = db.view()
    if not doc:
        db.insert("layout", 9)
        db.insert("fullscreen", True)
        db.insert("port", port)
    else:
        for row in doc:
            if row["key"] == "port":
                port = row["value"]
    # tcp server
    tcp_server = TCPServer("", port, tcp_callback)
    server = threading.Thread(target=tcp_server.start)
    server.daemon = True
    server.start()
    # ui
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    player = Player()
    player.show()
    player.resize(640, 480)
    player.set_layout_9()
    player.play(0)
    sys.exit(app.exec())

import platform
import os
import sys

from PySide6 import QtWidgets, QtGui, QtCore
import vlc

class Player(QtWidgets.QMainWindow):
    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle("Multiview")

        # Create a basic vlc instance
        self.instances = [vlc.Instance() for _ in range(9)]
        # Create an empty vlc media player
        self.mediaplayers = [instance.media_player_new() for instance in self.instances]
        # fullscreen
        self.is_fullscreen = False

        self.create_ui()

    def create_ui(self):
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        # frames to display
        self.videoframes = [QtWidgets.QFrame() for _ in range(9)]
        self.palettes = [frame.palette() for frame in self.videoframes]
        for i, palette in enumerate(self.palettes):
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
            self.videoframes[i].setPalette(palette)
            self.videoframes[i].setAutoFillBackground(True)
        # player에 할당
        for i in range(9):
            self.mediaplayers[i].set_hwnd(self.videoframes[i].winId())
            self.mediaplayers[i].set_mrl("rtp://@239.12.12.12:5004")
            
        # layouts
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.hboxlayouts = [QtWidgets.QHBoxLayout() for _ in range(3)]
        self.setContentsMargins(1,1,1,1)
        self.vboxlayout.setSpacing(1)
        
        self.widget.setLayout(self.vboxlayout)

        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        # Add actions to file menu
        open_action = QtGui.QAction("Set 4 view", self)
        close_action = QtGui.QAction("Set 9 view", self)
        play_action = QtGui.QAction("Play", self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(play_action)

        open_action.triggered.connect(self.set_layout_4)
        close_action.triggered.connect(self.set_layout_9)
        play_action.triggered.connect(self.play)
    
    def play(self):
        for mediaplayer in self.mediaplayers:
            mediaplayer.play()

    def set_layout_9(self):
        self.clear_layouts()
        for i in range(3):
            for j in range(3):
                self.hboxlayouts[i].addWidget(self.videoframes[i * 3 + j])
        
        for hbox in self.hboxlayouts:
            self.vboxlayout.addLayout(hbox)
            hbox.setSpacing(1)
        print("Set layout 9")

    def set_layout_4(self):
        self.clear_layouts()
        for i in range(2):
            for j in range(2):
                self.hboxlayouts[i].addWidget(self.videoframes[i * 2 + j])
        
        for hbox in self.hboxlayouts:
            self.vboxlayout.addLayout(hbox)
            hbox.setSpacing(1)
        print("Set layout 4")
        
    def clear_layouts(self):
        for hbox in self.hboxlayouts:
            for i in reversed(range(hbox.count())):
                widget = hbox.itemAt(i).widget()
                hbox.removeWidget(widget)
                widget.setParent(None)
        print("Cleared layouts")
    

def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    player.set_layout_9()
    # devices = player.get_devices()
    # player.mediaplayer.audio_output_device_set(devices[1]["device"], devices[1]["description"])
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
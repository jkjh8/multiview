import sys, vlc
from PySide6 import QtWidgets, QtGui, QtCore

class Player(QtWidgets.QMainWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.setWindowTitle("Multiview")

        # Create a basic vlc instance and media players
        self.instances = [vlc.Instance() for _ in range(9)]
        self.mediaplayers = [instance.media_player_new() for instance in self.instances]
        
        self.is_fullscreen = False
        self.show_mode = 9

        self.create_ui()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape and self.is_fullscreen:
            self.set_fullscreen()
        elif event.key() == QtCore.Qt.Key_F11:
            self.set_fullscreen()
        elif event.key() == QtCore.Qt.Key_Control and event.key() == QtCore.Qt.Key_F4:
            self.close()

    def create_ui(self):
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        
        # Create video frames and set their palettes
        self.videoframes = [self.create_video_frame() for _ in range(9)]
        
        # Assign media players to frames
        for i, player in enumerate(self.mediaplayers):
            player.set_hwnd(self.videoframes[i].winId())
            player.set_mrl("udp://@239.12.12.12:5004")
            
        # Layouts
        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.hboxlayouts = [QtWidgets.QHBoxLayout() for _ in range(3)]
        self.setContentsMargins(1, 1, 1, 1)
        self.vboxlayout.setSpacing(1)
        self.widget.setLayout(self.vboxlayout)

        self.menu_bar = self.menuBar()
        self.create_menu()

    def create_video_frame(self):
        frame = QtWidgets.QFrame()
        palette = frame.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        frame.setPalette(palette)
        frame.setAutoFillBackground(True)
        return frame

    def create_menu(self):
        file_menu = self.menu_bar.addMenu("File")

        actions = [
            ("Set 4 view", self.set_layout_4),
            ("Set 9 view", self.set_layout_9),
            ("Play", self.play),
            ("Full Screen", self.set_fullscreen, "F11"),
            ("Quit", self.close, "Ctrl+F4")
        ]

        for name, method, *shortcut in actions:
            action = QtGui.QAction(name, self)
            if shortcut:
                action.setShortcut(shortcut[0])
            action.triggered.connect(method)
            file_menu.addAction(action)

    def play(self, num=0):
        try:
            if num == 0 :
                for player in self.mediaplayers:
                    player.play()
            else:
                self.mediaplayers[num-1].play()
        except Exception as e:
            print(e)
    
    def stop(self, num=0):
        try:
            if num == 0 :
                for player in self.mediaplayers:
                    player.stop()
            else:
                self.mediaplayers[num-1].stop()
        except Exception as e:
            print(e)
            
    
    def set_fullscreen(self, value=None):
        try:
            if value is not None:
                if self.is_fullscreen:
                    self.showNormal()
                    self.menu_bar.show()
                else:
                    self.showFullScreen()
                    self.menu_bar.hide()
                self.is_fullscreen = not self.is_fullscreen
            else:
                if value == True or value == 'true' or value == 1:
                    self.showFullScreen()
                    self.menu_bar.hide()
                    self.is_fullscreen = True
                else:
                    self.showNormal()
                    self.menu_bar.show()
                    self.is_fullscreen = False
        except Exception as e:
            print(e)

    def set_layout_9(self):
        self.set_layout(3, 3)
        print("Set layout 9")

    def set_layout_4(self):
        self.set_layout(2, 2)
        print("Set layout 4")
        
    def set_layout(self, rows, cols):
        self.clear_layouts()
        for i in range(rows):
            for j in range(cols):
                self.hboxlayouts[i].addWidget(self.videoframes[i * cols + j])
        
        for hbox in self.hboxlayouts:
            self.vboxlayout.addLayout(hbox)
            hbox.setSpacing(1)

    def clear_layouts(self):
        for hbox in self.hboxlayouts:
            while hbox.count():
                widget = hbox.takeAt(0).widget()
                if widget:
                    widget.setParent(None)
        print("Cleared layouts")


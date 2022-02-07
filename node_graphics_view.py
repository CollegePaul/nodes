from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)


    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self,event):#
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(),event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        #simulate pressing the left mouse button for the dragging
        fakeEvent = QMouseEvent(event.type(),event.localPos(),event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self,event):
        fakeEvent = QMouseEvent(event.type(),event.localPos(),event.screenPos(),
                                Qt.LeftButton, event.buttons() & -Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)
    
#https://www.youtube.com/watch?v=5IKOIOg76so&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=5
#11.03
from decimal import Clamped
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_socket import QDMGraphicsSocket

MODE_NOOP = 1   
MODE_EDGE_DRAG  = 2

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoom = 10
        self.zoomClamp = True
        self.zoomStep = 1
        self.zoomRange = [0,14]


    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
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


    def leftMouseButtonPress(self,event):
        

        item = self.getItemAtClick(event)
        
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                print("Start Dragging Edge")
                print("  assign start socket")
                return
        
        if self.mode == MODE_EDGE_DRAG:
            self.mode = MODE_NOOP
            print("End Dragging edge")

            if type(item) is QDMGraphicsSocket:
                print("  assign End Socket")
                return

        #this will pass the event higher up to the node,and allow the whole node to move
        super().mousePressEvent(event)
    
    def leftMouseButtonRelease(self,event):
        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self,event):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self,event):
        super().mouseReleaseEvent(event)

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def wheelEvent(self, event) :
        #calculate zoom factor
        zoomOutFactor = 1  / self.zoomInFactor
      

        #calculate the zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True
        
        #set the sceen scale
        if not clamped or self.zoom is False:
            self.scale(zoomFactor, zoomFactor)

   
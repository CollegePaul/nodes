from decimal import Clamped
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_graphics_edge import QDMGraphicsEdge

from node_graphics_socket import QDMGraphicsSocket
from node_edge import Edge, EDGE_TYPE_BEZIER

MODE_NOOP = 1   
MODE_EDGE_DRAG  = 2

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True

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

        self.last_lmb_click_scene_pop = self.mapToScene(event.pos())
        
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
        
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return


        #this will pass the event higher up to the node,and allow the whole node to move
        super().mousePressEvent(event)


    def leftMouseButtonRelease(self,event):
        #get item clicked on
        item = self.getItemAtClick(event)

        #
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self,event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)
        if DEBUG:
            if isinstance(item, QDMGraphicsEdge): print("RMB DEBUG:", item.edge, "connecting sockets:",
                                                        item.edge.start_socket, "<-->", item.edge.end_socket )
            if type(item) is QDMGraphicsSocket: print("RMB DEBUG:", item.socket, "has Edge:", item.socket.edge)
            if item is None:
                print("SCENE:")
                print("  Nodes:")
                for node in self.grScene.scene.nodes: print("    ", node)
                print("  Edges:")
                for edge in self.grScene.scene.edges: print("    ", edge)

    def rightMouseButtonRelease(self,event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):

        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDest(pos.x(),pos.y())
            self.dragEdge.grEdge.update()
        
        super().mouseMoveEvent(event)

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self,item):
        if DEBUG: print("View::EdgeDragStart - Start Dragging Edge")
        if DEBUG: print("View::EdgeDragStart -   assign Start socket to:", item.socket)
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print("VIEW::EdgeDragStart - drag edge:", self.dragEdge   )
        
  
    def edgeDragEnd(self, item):
        #return true if the rest of the code is to be skipped
        self.mode = MODE_NOOP
        
        if type(item) is QDMGraphicsSocket:
            if DEBUG: print("View::edgeDragEnd -   assign End Socket")
            return True

        if DEBUG: print("View::edgeDragEnd - End Dragging edge")
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG: print("View::endDragEnd")

        return False

    def distanceBetweenClickAndReleaseIsOff(self, event):
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pop
        edge_draag_threshold_sq= EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y() ) >  edge_draag_threshold_sq
        

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

   
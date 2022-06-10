from math import dist
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent = None):
        super().__init__(parent)

        self.edge = edge
        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color) 
        self._pen_selected = QPen(self._color_selected) 
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen.setWidth(2.0)
        self._pen_selected.setWidth(2.0)
        self._pen_dragging.setWidth(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)  

        self.setZValue(-1.0)

        self.posSource = [0,0]
        self.posDestination = [200, 100] 
    
    def setSource(self, x, y):
        self.posSource = [x,y]
    
    def setDest(self, x, y):
        self.posDestination = [x, y]



    def paint(self, painter, QStyleOptionGraphicsItem, widgit = None):

        #calculate the path
        self.updatePath()

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)    
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        #will handel drawing QPainter path from point A to B

        #this class is a non specific implimentation of the edge
        #the types staight and bezier will be the implemted class
        #this is an abstract class that defines the must impliment methods.

        raise NotImplemented("This method has to be overriden in a child class")



#concrete classes

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0],self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)

class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]: dist *= -1

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + dist, s[1], d[0] - dist, d[1],            
            self.posDestination[0], self.posDestination[1])
        self.setPath(path)






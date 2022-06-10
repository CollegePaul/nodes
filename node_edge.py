from numpy import source
from node_graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False

class Edge():
    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.grEdge = QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)
        self.updatePositions()
        #print("Edge: ", self.grEdge.posSource, "to", self.grEdge.posDestination)

        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x() 
        source_pos[1] += self.start_socket.node.grNode.pos().y() 
        self.grEdge.setSource(*source_pos)
                                               

        #if creating an edge the end socket maybe empty at this time
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x() 
            end_pos[1] += self.end_socket.node.grNode.pos().y() 
            self.grEdge.setDest(*end_pos)
        else:
            self.grEdge.setDest(*source_pos)   

        #print("SS: ", self.start_socket)
        #print("ES: ", self.end_socket)
        self.grEdge.update()

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
    

    def remove_from_socket(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        
        if self.end_socket is not None:
            self.end_socket.edge = None

        self.end_socket = None
        self.start_socket = None

    def remove(self):
        if DEBUG: print(">  Removing Edge", self)
        if DEBUG: print(" - remove edge from all sockets.")
        self.remove_from_socket()
        if DEBUG: print(" - remove graphical edge")
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None

        if DEBUG: print(" - remove edge from scene")
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass
       

        if DEBUG: print(" - All done")


    
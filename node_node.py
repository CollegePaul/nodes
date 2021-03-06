from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *

DEBUG = False

class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]) -> None:
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget(self)
        self.grNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22
        
        #create the sockets for input and output
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index = counter, position = LEFT_BOTTOM, socket_type = item)
            counter += 1
            self.inputs.append(socket)  

        counter = 0     
        for item in outputs:
            socket = Socket(node=self, index = counter, position = RIGHT_TOP, socket_type= item)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
    
    @property   
    def pos(self):
        self.grNode.pos()


    def setPos(self,x,y):
        self.grNode.setPos(x,y)
    
    def getSocketPosition(self, index, position):
        x=0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.grNode.width

        if position in(LEFT_BOTTOM, RIGHT_BOTTOM):
            #Start from the bottom
            y= self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing 
        else:
            #start from the top
            y=self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing 
        return [x,y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                #print("Updating")
                socket.edge.updatePositions()

    def remove(self):
        if DEBUG: print("> Removing Node", self)
        if DEBUG: print(" - remove all edges from sockets", self)
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                if DEBUG: print("    - removing from socket:" , socket, "edge:", socket.edge)
                socket.edge.remove()
        if DEBUG: print(" - remove all grNode", self)
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        if DEBUG: print(" - remove node from the scene", self)
        self.scene.removeNode(self)
        if DEBUG: print(" - all done", self)    







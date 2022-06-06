from re import S
from node_graphics_socket import QDMGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

class Socket():
    def __init__(self, node, index = 0, position = LEFT_TOP):

        self.node = node
        self.index = index   
        self.position = position

        #print("Socket - Creating: " , self.index, self.position, "for node: ",self.node)

        self.grSocket = QDMGraphicsSocket(self.node.grNode)
        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None    
    
    def getSocketPosition(self):
        #print(" GSP: ", self.index, self.position, "node: ", self.node)
        res = self.node.getSocketPosition(self.index, self.position)
        #print(" RES: ", res)
        return res
    
    def setConnectedEdge(self, edge= None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None

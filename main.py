import sys
from PyQt5.QtWidgets import *

from node_editor_wnd import NodeEditorWnd


if __name__ == '__main__':
    app = QApplication(sys.argv) 

    wnd = NodeEditorWnd()

    sys.exit(app.exec_())
    

#11   16.28   mose realse on end socket

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):

        # Action to exit program
        exitAct = qtw.QAction(qtg.QIcon('exit.jpg'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qtw.qApp.quit)

        # Menu to Búsquedas ciegas: Anchura y profundidad
        algoritCat1 = qtw.QMenu('Búsquedas ciegas', self)

        anchuraAct = qtw.QAction(qtg.QIcon('code-icon.png'), '&Anchura', self)
        anchuraAct.triggered.connect(self.bdfInit)
        profundidadAct = qtw.QAction(qtg.QIcon('code-icon.png'), '&Profundidad', self)

        algoritCat1.addAction(anchuraAct)
        algoritCat1.addAction(profundidadAct)

        # Menu to Búsquedas informadas: Primero el mejor
        algoritCat2 = qtw.QMenu('Búsquedas informadas', self)

        primeroMejorAct = qtw.QAction(qtg.QIcon('code-icon.png'), '&Primero el mejor', self)
        algoritCat2.addAction(primeroMejorAct)

        # Búsquedas optimizadas: Costo Uniforme y A*.
        algoritCat3 = qtw.QMenu('Búsquedas optimizadas', self)

        costoUniformAct = qtw.QAction(qtg.QIcon('code-icon.png'), '&Costo uniforme', self)
        AestrellaAct = qtw.QAction(qtg.QIcon('code-icon.png'), '&A*', self)

        algoritCat3.addAction(costoUniformAct)
        algoritCat3.addAction(AestrellaAct)

        # Problemas con Satisfacción de Restricciones (PSR).
        algoritCat4 = qtw.QMenu('PSR', self)

        self.statusBar()

        menubar = self.menuBar()

        AlgoritmosMenu = menubar.addMenu('&Algoritmos')
        AlgoritmosMenu.addMenu(algoritCat1)
        AlgoritmosMenu.addMenu(algoritCat2)
        AlgoritmosMenu.addMenu(algoritCat3)
        AlgoritmosMenu.addMenu(algoritCat4)

        ExitMenu = menubar.addMenu('&Salir')
        ExitMenu.addAction(exitAct)

        # University logo / label
        labelLogo = qtw.QLabel(self)
        logoPixmap = qtg.QPixmap('arlogo.png')

        # University logo as centered widget
        labelLogo.setPixmap(logoPixmap)
        self.setCentralWidget(labelLogo)

        self.resize(logoPixmap.width(), logoPixmap.height())
        self.setWindowTitle('Algoritmos IA')    
        self.show()

    def bfs(self, graph, initial):
        visited = []
        
        queue = [initial]
    
        while queue:
            node = queue.pop(0)
            if node not in visited:
                
                visited.append(node)
                neighbours = graph[node]
    
                for neighbour in neighbours:
                    queue.append(neighbour)
        return visited

    def bdfInit(self):
        graph = {'A': ['B', 'C', 'E'],
                'B': ['A','D', 'E'],
                'C': ['A', 'F', 'G'],
                'D': ['B'],
                'E': ['A', 'B','D'],
                'F': ['C'],
                'G': ['C']}

        print(self.bfs(graph, 'A'))

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
import os
import sys
import time
from graph import *
from priority_queue import *

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt


class MainWindow(qtw.QMainWindow):

    def run(self):
        key_node_start = 'S'
        key_node_goal = 'G'
        verbose = True
        time_sleep = 2
        graphucs = Graph()
        graphucs.addNode('S') # start
        graphucs.addNode('a')
        graphucs.addNode('b')
        graphucs.addNode('c')
        graphucs.addNode('d')
        graphucs.addNode('e')
        graphucs.addNode('f')
        graphucs.addNode('G') # goal
        graphucs.addNode('h')
        graphucs.addNode('p')
        graphucs.addNode('q')
        graphucs.addNode('r')
        graphucs.connect('S', 'd', 3)
        graphucs.connect('S', 'e', 9)
        graphucs.connect('S', 'p', 1)
        graphucs.connect('b', 'a', 2)
        graphucs.connect('c', 'a', 2)
        graphucs.connect('d', 'b', 1)
        graphucs.connect('d', 'c', 8)
        graphucs.connect('d', 'e', 2)
        graphucs.connect('e', 'h', 8)
        graphucs.connect('e', 'r', 2)
        graphucs.connect('f', 'c', 3)
        graphucs.connect('f', 'G', 2)
        graphucs.connect('h', 'p', 4)
        graphucs.connect('h', 'q', 4)
        graphucs.connect('p', 'q', 15)
        graphucs.connect('r', 'f', 1)
        if key_node_start not in graphucs.getNodes() or key_node_goal not in graphucs.getNodes():
            print('Error: key_node_start \'%s\' or key_node_goal \'%s\' not exists!!' % (key_node_start, key_node_goal))
        else:
            # UCS uses priority queue, priority is the cumulative cost (smaller cost)
            queue = PriorityQueue()

            # expands initial node

            # get the keys of all successors of initial node
            keys_successors = graphucs.getSuccessors(key_node_start)

            # adds the keys of successors in priority queue
            for key_sucessor in keys_successors:
                weight = graphucs.getWeightEdge(key_node_start, key_sucessor)
                # each item of queue is a tuple (key, cumulative_cost)
                queue.insert((key_sucessor, weight), weight)


            reached_goal, cumulative_cost_goal = False, -1
            while not queue.is_empty():
                # remove item of queue, remember: item of queue is a tuple (key, cumulative_cost)
                key_current_node, cost_node = queue.remove() 
                if(key_current_node == key_node_goal):
                    reached_goal, cumulative_cost_goal = True, cost_node
                    break

                if verbose:
                    # shows a friendly message
                    print('Expands node \'%s\' with cumulative cost %s ...' % (key_current_node, cost_node))
                    time.sleep(time_sleep)

                # get all successors of key_current_node
                keys_successors = graphucs.getSuccessors(key_current_node)

                if keys_successors: # checks if contains successors
                    # insert all successors of key_current_node in the queue
                    for key_sucessor in keys_successors:
                        cumulative_cost = graphucs.getWeightEdge(key_current_node, key_sucessor) + cost_node
                        queue.insert((key_sucessor, cumulative_cost), cumulative_cost)

            if(reached_goal):
                print('\nReached goal! Cost: %s\n' % cumulative_cost_goal)
            else:
                print('\nUnfulfilled goal.\n')


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
        # os.system('python ucs/ucs.py')
        costoUniformAct.triggered.connect(self.run)

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
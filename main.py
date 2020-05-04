import os
import sys
import time
from graph import *
from priority_queue import *
from node import *
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

    def __eq__(self, other):
        return self.position == other.position

    def __init__(self):
        self.parent = None
        self.position = None
        self.g = 0
        self.h = 0
        self.f = 0
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

        
        AestrellaAct.triggered.connect(self.astar)
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
    
    def astar(self):

        maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        start = (0, 0)
        end = (7, 6)

        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = NodeA(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = NodeA(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                print(path)
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = NodeA(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)




if __name__ == "__main__":

    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
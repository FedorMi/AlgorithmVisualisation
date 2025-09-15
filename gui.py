import sys
import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from random import randint, choice
from search_and_sort_algorithms import Sort_Worker, Search_Worker
#from implement_algorithms import Sort_Worker, Search_Worker


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python ")
        self.setGeometry(100, 100, 1400, 920)
        self.choice = 0
        self.small, self.large, self.amount = 0, 1000, 50
        self.layout = QVBoxLayout()
        choose_mode = QComboBox()
        choose_mode.setStyleSheet("background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px")
        self.current_wrapper = QWidget()
        self.sort_layout = QVBoxLayout()
        self.current_wrapper.setLayout(self.sort_layout)
        self.setStyleSheet("background-color: rgb(20, 20, 35);")
        modes = ["Sorting", "Searching"]
        choose_mode.addItems(modes)
        choose_mode.currentIndexChanged.connect(self.sort_or_search)
        self.setLayout(self.layout)
        self.layout.addWidget(choose_mode)
        self.setup_sorting_layout(self.sort_layout)
        self.layout.addWidget(self.current_wrapper)
        self.show()

    def sort_or_search(self, choice):
        self.choice = choice
        if choice:
            self.layout.removeWidget(self.current_wrapper)
            self.current_wrapper.close()
            self.current_wrapper = QWidget()
            self.search_layout = QVBoxLayout()
            self.current_wrapper.setLayout(self.search_layout)
            self.setup_searching_layout(self.search_layout)
            self.layout.addWidget(self.current_wrapper)
            self.search_num = 0
        else:
            self.layout.removeWidget(self.current_wrapper)
            self.current_wrapper.close()
            self.current_wrapper = QWidget()
            self.sort_layout = QVBoxLayout()
            self.current_wrapper.setLayout(self.sort_layout)
            self.setup_sorting_layout(self.sort_layout)
            self.layout.addWidget(self.current_wrapper)
            self.sort_num = 0

    # searching functions
    def setup_searching_layout(self, search_layout):
        self.pixw = 1400
        self.pixh = 800
        self.label = QtWidgets.QLabel()
        top_row = QHBoxLayout()

        # button to generate a new random array
        button_new = QPushButton("New Random Array", self)
        button_new.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
        button_new.clicked.connect(self.setup_random_array_search)
        top_row.addWidget(button_new)

        # dropdown to select searching algorithm
        select_searching_algo = QComboBox()
        select_searching_algo.setStyleSheet("background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px")
        searching_algos = ["Linear Search", "Binary Search"]
        select_searching_algo.addItems(searching_algos)
        select_searching_algo.currentIndexChanged.connect(self.search_choice)
        self.search_num = 0
        top_row.addWidget(select_searching_algo)

        # button to run the searching algorithm
        button_searching = QPushButton("Run Searching Algorithm", self)
        button_searching.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
        button_searching.clicked.connect(self.run_searching)
        top_row.addWidget(button_searching)

        # button to sort the array
        button_sort = QPushButton("Sort the list", self)
        button_sort.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
        button_sort.clicked.connect(self.run_sort)
        top_row.addWidget(button_sort)

        # dropdown to select size of the array
        select_size = QComboBox()
        select_size.setStyleSheet("background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px")
        choose_a_size = ["Choose Size of List", "8", "16", "50", "100", "200", "300", "400", "500"]
        select_size.addItems(choose_a_size)
        select_size.currentIndexChanged.connect(self.choose_size_search)
        top_row.addWidget(select_size)
        
        # initial row of buttons at the bottom to manually search
        # only shows up to 16 buttons
        search_layout.addLayout(top_row)
        self.bottom_wrapper = QWidget()
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(0, 0, 0, 0)
        how_many = self.amount if self.amount <= 16 else 16
        for i in range(how_many):
            button = QPushButton(str(i), self)
            button.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
            button.setObjectName(str(i))
            button.clicked.connect(self.show_number)
            bottom_row.addWidget(button)
        search_layout.addWidget(self.label)
        self.bottom_wrapper.setLayout(bottom_row)
        search_layout.addWidget(self.bottom_wrapper)
        self.label.setStyleSheet("border:1px solid rgb(0, 255, 0);")
        canvas = QtGui.QPixmap(self.pixw, self.pixh)
        self.label.setPixmap(canvas)
        self.threadpool = QThreadPool()
        self.setup_random_array_search()
    
    def search_choice(self, num):
        self.search_num = num

    def choose_size_search(self, num):
        # sets up the row of buttons at the bottom to manually search
        # only shows up to 16 buttons
        amounts = [50, 8, 16, 50, 100, 200, 300, 400, 500]
        self.amount = amounts[num]
        self.search_layout.removeWidget(self.bottom_wrapper)
        self.bottom_wrapper.close()
        self.bottom_wrapper = QWidget()
        bottom_row = QHBoxLayout()
        self.setup_random_array_search()
        how_many = self.amount if self.amount <= 16 else 16
        for i in range(how_many):
            button = QPushButton(str(i), self)
            button.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
            button.setObjectName(str(i))
            button.clicked.connect(self.show_number)
            bottom_row.addWidget(button)
        bottom_row.setContentsMargins(0, 0, 0, 0)
        self.bottom_wrapper.setLayout(bottom_row)
        self.search_layout.addWidget(self.bottom_wrapper)
        self.update()
    
    def run_searching(self):
        # creates a worker thread to run the searching algorithm
        worker = Search_Worker(self.arr, self.guess_number, self.search_num)
        worker.signals.guess.connect(self.draw_guess_line)
        self.threadpool.start(worker)

    def run_sort(self):
        # sorts the array for binary search
        self.arr.sort()
        self.draw_array_with_outline_search()

    def show_number(self):
        # when a button at the bottom is clicked, it shows the guess line for that index
        i = int(self.sender().objectName())
        self.draw_guess_line(i)

    def draw_guess_line(self, i):
        # draws a line for the guess at index i
        painter = QtGui.QPainter(self.label.pixmap())
        myx = int(self.aw*i/self.lengtho)+int(self.pen_width/2)
        myy = int(self.ah*(self.arr[i]/self.highest))
        self.pen.setColor(QtGui.QColor('black'))
        self.pen.setWidth(int(self.pen_width))
        painter.setPen(self.pen)
        painter.drawLine(myx, self.ah, myx, self.ah-myy)
        if self.guess_number == self.arr[i]:
            self.pen.setColor(QtGui.QColor('green'))
            self.pen.setWidth(int(self.pen_width-2))
            painter.setPen(self.pen)
            painter.drawLine(myx, self.ah, myx, self.ah-myy)
            print("correct guess")
        else:
            self.pen.setColor(QtGui.QColor('red'))
            self.pen.setWidth(int(self.pen_width-2))
            painter.setPen(self.pen)
            painter.drawLine(myx, self.ah, myx, self.ah-myy)
            if self.guess_number < self.arr[i]:
                print("smaller")
            else:
                print("bigger")

        self.update()
    
    def setup_random_array_search(self):
        # generates a new random array and a new guess number
        self.arr = np.random.randint(self.small, self.large, self.amount)
        #self.arr.sort()
        self.guess_number = choice(self.arr)
        self.draw_array_with_outline_search()

    def draw_array_with_outline_search(self):
        # draws the array 
        lengtho, aw, ah, highest, painter, pen, pen_width = self.setup_draw()
        for i, k in enumerate(self.arr):
            myx = int(aw*i/lengtho)+int(pen_width/2)
            myy = int(ah*(k/highest))
            pen.setColor(QtGui.QColor('black'))
            pen.setWidth(int(pen_width))
            painter.setPen(pen)
            painter.drawLine(myx, ah, myx, ah-myy)
            pen.setColor(QtGui.QColor('white'))
            pen.setWidth(int(pen_width-2))
            painter.setPen(pen)
            painter.drawLine(myx, ah, myx, ah-myy)
        self.lengtho, self.aw, self.ah, self.highest, self.pen, self.pen_width = lengtho, aw, ah, highest, pen, pen_width 
        self.update()
    

    # sorting part functions
    def setup_sorting_layout(self, sort_layout):
        self.pixw = 1400
        self.pixh = 800
        self.label = QtWidgets.QLabel()
        top_row = QHBoxLayout()

        # button to generate a new random array
        button = QPushButton("New Random Array", self)
        button.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
        button.clicked.connect(self.setup_random_array)
        top_row.addWidget(button)

        # dropdown to select sorting algorithm
        select_sorting_algo = QComboBox()
        select_sorting_algo.setStyleSheet("background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px")
        sorting_algos = ["Bubble Sort", "Selection Sort", "Quick Sort", "Merge Sort", "Heap Sort"]
        select_sorting_algo.addItems(sorting_algos)
        select_sorting_algo.currentIndexChanged.connect(self.sort_choice)
        self.sort_num = 0
        top_row.addWidget(select_sorting_algo)

        # button to run the sorting algorithm
        button_sorting = QPushButton("Run Sorting Algorithm", self)
        button_sorting.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
        button_sorting.clicked.connect(self.run_sorting)
        top_row.addWidget(button_sorting)

        # dropdown to select size of the array
        select_size = QComboBox()
        select_size.setStyleSheet("background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px")
        choose_a_size = ["Choose Size of List", "8", "16", "50", "100", "200", "300", "400", "500"]
        select_size.addItems(choose_a_size)
        select_size.currentIndexChanged.connect(self.choose_size_sort)
        top_row.addWidget(select_size)
        
        # initial row of buttons at the bottom to manually sort
        # only shows up to 16 buttons
        self.bottom_wrapper = QWidget()
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(0, 0, 0, 0)
        self.switch_places = []
        how_many = self.amount if self.amount <= 16 else 16
        for i in range(how_many):
            button = QPushButton(str(i), self)
            button.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
            button.setObjectName(str(i))
            button.clicked.connect(self.show_number_sort)
            bottom_row.addWidget(button)
        self.bottom_wrapper.setLayout(bottom_row)
        sort_layout.addLayout(top_row)
        sort_layout.addWidget(self.label)
        sort_layout.addWidget(self.bottom_wrapper)
        self.label.setStyleSheet("border:1px solid rgb(0, 255, 0);")
        canvas = QtGui.QPixmap(self.pixw, self.pixh)
        self.label.setPixmap(canvas)
        self.threadpool = QThreadPool()
        self.setup_random_array()
        #self.setup_sorting_steps()
    
    def show_number_sort(self):
        # when a button at the bottom is clicked, it shows the sort line for that index
        i = int(self.sender().objectName())
        self.draw_sort_line(i)
        self.switch_places.append(i)
        if len(self.switch_places) > 1:
            self.arr[self.switch_places[0]], self.arr[self.switch_places[1]] = self.arr[self.switch_places[1]], self.arr[self.switch_places[0]]
            self.draw_aray_with_outline()
            self.switch_places = []

    def draw_sort_line(self, i):
        # draws a line at index i
        painter = QtGui.QPainter(self.label.pixmap())
        myx = int(self.aw*i/self.lengtho)+int(self.pen_width/2)
        myy = int(self.ah*(self.arr[i]/self.highest))
        self.pen.setColor(QtGui.QColor('black'))
        self.pen.setWidth(int(self.pen_width))
        painter.setPen(self.pen)
        painter.drawLine(myx, self.ah, myx, self.ah-myy)
        self.pen.setColor(QtGui.QColor('red'))
        self.pen.setWidth(int(self.pen_width-2))
        painter.setPen(self.pen)
        painter.drawLine(myx, self.ah, myx, self.ah-myy)
        self.update()
    
    def choose_size_sort(self, num):
        # sets up the row of buttons at the bottom to manually sort
        # only shows up to 16 buttons
        amounts = [50, 8, 16, 50, 100, 200, 300, 400, 500]
        self.amount = amounts[num]
        self.sort_layout.removeWidget(self.bottom_wrapper)
        self.bottom_wrapper.close()
        self.bottom_wrapper = QWidget()
        bottom_row = QHBoxLayout()
        self.setup_random_array()
        self.switch_places = []
        how_many = self.amount if self.amount <= 16 else 16
        for i in range(how_many):
            button = QPushButton(str(i), self)
            button.setStyleSheet("QPushButton {background-color: rgb(20, 20, 35); color: rgb(0, 255, 0); border:1px solid rgb(0, 255, 0); font: 18px} QPushButton::hover {background-color: rgb(20, 100, 35);}")
            button.setObjectName(str(i))
            button.clicked.connect(self.show_number_sort)
            bottom_row.addWidget(button)
        bottom_row.setContentsMargins(0, 0, 0, 0)
        self.bottom_wrapper.setLayout(bottom_row)
        self.sort_layout.addWidget(self.bottom_wrapper)
        self.update()
    
    def setup_random_array(self):
        # generates a new random array
        self.arr = np.random.randint(self.small, self.large, self.amount)
        self.draw_aray_with_outline()
    
    def sort_choice(self, num):
        # sets the sorting algorithm choice
        self.sort_num = num
    
    def run_sorting(self):
        # creates a worker thread to run the sorting algorithm
        worker = Sort_Worker(self.arr, self.sort_num)
        worker.signals.progress.connect(self.draw_aray_show_with_outline_switch)
        worker.signals.comparison.connect(self.draw_aray_show_with_outline_comparison)
        worker.signals.finished.connect(self.draw_aray_with_outline)
        self.threadpool.start(worker)

    def draw_aray_with_outline(self):
        # draws the array with an outline
        lengtho, aw, ah, highest, painter, pen, pen_width = self.setup_draw()
        for i, k in enumerate(self.arr):
            myx = int(aw*i/lengtho)+int(pen_width/2)
            myy = int(ah*(k/highest))
            pen.setColor(QtGui.QColor('black'))
            pen.setWidth(int(pen_width))
            painter.setPen(pen)
            painter.drawLine(myx, ah, myx, ah-myy)
            pen.setColor(QtGui.QColor('green'))
            pen.setWidth(int(pen_width-2))
            painter.setPen(pen)
            painter.drawLine(myx, ah, myx, ah-myy)
        self.lengtho, self.aw, self.ah, self.highest, self.pen, self.pen_width = lengtho, aw, ah, highest, pen, pen_width 
        self.update()

    def draw_aray_show_with_outline_switch(self, a, b):
        # draws the array with an outline and highlights the indexes being chosen to switch in red
        self.draw_aray_show_with_outline_helper(a, b, "red")

    def draw_aray_show_with_outline_comparison(self, a, b):
        # draws the array with an outline and highlights the comparison in blue
        self.draw_aray_show_with_outline_helper(a, b, "blue")
    
    def draw_aray_show_with_outline_helper(self, a, b, color):
        # array draw helper for switching and comparison
        lengtho, aw, ah, highest, painter, pen, pen_width = self.setup_draw()
        for i, k in enumerate(self.arr):
            myx = int(aw*i/lengtho)+int(pen_width/2)
            myy = int(ah*(k/highest))
            pen.setColor(QtGui.QColor('black'))
            pen.setWidth(int(pen_width))
            painter.setPen(pen)
            painter.drawLine(myx, ah, myx, ah-myy)
            pen.setWidth(int(pen_width-2))
            if i == a or i == b:
                pen.setColor(QtGui.QColor(color))
                painter.setPen(pen)
                painter.drawLine(myx, ah, myx, ah-myy)
                pen.setColor(QtGui.QColor('green'))
                painter.setPen(pen)
            else:
                pen.setColor(QtGui.QColor('green'))
                painter.setPen(pen)
                painter.drawLine(myx, ah, myx, ah-myy)
        self.lengtho, self.aw, self.ah, self.highest, self.pen, self.pen_width = lengtho, aw, ah, highest, pen, pen_width 
        self.update()

    def setup_draw(self):
        # sets up the drawing parameters
        self.label.clear()
        canvas = QtGui.QPixmap(self.pixw, self.pixh)
        self.label.setPixmap(canvas)
        lengtho = len(self.arr)
        aw = self.pixw
        ah = self.pixh
        highest = max(self.arr)
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor('green'))
        pen_width = aw/lengtho
        pen.setWidth(int(pen_width))
        painter.setPen(pen)
        return lengtho, aw, ah, highest, painter, pen, pen_width

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

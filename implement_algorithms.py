from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from random import randint, choice
import time


class Sort_Worker(QRunnable):
    def __init__(self, arr = [3, 2, 1], choice = 0):
        super(Sort_Worker, self).__init__()
        self.arr = arr
        self.signals = WorkerSignals()
        sorting_algos = [self.bubble_sort, self.selection_sort, self.quick_sort, self.merge_sort, self.heap_sort]
        self.fn = sorting_algos[choice]
    
    def run(self):
        self.fn()

    def draw_switch(self, i, j, times):
        self.signals.progress.emit(i, j)
        time.sleep(times)

    def draw_comparison(self, i, j, times):
        self.signals.comparison.emit(i, j)
        time.sleep(times)

    def bubble_sort(self):
        arr = self.arr
        n = len(arr)
        #TODO implement bubble sort

        self.signals.finished.emit()

    def selection_sort(self):
        arr = self.arr
        n = len(arr)
        #TODO implement selection sort

        self.signals.finished.emit()

    def quick_sort(self, begin=0, end=None):
        arr = self.arr
        n = len(arr)
        #TODO implement quick sort

        self.signals.finished.emit()

    def merge_sort(self):
        arr = self.arr
        n = len(arr)
        #TODO implement merge sort

        self.signals.finished.emit()
    
    def heap_sort(self):
        arr = self.arr
        n = len(arr)
        #TODO implement heap sort

        self.signals.finished.emit()

class Search_Worker(QRunnable):
    def __init__(self, arr = [3, 2, 1], guess = 1, choice = 0):
        super(Search_Worker, self).__init__()
        self.guess = guess
        self.arr = arr
        self.signals = WorkerSignals()
        searching_algos = [self.linear_search, self.binary_search]
        self.fn = searching_algos[choice]

    def run(self):
        self.fn()

    def draw(self, i, times):
        self.signals.guess.emit(i)
        time.sleep(times)

    def linear_search(self):
        arr = self.arr
        n = len(arr)
        #TODO implement linear search


    def binary_search(self):
        arr = self.arr
        n = len(arr)
        #TODO implement binary search


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    list = pyqtSignal(list)
    progress = pyqtSignal(int, int)
    comparison = pyqtSignal(int, int)
    guess = pyqtSignal(int)
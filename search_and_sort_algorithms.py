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
        for i in range(n):
            for j in range(n-1):
                if self.arr[j]>arr[j+1]:
                    temp = arr[j]
                    arr[j] = arr[j+1]
                    arr[j+1] = temp
                    self.signals.progress.emit(j+1, j)
                    time.sleep(0.01)
        self.signals.finished.emit()

    def selection_sort(self):
        arr = self.arr
        n = len(arr)
        for i in range(n):
            j = i
            while j > 0 and arr[j]<arr[j-1]:
                temp = arr[j-1]
                arr[j-1] = arr[j]
                arr[j] = temp
                self.signals.progress.emit(j-1, j)
                time.sleep(0.01)
                j -= 1
        self.signals.finished.emit()

    def quick_sort(self, begin=0, end=None):
        arr = self.arr
        if end is None:
            end = len(arr) - 1
        def _quick_sort(begin, end):
            if begin >= end:
                return
            pivot = self.quick_helper(begin, end)
            _quick_sort(begin, pivot-1)
            _quick_sort(pivot+1, end)
        _quick_sort(begin, end)
        self.signals.finished.emit()

    def quick_helper(self, begin, end):
        arr = self.arr
        pivot = begin
        for i in range(begin+1, end+1):
            if arr[i] <= arr[begin]:
                pivot += 1
                arr[i], arr[pivot] = arr[pivot], arr[i]
                self.signals.progress.emit(i, pivot)
                time.sleep(0.01)
        arr[pivot], arr[begin] = arr[begin], arr[pivot]
        self.signals.progress.emit(pivot, begin)
        time.sleep(0.01)
        return pivot
    
    def merge_sort(self):
        arr = self.arr
        self.merge_sort_helper(arr, 0, len(arr)-1)
        self.signals.finished.emit()

    def merge_sort_helper(self, arr, l, r):
        if (l < r):
            # Same as (l + r) / 2, but avoids overflow
            # for large l and r
            m = l + (r - l) // 2
            # Sort first and second halves
            self.merge_sort_helper(arr, l, m)
            self.merge_sort_helper(arr, m + 1, r)
            self.merge(arr, l, m, r)
    
    def merge(self, arr, start, mid, end):
        start2 = mid + 1
        # If the direct merge is already sorted
        if (arr[mid] <= arr[start2]):
            return
        # Two pointers to maintain start
        # of both arrays to merge
        while (start <= mid and start2 <= end):
            # If element 1 is in right place
            if (arr[start] <= arr[start2]):
                start += 1
            else:
                value = arr[start2]
                index = start2
                # Shift all the elements between element 1
                # element 2, right by 1.
                while (index != start):
                    arr[index] = arr[index - 1]
                    index -= 1
                    self.signals.progress.emit(index, index - 1)
                    time.sleep(0.01)
                arr[start] = value
                self.signals.progress.emit(start, start2)
                time.sleep(0.01)
                # Update all the pointers
                start += 1
                mid += 1
                start2 += 1
        
    def heap_sort(self):
        arr = self.arr
        n = len(arr)
        # Build max heap
        for i in range(n//2, -1, -1):
            self.heapify(arr, n, i)
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i] # Swap
            self.signals.progress.emit(i, 0)
            time.sleep(0.01)
            self.heapify(arr, i, 0) # Heapify root element
        self.signals.finished.emit()

    def heapify(self, arr, n, i):
        # Find largest among root and children
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        # If root is not largest, swap with largest and continue heapifying
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.signals.progress.emit(largest, i)
            time.sleep(0.01)
            self.heapify(arr, n, largest)

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
        for i in range(n):
            self.signals.guess.emit(i)
            time.sleep(0.04)
            if self.guess == self.arr[i]:
                break
    def binary_search(self):
        arr = self.arr
        self.binary_search_helper(arr, 0, len(arr)-1, self.guess)
    def binary_search_helper(self, arr, low, high, x):
        # Check base case
        if high >= low:
            mid = (high + low) // 2
            # If element is present at the middle itself
            self.signals.guess.emit(mid)
            time.sleep(0.5)
            if arr[mid] == x:
                print("found")
            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif arr[mid] > x:
                self.binary_search_helper(arr, low, mid - 1, x)
            # Else the element can only be present in right subarray
            else:
                self.binary_search_helper(arr, mid + 1, high, x)
        else:
            # Element is not present in the array
            print("not in array")

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    list = pyqtSignal(list)
    progress = pyqtSignal(int, int)
    comparison = pyqtSignal(int, int)
    guess = pyqtSignal(int)

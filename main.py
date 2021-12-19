import sys
import time
import pylab as pl
import numpy as np
from random import shuffle
from matplotlib.pyplot import scatter, show

N_TIMES = 5
LENGTHS = [1000, 5000, 10000]
PERFORMANCE_FUNCTIONS = ['insertion_sort', 'selection_sort', 'bubble_sort', 'merge_sort', 'quick_sort']
sys.setrecursionlimit(100000)


# Inserción

def insertion_sort(unorder_list):
    for i in range(1, len(unorder_list)):
        pivot = unorder_list[i]
        j = i - 1
        while j >= 0 and pivot < unorder_list[j]:
            unorder_list[j + 1] = unorder_list[j]
            j -= 1
        unorder_list[j + 1] = pivot
    return unorder_list


# Selección

def selection_sort(unorder_list):
    flag = True
    initial = 0
    while flag:
        flag = False
        for x in range(initial, len(unorder_list)):
            if x == initial:
                pivot = unorder_list[x]
                pivot_index = x
            if unorder_list[x] < pivot:
                flag = True
                pivot = unorder_list[x]
                pivot_index = x
        aux = unorder_list[initial]
        unorder_list[initial] = pivot
        unorder_list[pivot_index] = aux
        initial += 1
    return unorder_list


# Burbuja

def bubble_sort(unorder_list):
    flag = False
    for x in range(0, len(unorder_list) - 1):
        if unorder_list[x] > unorder_list[x + 1]:
            flag = True
            pivot = unorder_list[x]
            unorder_list[x] = unorder_list[x + 1]
            unorder_list[x + 1] = pivot
    if flag:
        return bubble_sort(unorder_list)
    return unorder_list


def merge(array, left_index, right_index, middle):
    left_copy = array[left_index:middle + 1]
    right_copy = array[middle + 1:right_index + 1]
    left_copy_index = 0
    right_copy_index = 0
    sorted_index = left_index
    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        if left_copy[left_copy_index] <= right_copy[right_copy_index]:
            array[sorted_index] = left_copy[left_copy_index]
            left_copy_index = left_copy_index + 1
        else:
            array[sorted_index] = right_copy[right_copy_index]
            right_copy_index = right_copy_index + 1
        sorted_index = sorted_index + 1
    while left_copy_index < len(left_copy):
        array[sorted_index] = left_copy[left_copy_index]
        left_copy_index = left_copy_index + 1
        sorted_index = sorted_index + 1
    while right_copy_index < len(right_copy):
        array[sorted_index] = right_copy[right_copy_index]
        right_copy_index = right_copy_index + 1
        sorted_index = sorted_index + 1


def merge_sort(array, left_index, right_index):
    if left_index >= right_index:
        return
    middle = (left_index + right_index) // 2
    merge_sort(array, left_index, middle)
    merge_sort(array, middle + 1, right_index)
    merge(array, left_index, right_index, middle)


def partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


def generate_lists(list_items, mixed=False):
    list_aux = list((range(1, list_items)))
    if mixed:
        shuffle(list_aux)
    return list_aux[:], list_aux[:], list_aux[:], list_aux[:], list_aux[:]


def test_performance(function_name, times):
    start_time = time.time()
    exec(function_name)
    time_performance = time.time() - start_time
    times.append(time_performance)


def mix_lists(lists, version, mixed=False):
    list_aux = list((range(1, LENGTHS[version])))
    if mixed:
        shuffle(list_aux)
    for list_name in lists:
        globals()[f"{list_name}_v{version}"] = list_aux[:]


for z in range(len(LENGTHS)):
    for j in PERFORMANCE_FUNCTIONS:
        globals()[f"{j}_times_v{z}"] = []
        globals()[f"no_{j}_times_v{z}"] = []


# Amplicación 1
def execute_sorts(mix=False):
    pre = 'no_' if mix else ''
    for x in range(0, len(LENGTHS)):
        for _ in range(N_TIMES):
            mix_lists(['list_one', 'list_two', 'list_three', 'list_four', 'list_five'], x, mix)
            test_performance(f"bubble_sort(list_one_v{x})", globals()[f"{pre}bubble_sort_times_v{x}"])
            test_performance(f"insertion_sort(list_two_v{x})", globals()[f"{pre}insertion_sort_times_v{x}"])
            test_performance(f"selection_sort(list_three_v{x})", globals()[f"{pre}selection_sort_times_v{x}"])
            test_performance(f"merge_sort(list_four_v{x}, 0, len(list_four_v{x}) - 1)",
                             globals()[f"{pre}merge_sort_times_v{x}"])
            test_performance(f"quick_sort(list_five_v{x}, 0, len(list_five_v{x}) - 1)",
                             globals()[f"{pre}quick_sort_times_v{x}"])


print('Unsorted list performance...')
execute_sorts(True)
print('Sorted list performance...')
execute_sorts(False)

X = []
for length in LENGTHS:
    X.append(length)

for index, k in enumerate(PERFORMANCE_FUNCTIONS):
    globals()[f"y_{index}"] = []
    for h in range(0, len(LENGTHS)):
        globals()[f"y_{index}"].append(np.mean(globals()[f"{k}_times_v{h}"]))
    scatter(X, globals()[f"y_{index}"])
    pl.plot(X, globals()[f"y_{index}"], '-o', label=f"ORDERED: {k}")

for index, k in enumerate(PERFORMANCE_FUNCTIONS):
    globals()[f"z_{index}"] = []
    for h in range(0, len(LENGTHS)):
        globals()[f"z_{index}"].append(np.mean(globals()[f"no_{k}_times_v{h}"]))
    scatter(X, globals()[f"z_{index}"])
    pl.plot(X, globals()[f"z_{index}"], '-o', label=f"UN-ORDERED: {k}")

pl.xlabel('List length')
pl.ylabel('Time')
pl.title("List Performance")
pl.legend()
show()

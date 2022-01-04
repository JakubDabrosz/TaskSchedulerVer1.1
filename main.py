# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import numpy
import random
import time
from pathlib import Path
import matplotlib.pyplot as plt

tab = []
tabix = []
tabInts = []


# czytanie z pliku
def file(dir_name):
    last_uploaded_file = dir_name + os.listdir(dir_name)[len(os.listdir(dir_name)) - 1]
    with open(last_uploaded_file, "r") as file:
        row_num = 0
        jobs, machines = [int(x) for x in next(file).split()]
        print("Liczba zadań w wszystkich projektach:", jobs)
        print("Ilość grup projektujących (2D, 3D, sprawdzający):", machines)
        for line in file:
            if 'Projekt' in line or 'Weryfikacja' in line:
                pass
            else:
                tabix.append(line.split())
                del tabix[row_num][0]
                tabInts.append([int(i) for i in tabix[row_num]])
                row_num += 1
        o = [list(x) for x in zip(*tabInts)]
        print("Czasy wykonywania zadań w projekcie przez projektantów:")
        print("Projektanci 3D:", o[0])
        print("Projektanci 2D:", o[1])
        print("Sprawdzający", o[2])
        print('\n')
    return machines, jobs, o


# obliczanie cmaxa
def makespan(sequence, tab, machines):
    cmax = numpy.zeros((machines, len(sequence) + 1))  # tworzy tablice

    for j in range(1, len(sequence) + 1):
        cmax[0][j] = cmax[0][j - 1] + tab[0][sequence[j - 1]]
    for i in range(1, machines):
        for j in range(1, len(sequence) + 1):
            cmax[i][j] = max(cmax[i - 1][j], cmax[i][j - 1]) + tab[i][sequence[j - 1]]
    return cmax


# funkcja dopisujaca sekwencje
def insertion(sequence, position, value):
    new = sequence[:]  # nowa sekwencja
    new.insert(position, value)  # dopisanie nowej sekwencji
    return new


# obliczanie czasu
def jobtime(job_id, data, machines):
    sum_p = 0
    for i in range(machines):
        sum_p += data[i][job_id]
    return sum_p


# zwykly neh
def neh(data, machines, jobs):
    sequence = []
    for j in range(jobs):
        sequence.append(j)
    order = sorted(sequence, key=lambda x: jobtime(x, data, machines), reverse=True)
    sequence = [order[0]]

    for i in range(1, jobs):
        min_cmax = 30000000
        for j in range(0, i + 1):
            seq = insertion(sequence, j, order[i])
            cmax = makespan(seq, data, machines)[machines - 1][len(seq)]
            if min_cmax > cmax:
                best_seq = seq
                min_cmax = cmax
        sequence = best_seq
        best_cmax = makespan(sequence, data, machines)
        # print ("Sekwencja: ",sequence)
    return sequence, makespan(sequence, data, machines)[machines - 1][jobs], makespan(sequence, data, machines)


def graph(best_makespan):
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    # Setting Y-axis limits
    gnt.set_ylim(0, 50)
    # Setting X-axis limits
    gnt.set_xlim(0, best_makespan[2][-1])
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Czas')
    gnt.set_ylabel('Processor')
    # Setting ticks on y-axis
    gnt.set_yticks([15, 25, 35])
    # Labelling tickes of y-axis
    gnt.set_yticklabels(['Walidacja', '2D', '3D'])
    # Setting graph attribute
    gnt.grid(True)

    # best_makespan = [[0, 18, 183, 409, 471], [0, 49, 304, 526, 536], [0, 59, 314, 536, 547]]
    # best_makespan = [[0, 25, 55, 73, 104, 176, 268, 347, 512, 957, 1282, 1508, 1808, 1870, 1895, 1910],
    #                  [0, 46, 78, 109, 168, 247, 363, 480, 633, 1251, 1552, 1669,
    #                   1862, 1881, 1905, 1917],
    #                  [0, 49, 79, 119, 177, 254, 371, 491, 643, 1551, 1758, 1768,
    #                   1872, 1891, 1907, 1919]]
    _2D = []
    _3D = []
    _Validation = []
    tab1 = best_makespan[0]
    tab2 = best_makespan[1]
    tab3 = best_makespan[2]
    for j in range(len(tab1)):
        _2D.append(tab1[j])
        _3D.append(tab2[j])
        _Validation.append(tab3[j])
    print("2D: ", _2D)
    print("3D: ", _3D)
    print("Validation: ", _Validation)
    print(" ")
    ### 2D
    _2D.insert(2, _2D[1])
    for i in range(3, len(_2D) * 2 - 3, 2):
        _2D.insert(i, _2D[i])

    ### 3D i
    _3D[0] = _2D[1]
    for i in range(2, len(_3D) * 2 - 4, 2):
        if _2D[i + 1] > _3D[i - 1]:
            _3D.insert(i, _2D[i + 2])
        else:
            _3D.insert(i, _3D[i - 1])

    if (_3D[len(_3D) - 2] > _2D[len(_2D) - 1]):
        _3D.insert(len(_3D) - 1, _3D[len(_3D) - 2])
    else:
        _3D.insert(len(_3D) - 1, _2D[len(_2D) - 1])

    ### Validation - sprawdzający
    _Validation[0] = _3D[1]
    for i in range(2, len(_Validation) * 2 - 4, 2):
        if _3D[i + 1] > _Validation[i - 1]:
            _Validation.insert(i, _3D[i + 1])
        else:
            _Validation.insert(i, _Validation[i - 1])

    if (_Validation[len(_Validation) - 2] > _3D[len(_3D) - 1]):
        _Validation.insert(len(_Validation) - 1, _Validation[len(_Validation) - 2])
    else:
        _Validation.insert(len(_Validation) - 1, _3D[len(_3D) - 1])

    print("2D: ", _2D)
    print("3D: ", _3D)
    print("Validation: ", _Validation)
    print(" ")
    ### wyznaczenie długości paska
    for i in range(3, len(_2D), 2):
        _2D[i] = _2D[i] - _2D[i - 1]

    for i in range(1, len(_3D), 2):
        _3D[i] = _3D[i] - _3D[i - 1]
        _Validation[i] = _Validation[i] - _Validation[i - 1]

    data_2D = iter(_2D)
    data_3D = iter(_3D)
    data_Validation = iter(_Validation)
    print("2D: ", _2D)
    print("3D: ", _3D)
    print("Validation: ", _Validation)
    print(" ")
    graph_2D = [i for i in zip(data_2D, data_2D)]
    graph_3D = [i for i in zip(data_3D, data_3D)]
    graph_Validation = [i for i in zip(data_Validation, data_Validation)]
    # Declaring a bar in schedule
    print("2D: ", graph_2D)
    print("3D: ", graph_3D)
    print("Validation: ", graph_Validation)
    print(" ")
    gnt.broken_barh(graph_2D, (30, 9),
                    facecolors=('b', 'g', 'r', 'c', 'm', 'y', 'k'))
    gnt.broken_barh(graph_3D, (20, 9),
                    facecolors=('b', 'g', 'r', 'c', 'm', 'y', 'k'))
    gnt.broken_barh(graph_Validation, (10, 9),
                    facecolors=('b', 'g', 'r', 'c', 'm', 'y', 'k'))
    plt.savefig("graph1_main_test.png")


# main
if __name__ == "__main__":
    jobs, machines, o = file("static/uploads/")
    seq, cmax, cmax2 = neh(o, jobs, machines)
    graph(cmax2)
    print("NEH:", seq, '\nBest makespan:', cmax2)

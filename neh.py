import os
import numpy


# czytanie z pliku
def file(dir_name):
    last_uploaded_file = dir_name
    with open(last_uploaded_file, "r") as file:
        row_num = 0
        tabix = []
        tabInts = []
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
    cmax = numpy.zeros((machines, len(sequence) + 1))

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

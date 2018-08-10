from __future__ import print_function
from itertools import combinations, permutations
# Import Python wrapper for or-tools constraint solver.
# from ortools.constraint_solver import pywrapcp
import random
import numpy as np


def getdatas(machines, processing_times, sol_line_tasks, sol_line):
    numberofjob = len(machines)
    numberofmashine = len(machines[0])

    # get the sum processing time for every macshine
    sumtimeforeachmachine = np.zeros((numberofmashine))
    for i in range(numberofjob):
        for j in range(numberofmashine):
            for m in range(numberofmashine):

                if machines[i][j] == m:
                    sumtimeforeachmachine[m] += processing_times[i][j]

    sumtimeforeachjob = np.array(processing_times).sum(1)

    sumprosessingtime = [np.array(processing_times).sum().sum()]
    avetime_machine = sumtimeforeachmachine.sum()/numberofmashine
    avetime_job = sumtimeforeachjob.sum()/numberofjob

    datas = []
    id = 0
    for i in range(numberofjob):
        for j in range(numberofmashine):
            data1 = [
                id,                                    # id
                1/numberofjob,
                1/numberofmashine,
                j/numberofmashine,
                sumtimeforeachmachine[j]/avetime_machine,
                sumtimeforeachjob[i]/avetime_job,
                processing_times[i][j]/sumtimeforeachmachine[j],
                processing_times[i][j]/sumtimeforeachjob[i],
                machines[i][j]/numberofmashine,
            ]
            data2 = []
            for ii in range(numberofjob):
                for jj in range(numberofmashine):
                    data2.append(
                        processing_times[ii][jj] / sumprosessingtime[0])

            data3 = []
            for ii in range(numberofjob):
                for jj in range(numberofmashine):
                    data3.append(machines[ii][jj] / numberofmashine)
            a = sol_line_tasks.find(str(i)+'_'+str(j))
            b = a % (11 + numberofjob * 10 + 1)
            # b = a % 82
            c = b - 11
            data4 = [c // 10]+[machines[i][j]]
            # print(data4)

            data = data1+data2+data3+data4
            datas.append(data)
            id += 1
    return datas


def gettraindata(name, m, n, time_low, time_high, numofloop):
    # machines is the workpiece processing sequence
        # line i is job i
        # row j is mashine j
        # means that job i's processing sequence
    # processing_time is the processing time of job i processing j
    fzzl = open('./data/withoutsolute_log_' + name + '.txt', 'a')
    datatosave = []
    a = list(range(time_low, time_high))

    processing_times = []
    for k in range(n):
        processing_times.append(random.sample(a, m))

    pssave = np.array(processing_times)
    np.savetxt('./data/pssave_' + name + '.csv',
               pssave, fmt='%d', delimiter=',')

    for i in range(numofloop):
        print(i, file=fzzl)
        a = list(range(m))
        machines = []
        for k in range(n):
            machines.append(random.sample(a, m))

        print('machines', file=fzzl)
        print(machines, file=fzzl)

        print('processing_times', file=fzzl)
        print(processing_times, file=fzzl)


if __name__ == '__main__':
    m = 8
    n = 8
    time_low = 6
    time_high = 30
    numofloop = 1000

    gettraindata('traindata_'+'m='+str(m)+'_n='+str(n) +
                 '_timelow='+str(time_low)+'_timehight='+str(time_high)
                 + '_numofloop='+str(numofloop), m=m, n=n, time_low=time_low,
                 time_high=time_high, numofloop=numofloop)

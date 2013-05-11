#!/usr/bin/python

def compv(vector1, vector2):
        return reduce(lambda bool1, bool2 : bool1 and bool2, [i >= j for i, j in zip(vector1, vector2)])

def addv(vector1, vector2):
        return [i + j for i, j in zip(vector1, vector2)]

def subv(vector1, vector2):
        return [i - j for i, j in zip(vector1, vector2)]

def isSafe(avail, need, alloc):
        np = len(need)
        finish = [False for i in range(np)]
        sequence = []
        count = 0;
        stop = True
        i = 0
        while i < len(finish):
                if finish[i] == False and compv(avail, need[i]) == True:
                        stop = False
                        finish[i] = True
                        sequence.append(i)
                        avail = addv(avail, alloc[i])
                        count += 1
                if stop == False and i == len(finish) - 1:
                        i = 0
                        stop = True
                else:
                        i += 1
        if count == np:
                print "Safe sequence found: " + str(sequence)
                return True
        else:
                return False

def requestResource(processNumber, request, avail, need, alloc):
        if compv(need[processNumber], request) == False:
                print "Exceeded maximum claim"
                return
        if compv(avail, request) == False:
                print "Resources not yet available. Process must wait"
                return
        avail = subv(avail, request)
        need = list(need)
        alloc = list(alloc)
        need[processNumber] = subv(need[processNumber], request)
        alloc[processNumber] = addv(alloc[processNumber], request)
        return isSafe(avail, need, alloc)


""" Testing Banker's Algorithm with user input """
avail = []
alloc = need = None
nr = np = 0
reqM = allocM = maxM = ""

np = int(raw_input("Number of processes:"))
availV = raw_input("Enter the claim vector:") + "\n"
nr = len(availV)

print "Enter the allocation matrix:"
for i in range(np):
        allocM = allocM + raw_input() + "\n"
print "Enter the maximum claim matrix:"
for i in range(np):
        maxM = maxM + raw_input() + "\n"
requests = int(raw_input("How many resource requests to perform? "))
print "Enter ", requests, " request vectors in <process-number>:<resource-vector> form. Example- 3:4 5 6"
for i in range(requests):
        reqM = reqM + raw_input() + "\n"

avail = [int(a) for a in availV.split()]
alloc = tuple(tuple(int(b) for b in a.split()) for a in allocM.split("\n")[:-1])
maxClaims = tuple(tuple(int(b) for b in a.split()) for a in maxM.split("\n")[:-1])
need = tuple(subv(i, j) for i, j in zip(maxClaims, alloc))
reqs = tuple(a for a in reqM.split("\n")[:-1])

for r in reqs:
        r = r.split(':')
        process = int(r[0])
        reqVector = [int(a) for a in r[1].split()]
        print "Request vector for process", process, ":", reqVector
        result = requestResource(process, reqVector, avail, need, alloc)
        if result == True:
                print "Request granted\n"
        else if result == False:
                print "Unsafe state found. Request not granted\n"
        else:
                print "Request not granted\n"

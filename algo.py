# By default this is a max heap, but you can assign mycmp method to
# make it min heap.
class myHeap:
    def __init__(self, lst, mycmp = lambda a, b : a >= b):
        self.A = [item for item in lst]
        self.mycmp = mycmp
        self.buildHeapInPlace(self.A)

    def __str__(self):
        return str(self.A)

    def downwardHeapify(self, A, i, heapSize):
        if(heapSize <= 0 or i >= heapSize): return
        curI = i
        while(True):
            lgstI, l, r = curI, (curI << 1) + 1, (curI + 1) << 1
            if(l < heapSize and self.mycmp(A[l], A[lgstI])): lgstI = l
            if(r < heapSize and self.mycmp(A[r], A[lgstI])): lgstI = r
            if(lgstI != curI):
                A[lgstI], A[curI] = A[curI], A[lgstI]
                curI = lgstI
            else: break

    def upwardHeapify(self, A, i):
        curI = i
        while(True):
            parent = (curI >> 1) + 1
            if(parent >= 0 and self.mycmp(A[curI], A[parent])): 
                A[parent], A[curI] = A[curI], A[parent]
                curI = parent
            else: break
    
    def buildHeapInPlace(self, A):
        for i in range((len(A) >> 1) - 1, -1, -1):
            self.downwardHeapify(A, i, len(A))

    def sort(self):
        res = [item for item in self.A]
        for heapSize in range(len(res) - 1, 0, -1):
            res[0], res[heapSize] = res[heapSize], res[0]
            self.downwardHeapify(res, 0, heapSize)
        return res

    def add(self, val):
        A = self.A
        A.append(val)
        self.upwardHeapify(A, len(A) - 1)

    def pop(self):
        A = self.A
        if(not A): return
        A[0], A[len(A) - 1] = A[len(A) - 1], A[0]
        res = A.pop()
        self.downwardHeapify(A, 0, len(A))
        return res

    def top(self):
        if(self.A): return self.A[0]

    def size(self):
        return len(self.A)

# upperObject is the upperbound object in A.
# lowerObject is default to be 0
# this sorting is also stable, meaning if a and b both in A, a == b, and
# a appears before b, then in res a will also appear before b.
def myCountingSort(A, upperObject, lowerObject = 0, myhash = lambda a: a, useHashForUpperAndLowerBound = True):
    upperBound, lowerBound = upperObject, lowerObject
    if(useHashForUpperAndLowerBound):
        upperBound, lowerBound = myhash(upperObject), myhash(lowerObject)
    if(upperBound < lowerBound): return []
    res = [0 for i in A]
    track = [0 for i in range(upperBound - lowerBound + 1)]
    for val in A:
        track[myhash(val) - lowerBound] += 1
    for i in range(1, len(track)):
        track[i] += track[i - 1]
    for i in range(len(A) - 1, -1, -1):
        trackIndex = myhash(A[i]) - lowerBound
        track[trackIndex] -= 1
        res[track[trackIndex]] = A[i]
    return res

def getDecimalHashLst(smallestVal = 0, digits = 10, decimal = 10):
    return [lambda a, i=i: ((a - smallestVal) // (decimal**i)) % decimal for i in range(digits)]

# the key idea of radixSort is to create a list of hashes. The later that hash appears in the list,
# the more significant it is and the more impact it will have for the final result. For each hash,
# it takes O(k + n) where k is all the possible values for that hash. We have d hashes, so 
# eventually the whole algo takes O(d(k + n)).
def radixSort(A, digitUpperBound, digitLowerBound, myhashLst = getDecimalHashLst()):
    for myhash in myhashLst:
        A = myCountingSort(A, digitUpperBound, digitLowerBound, myhash, False)
    return A

def bucketSort(A, bucketsNum, myBucketHash, mySortHash = lambda a: a):
    res = []
    buckets = [[] for i in range(bucketsNum + 1)]
    for val in A:
        buckets[myBucketHash(val)].append(val)
    for bucket in buckets:
        bucket.sort(key = mySortHash)
    for bucket in buckets:
        res.extend(bucket)
    return res

#A = [-5,1,10,14,2,17,13,6,5,7,12,-3,-2,-1,-2,-3,0,3,2,-4,9,10,8]
#A = [(5, 2), (4, 3), (6, 9), (11, 5), (2, 4), (4, 5)]
#myhash = lambda a: (a[1] + 10) // 3
#sorthash = lambda a: a[1]

#mycmp = lambda a: a[1]
#A = [-5,1,10,14,2,17,13,6,5,7,12,-3,-2,-1,-2,-3,0,3,2,-4,9,10,8]
#print(myCountingSort(A, 20, -5))

#B = [(i, val) for i, val in enumerate(A)]
#print(myCountingSort(B, (99, 20), (99, -5), mycmp))

#B = [(99, i) for i in A]



#print(myCountingSort(B, (99, 20), (99, -5), mycmp))

#C = [(99, 0) for i in A]
#print(myCountingSort(C, (99, 0), (99, 0), mycmp))

#C = [(99, -4) for i in A]
#print(myCountingSort(C, (99, -4), (99, -4), mycmp))

#C = [(99, 1) for i in A]
#print(myCountingSort(C, (99, 1), (99, 1), mycmp))

#C = [-3 for i in A]
#print(myCountingSort(C, -3, -3))

#print(myCountingSort([], -3, -3))


#A = [-5,1,10,14,2,17,13,6,5,7,12,-3,-2,-1,-2,-3,0,3,2,-4,9,10,8]
#myhashLst = getDecimalHashLst(-100)
#print(radixSort(A, 9, 0, myhashLst))
##[-5, -4, -3, -3, -2, -2, -1, 0, 1, 2, 2, 3, 5, 6, 7, 8, 9, 10, 10, 12, 13, 14, 17]


#B = ["COW", "DOG", "SEA", "RUG", "ROW", "MOB", "BOX", "TAB", "BAR", "EAR", "TAR", "DIG", "BIG", "TEA", "NOW", "FOX"]
#myhashLst = [lambda a, i=i: ord(a[i]) for i in range(2, -1, -1)]
#print(radixSort(B, ord('Z'), ord('A'), myhashLst))
##['BAR', 'BIG', 'BOX', 'COW', 'DIG', 'DOG', 'EAR', 'FOX', 'MOB', 'NOW', 'ROW', 'RUG', 'SEA', 'TAB', 'TAR', 'TEA']

#C = [(5, 2), (4, 3), (6, 9), (11, 5), (2, 4), (4, 5)]
#myhashLst = [lambda a, i=i: a[i] for i in range(1, -1, -1)]
#print(radixSort(C, 20, 2, myhashLst))
##[(2, 4), (4, 3), (4, 5), (5, 2), (6, 9), (11, 5)]


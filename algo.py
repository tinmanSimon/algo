# heapify A with index i, expecting everywhere else is already a heap
# except at position i.
def heapify(A, i, heapSize, maxHeap = True):
    if(heapSize <= 0 or i >= heapSize): return
    mycmp = lambda a, b : a >= b
    if(not maxHeap): mycmp = lambda a, b : a <= b
    while(True):
        lgstI, l, r = i, (i << 1) + 1, (i + 1) << 1
        if(l < heapSize and mycmp(A[l], A[lgstI])): lgstI = l
        if(r < heapSize and mycmp(A[r], A[lgstI])): lgstI = r
        if(lgstI != i):
            A[lgstI], A[i] = A[i], A[lgstI]
            i = lgstI
        else: return

# builds max heap in place if maxHeap = True. Otherwise, builds min heap
def buildHeapInPlace(A, maxHeap = True):
    for i in range((len(A) >> 1) - 1, -1, -1):
        heapify(A, i, len(A), maxHeap)

def heapSort(A, ascending = True):
    buildHeapInPlace(A, ascending)
    for heapSize in range(len(A) - 1, 0, -1):
        A[0], A[heapSize] = A[heapSize], A[0]
        heapify(A, 0, heapSize, ascending)


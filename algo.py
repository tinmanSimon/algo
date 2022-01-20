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
            parent = ((curI + 1) >> 1) - 1
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
        



#heapSort(A)
#print(A)
#heapSort(A, False)
#print(A)
h = myHeap([1,10,14,2,17,13,6,5,7,12])
print(h)
print(h.sort())
print(h.pop(), h)
h.add(30)
print(h)
for i in range(30):
    k = h.pop()
    print(k, h)
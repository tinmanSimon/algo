import random

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

def partition(A, l, h, mycmp = lambda a, b: a < b):
    sampleIndex = random.randint(l, h - 1)
    A[sampleIndex], A[h - 1] = A[h - 1], A[sampleIndex]
    i = l
    for j in range(l, h - 1):
        if(mycmp(A[j], A[h - 1])):
            A[i], A[j] = A[j], A[i]
            i += 1
    A[i], A[h - 1] = A[h - 1], A[i]
    return i

# randomized quickSort, assuming all elements are distinct
def quickSort(A, mycmp = lambda a, b: a < b):
    def helper(A, l, h):
        if(l < h):
            q = partition(A, l, h, mycmp)
            helper(A, l, q)
            helper(A, q + 1, h)
    helper(A, 0, len(A))

# expect 0 < i <= len(A)
# selecting ith smallest number by default.
def quickSelect(A, i, selectSmallest = True):
    if(not selectSmallest): i = len(A) - i + 1
    l, h = 0, len(A)
    while(l < h):
        q = partition(A, l, h)
        if(q - l + 1 == i): return A[q]
        elif(q - l + 1 > i):
            h = q
        else:
            i = i - (q - l + 1)
            l = q + 1

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

class BSTNode:
    def __init__(self, key, p = None, l = None, r = None):
        self.key = key
        self.p = p
        self.l = l
        self.r = r
    
class BST:
    def __init__(self, head = None, myhash = lambda a: a):
        self.head = head
        self.myhash = myhash
        self.size = 0

    def root(self):
        return self.head

    def insert(self, key):
        prevNode, curNode = None, self.head
        while(curNode):
            prevNode = curNode
            if(self.myhash(key) <= self.myhash(curNode.key)):
                curNode = curNode.l
            else:
                curNode = curNode.r
        if(not prevNode): 
            self.head = BSTNode(key)
        elif(self.myhash(key) <= self.myhash(prevNode.key)):
            prevNode.l = BSTNode(key, prevNode)
        else:
            prevNode.r = BSTNode(key, prevNode)
        self.size += 1

    # return None if the key doesn't exist, return the BSTNode if found.
    def search(self, key):
        n = self.head
        while(n):
            if(n.key == key): return n
            elif(self.myhash(key) <= self.myhash(n.key)): n = n.l
            else: n = n.r
        return None

    def successor(self, node):
        if(not node): return None
        if(node.r): 
            lMost = node.r
            while(lMost.l): lMost = lMost.l
            return lMost
        while(node.p and node.p.r == node):
            node = node.p
        return node.p

    # replace BSTNode a with b.
    # note: it not only replace a on itself, but also its subtrees.
    #       and this could potentially mess up with BST's size, so
    #       it would be great to keep the size consistent when using
    #       this method.
    def replaceNode(self, a, b):
        if(not a): return
        elif(not a.p): self.head = b
        elif(a.p.l == a): a.p.l = b
        else: a.p.r = b
        if(b): b.p = a.p

    # if key doesn't exist, do nothing. Otherwise, remove the first node with 
    # the corresponding key
    def remove(self, key):
        nextNode, targetNode = None, self.search(key)
        if(not targetNode): return
        if(not targetNode.r): nextNode = targetNode.l
        elif(not targetNode.l): nextNode = targetNode.r
        else:
            nextNode = self.successor(targetNode)
            self.replaceNode(nextNode, nextNode.r)
            nextNode.l, nextNode.r = targetNode.l, targetNode.r
            nextNode.l.p = nextNode
            # if nextNode == targetNode.r, then after self.replaceNode(nextNode, nextNode.r)
            # targetNode.r can be None if nextNode.r is None. Hence the validity check of 
            # nextNode.r
            if(nextNode.r): nextNode.r.p = nextNode
        self.replaceNode(targetNode, nextNode)
        self.size -= 1

    # returns a list of elements in order
    def inorderList(self):
        res = []
        def helper(n):
            if(not n): return
            helper(n.l)
            res.append(n.key)
            helper(n.r)
        helper(self.head)
        return res

    # height start from 1. so if you have only 1 item, it returns 1
    # if BST is empty meaning self.head == None, then returns 0
    def getHeight(self):
        maxHeight, curHeight = 0, 1
        prevNode, curNode = None, self.head
        while(curNode):
            maxHeight = max(maxHeight, curHeight)
            prevNode, curPrevNode = curNode, prevNode
            if(curNode.l and curNode.p == curPrevNode):
                curNode = curNode.l
                curHeight += 1
            elif(curNode.r and curNode.r != curPrevNode):
                curNode = curNode.r
                curHeight += 1
            elif(curNode.p):
                curNode = curNode.p
                curHeight -= 1
            else: break
        return maxHeight



    def __str__(self):
        n, h = self.size, self.getHeight()
        rowsPos = [0 for i in range(2 * h - 1)]
        rowsStrs = ["" for i in range(2 * h - 1)]
        curRow, curCol = 0, 0
        
        def helper(node, curRow, curCol):
            if(not node): return [0, 0, 0]
            keyStr = str(node.key)
            keyStrLen = len(keyStr)
            if(not node.l and not node.r):
                rowsStrs[curRow] += (curCol - rowsPos[curRow]) * " " + keyStr
                rowsPos[curRow] = len(rowsStrs[curRow])#curCol + len(str(node.key))
                return [0, keyStrLen, 0]
            l = helper(node.l, curRow + 2, curCol)
            rowsStrs[curRow] += (curCol - rowsPos[curRow] + l[0] + l[1] + 1) * " " + keyStr
            #if(l[1]): 
            #    rowsStrs[curRow + 1] += (curCol - rowsPos[curRow] + l[0] + l[1]) * " " + "/"
            rowsPos[curRow] = len(rowsStrs[curRow])# curCol + l[0] + l[1] + 1 + len(str(node.key))
            if(keyStrLen < l[2]):
               rowsStrs[curRow] += (l[2] - keyStrLen) * "_"
               rowsPos[curRow] = len(rowsStrs[curRow])# (l[2] - len(str(node.key)))
            if(l[1]): 
                rowsStrs[curRow + 1] += (rowsPos[curRow] - rowsPos[curRow + 1] - keyStrLen - max(l[2] - keyStrLen, 0) - 1) * " " + "/"
                rowsPos[curRow + 1] = len(rowsStrs[curRow + 1]) #curCol + l[0] + l[1] + 1
            r = helper(node.r, curRow + 2, rowsPos[curRow] + 1)
            rowsStrs[curRow] += r[0] * "_"
            rowsPos[curRow] = len(rowsStrs[curRow])#r[0]
            if(r[1]): 
                rowsStrs[curRow + 1] += (rowsPos[curRow] - rowsPos[curRow + 1]) * " " + "\\"
                rowsPos[curRow + 1] = len(rowsStrs[curRow + 1]) #rowsPos[curRow]

            return [l[0] + l[1], l[2] + keyStrLen + r[0], r[1] + r[2]]

        helper(self.head, 0, 0)

        print("\n\n\nmat***********************************")
        for lst in rowsStrs:
            print("".join(lst))
        print("mat***********************************")
        return str(self.inorderList())

    


print(" " + "/")
    
b = BST()

A = []
n = 50
randIntBottom, randIntTop = 0, 100
print("started")
for i in range(n):
    A.append(random.randint(randIntBottom, randIntTop))

#A = [5,4,4,5]
A = [5, 59, 19, 36, 18, 40, 87, 49, 96, 67, 67, 88, 69, 75, 49, 97, 16, 48, 53, 93, 26, 52, 79, 72, 94, 23, 40, 15, 5, 60, 8, 44, 79, 26, 15, 44, 30, 58, 45, 87, 73, 11, 56, 58, 93, 48, 60, 1, 9, 96]
print("A:******************")
print(A)
for a in A:
    b.insert(a)
    #print(a, b)
#for i in range(10 * n):
#    j, k = random.randint(0, n - 1), random.randint(0, n - 1)
#    A[j], A[k] = A[k], A[j]
#print("A:******************")
#print(A)

print(b, b.size, b.getHeight())
#for a in A:
#    b.remove(a)
#    curB = b.inorderList()
#    for i in range(len(curB) - 1):
#        if(curB[i] > curB[i + 1]):
#            print("Error!!!! i = ", i)
#    print(b, b.getHeight())
print("finished")


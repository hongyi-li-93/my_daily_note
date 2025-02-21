

class SegTreeSum:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [self.null_value()] * self.n + arr
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.combine(self.tree[i << 1], self.tree[i << 1 | 1])

    def combine(self, v1, v2):
        # TODO: this can be updated to other agg func
        return v1 + v2

    def null_value(self):
        # TODO: this can be updated to other agg func
        return 0

    def update_single(self, p, value):
        # set value at position p
        self.tree[p + self.n] = value
        # move upward and update parents
        i = p + self.n
        while i > 1:
            self.tree[i >> 1] =self.combine(self.tree[i], self.tree[i ^ 1])
            i >>= 1

    # function to get sum on interval [l, r)
    def query_leftclose_rightopen(self, l, r):
        res = self.null_value()

        # loop to find the sum in the range
        l += self.n
        r += self.n

        while l < r:

            if (l & 1):
                res = self.combine(res, self.tree[l])
                l += 1

            if (r & 1):
                r -= 1
                res = self.combine(res, self.tree[r])

            l >>= 1
            r >>= 1
        return res


import heapq

class SegTreeCov:
    def __init__(self, arr):
        self.n = len(arr)
        self.area = [None] * self.n + arr
        for i in range(self.n - 1, 0, -1):
            self.area[i] = self.area[i << 1] + self.area[i << 1 | 1]
        self.cts = [0] * len(self.area)
        self.covered = [0] * len(self.area)

    # function to update on interval [l, r)
    def update_leftclose_rightopen(self, l, r, d):

        # loop to find the sum in the range
        l += self.n
        r += self.n

        update_sequence = []
        while l < r:
            if (l & 1):
                heapq.heappush(update_sequence, (-l, 0))
                l += 1

            if (r & 1):
                r -= 1
                heapq.heappush(update_sequence, (-r, 0))

            l >>= 1
            r >>= 1

        updated = set()
        while update_sequence:
            cur = heapq.heappop(update_sequence)
            i = -cur[0]
            if i in updated:
                continue
            updated.add(i)
            if cur[1] == 0:
                self.cts[i] += d

            if self.cts[i] > 0:
                self.covered[i] = self.area[i]
            elif i >= self.n:
                self.covered[i] = 0
            else:
                self.covered[i] = self.covered[i << 1] + self.covered[i << 1 | 1]

            j = i >> 1
            if j > 0:
                heapq.heappush(update_sequence, (-j, 1))


# Driver Code
if __name__ == "__main__":
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    mytree = SegTreeSum(a)

    # print the sum in range(1,2) index-based
    print(mytree.query_leftclose_rightopen(1, 3))

    # modify element at 2nd index
    mytree.update_single(2, 1)

    # print the sum in range(1,2) index-based
    print(mytree.query_leftclose_rightopen(1, 3))

    import random

    random.seed(99)
    for _ in range(3):
        n = random.randint(50, 500)
        arr = [random.randint(0, 9999) for _ in range(n)]
        mytree = SegTreeSum([a for a in arr])
        for t in range(n):
            qs = random.randint(0, n - 1)
            qe = random.randint(0, n - 1)
            qs, qe = min(qs, qe), max(qs, qe)
            u = random.randint(0, n - 1)
            d = random.randint(-9999, 9999)
            arr[u] = d
            mytree.update_single(u, d)
            v = 0
            for i in range(qs, qe + 1):
                v += arr[i]
            myms = mytree.query_leftclose_rightopen(qs, qe + 1)
            assert myms == v, f'test {t}, {v} != {myms}'

    print('what?')
    for _ in range(3):
        n = random.randint(50, 500)
        arr = [random.randint(0, 9999) for _ in range(n)]
        cts = [0] * n
        mytree = SegTreeCov([a for a in arr])
        itvs = []
        for t in range(n):
            us = random.randint(0, n - 1)
            ue = random.randint(0, n - 1)
            us, ue = min(us, ue), max(us, ue)
            itvs.append((us, ue))
            for i in range(us, ue + 1):
                cts[i] += 1
            mytree.update_leftclose_rightopen(us, ue+1, 1)
            v = 0
            for i in range(n):
                if cts[i] > 0:
                    v += arr[i]
            myms = mytree.covered[1]
            assert myms == v, f'test {t}, {v} != {myms}'
        for t, (us, ue) in enumerate(itvs):
            for i in range(us, ue + 1):
                cts[i] -= 1
            mytree.update_leftclose_rightopen(us, ue+1, -1)
            v = 0
            for i in range(n):
                if cts[i] > 0:
                    v += arr[i]
            myms = mytree.covered[1]
            assert myms == v, f'test {t}, {v} != {myms}'


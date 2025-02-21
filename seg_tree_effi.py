

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

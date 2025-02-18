# Python3 implementation of segment tree with range

# Ideally, we should not use global variables
# and large constant-sized arrays, we have
# done it here for simplicity.

""" si -> index of current node in segment tree 
    ss and se -> Starting and ending indexes of elements 
                for which current nodes stores sum. 
    us and ue -> starting and ending indexes of update query 
    diff -> which we need to add in the range us to ue """


class SegTreeRangeSum:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [None] * (self.n * 4)
        self.lazy = [None] * len(self.tree)
        self.i_to_se = [None] * len(self.tree)

        def _construct(ss, se, si):
            # out of range as ss can never be
            # greater than se
            if (ss > se):
                return

            self.i_to_se[si] = (ss, se)

            # If there is one element in array,
            # store it in current node of
            # segment tree and return
            if (ss == se):
                self.tree[si] = arr[ss]
                return

            # If there are more than one elements,
            # then recur for left and right subtrees
            # and store the sum of values in this node
            mid = (ss + se) // 2
            _construct(ss, mid, si * 2 + 1)
            _construct(mid + 1, se, si * 2 + 2)

            self.tree[si] = self.combine(self.tree[self.left(si)], self.tree[self.right(si)])

        _construct(0, self.n-1, 0)

    def left(self, si):
        return si * 2 + 1

    def right(self, si):
        return si * 2 + 2

    def out_of_range(self, qus, que, si):
        if si >= len(self.i_to_se) or self.i_to_se[si] is None:
            raise ValueError(f'index {si} should not be queried')
        ss, se = self.i_to_se[si]
        # Out of range
        if (ss > se or ss > que or se < qus):
            return True
        return False

    def covered_in_range(self, qus, que, si):
        ss, se = self.i_to_se[si]
        return (ss >= qus and se <= que)

    def combine(self, v1, v2):
        #TODO: this can be updated to other agg func
        s = 0
        if v1 is not None:
            s += v1
        if v2 is not None:
            s += v2
        return s

    def updated_tree_val(self, si):
        # TODO: this can be updated to other agg func
        ss, se = self.i_to_se[si]
        return self.tree[si] + (se - ss + 1) * self.lazy[si]

    def update_lazy_child(self, sc, si):
        # TODO: this can be updated to other agg func
        s = 0
        if self.lazy[sc] is not None:
            s += self.lazy[sc]
        return s + self.lazy[si]

    def update_lazy(self, si):
        if (self.lazy[si] is None):
            return
        # Make pending updates to this node.
        # Note that this node represents sum of
        # elements in arr[ss..se] and all these
        # elements must be increased by lazy[si]
        self.tree[si] = self.updated_tree_val(si)

        # checking if it is not leaf node because if
        # it is leaf node then we cannot go further
        ss, se = self.i_to_se[si]
        if (ss != se):
            # Since we are not yet updating children os si,
            # we need to set lazy values for the children
            self.lazy[self.left(si)] = self.update_lazy_child(self.left(si), si)
            self.lazy[self.right(si)] = self.update_lazy_child(self.right(si), si)

        # unset the lazy value for current node
        # as it has been updated
        self.lazy[si] = None

    def query_range(self, qs, qe, si=0):
        # If lazy flag is set for current node
        # of segment tree, then there are
        # some pending updates. So we need to
        # make sure that the pending updates are
        # done before processing the sub sum query
        self.update_lazy(si)
        if self.out_of_range(qs, qe, si):
            return

        # At this point we are sure that
        # pending lazy updates are done for
        # current node. So we can return value
        # (same as it was for query in our previous post)

        # If this segment lies in range
        if self.covered_in_range(qs, qe, si):
            return self.tree[si]

        # If a part of this segment overlaps
        # with the given range
        left = self.query_range(qs, qe, self.left(si))
        right = self.query_range(qs, qe, self.right(si))
        return self.combine(left, right)

    def update_range(self, us, ue, diff, si=0):
        # If lazy value is non-zero for current node
        # of segment tree, then there are some
        # pending updates. So we need to make sure
        # that the pending updates are done before
        # making new updates. Because this value may be
        # used by parent after recursive calls
        # (See last line of this function)
        self.update_lazy(si)
        if self.out_of_range(us, ue, si):
            return

        # Current segment is fully in range
        if self.covered_in_range(us, ue, si):
            self.lazy[si] = diff
            self.update_lazy(si)
            return
        # If not completely in rang, but overlaps,
        # recur for children,

        self.update_range(us, ue, diff, self.left(si))
        self.update_range(us, ue, diff, self.right(si))

        # And use the result of children calls
        # to update this node
        self.tree[si] = self.combine(self.tree[self.left(si)], self.tree[self.right(si)])





# Driver Code
if __name__ == "__main__":

    arr = [ 1, 2, 3, 4, 5 ]
    mytree = SegTreeRangeSum(arr)

    # Print sum of values in array from index 1 to 3
    print("Sum of values in given range =",
          mytree.query_range(1, 3))

    # Add 10 to all nodes at indexes from 1 to 5.
    mytree.update_range(1, 5, 10)

    # Find sum after the value is updated
    print("Updated sum of values in given range =",
          mytree.query_range(1, 3))

    import random
    random.seed(99)
    for _ in range(3):
        n = random.randint(50, 500)
        arr = [random.randint(0, 9999) for _ in range(n)]
        mytree = SegTreeRangeSum([a for a in arr])
        for t in range(n):
            qs = random.randint(0, n - 1)
            qe = random.randint(0, n - 1)
            qs, qe = min(qs, qe), max(qs, qe)
            us = random.randint(0, n - 1)
            ue = random.randint(0, n - 1)
            us, ue = min(us, ue), max(us, ue)
            d = random.randint(-9999, 9999)
            for i in range(us, ue+1):
                arr[i] += d
            mytree.update_range(us, ue, d)
            v = 0
            for i in range(qs, qe+1):
                v += arr[i]
            myms = mytree.query_range(qs, qe)
            assert myms == v, f'test {t}, {v} != {myms}'

    print('what?')
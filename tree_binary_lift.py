import math


class BinaryLiftTree:
    def __init__(self, edges):
        # Number of nodes
        n = len(edges) + 1
        self.log = math.ceil(math.log(n, 2))

        self.adjs = [[] for _ in range(n)]
        for i, j in edges:
            self.adjs[i].append(j)
            self.adjs[j].append(i)

        self.mem = [[None] * (self.log+1) for _ in range(n)]
        # Stores the level of each node
        self.lev = [0] * n

        self.dfs(0, 0)

    def dfs(self, i, p):

        # Using recursion formula to calculate
        # the values of memo[][]
        self.mem[i][0] = p
        for l in range(1, self.log + 1):
            self.mem[i][l] = self.mem[self.mem[i][l - 1]][l - 1]

        for j in self.adjs[i]:
            if j == p:
                continue
            self.lev[j] = self.lev[i] + 1
            self.dfs(j, i)

    def lca(self, u, v):

        # The node which is present farthest
        # from the root node is taken as u
        # If v is farther from root node
        # then swap the two
        if self.lev[u] < self.lev[v]:
            u, v = v, u

        # Finding the ancestor of u
        # which is at same level as v
        for l in range(self.log, -1, -1):
            if (self.lev[u] - pow(2, l)) >= self.lev[v]:
                u = self.mem[u][l]

        # If v is the ancestor of u
        # then v is the LCA of u and v
        if u == v:
            return v

        # Finding the node closest to the
        # root which is not the common ancestor
        # of u and v i.e. a node x such that x
        # is not the common ancestor of u
        # and v but memo[x][0] is
        for l in range(self.log, -1, -1):
            if self.mem[u][l] != self.mem[v][l]:
                u = self.mem[u][l]
                v = self.mem[v][l]

        # Returning the first ancestor
        # of above found node
        return self.mem[u][0]


# Driver Code
if __name__ == "__main__":
    edges = [
        [0, 1],
        [1, 4],
        [0, 2],
        [2, 5],
        [2, 6],
        [2, 7],
        [0, 3],
        [3, 8],
    ]
    tree = BinaryLiftTree(edges)
    print("The LCA of 5 and 8 is", tree.lca(5, 8))
    print("The LCA of 4 and 8 is", tree.lca(4, 8))
    print("The LCA of 5 and 7 is", tree.lca(5, 7))
    print("The LCA of 5 and 0 is", tree.lca(5, 0))

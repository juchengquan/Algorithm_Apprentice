import functools


@functools.lru_cache(maxsize=None)
def f(n, m):
    if n == 0:
        return 0
    if m == 1:
        return n

    ans = min([max([f(i - 1, m - 1), f(n - i, m)]) for i in range(1, n + 1)]) + 1
    return ans


print(f(100, 2))	# 14
print(f(200, 2))	# 20


def solve(n, m):
    if n < 1 or m < 1:
        return 0

    f = [ [i for i in range(n+1)] for j in range(m+1)]

    for x in range(2, m+1):
        for y in range(1, n+1):
            for k in range(1, y):
                f[x][y] = min(f[x][y], 1 + max(f[x-1][k-1],f[x][y-k]))


    return f[m][n]


def solve_simple(n, m):
    if n < 1 or m < 1:
        return 0

    f_pre = [i for i in range(n+1)]
    f = [i for i in range(n+1)]

    for x in range(2, m+1):
        for y in range(1, n+1):
            for k in range(1, y):
                f[y] = min(f[y], 1 + max(f_pre[k - 1], f[y - k]))

        f_pre = f[:]

    return f[n]



print(solve(5000, 4))
print(solve_simple(5000, 4))

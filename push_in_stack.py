# a = "1043275689"
a = "1043275689"
# a = input().split("")

a = list(a)
a = [int(ele) for ele in a]

def get_what(a):
    p = []
    while len(a) > 0:
        idx = a.index(min(a))
        a.pop(idx)
        p.append(idx)

    for n in range(len(p)-1):
        if p[n] != 0:
            if p[n] <= p[n+1]:
                return False

    return True


def get_stack(a):
    p = [9,8,7,6,5,4,3,2,1,0]
    q = []
    a = a[::-1]
    while len(a) > 0:
        if p[-1] < a[-1]:
            q.append(p.pop())
        elif p[-1] == a[-1]:
            q.append(p.pop())
            while len(a)>0 and len(q)>0 and q[-1] == a[-1]:
                q.pop()
                a.pop()
        elif p[-1] > a[-1]:
            return False

    if len(q) == 0:
        return True
    else:
        return False


print(get_stack(a))

# print(get_what(a))

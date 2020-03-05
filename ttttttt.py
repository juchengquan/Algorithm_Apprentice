a = "5432987610"
# a = input().split("")

a = list(a)
a = [int(ele) for ele in a]


def get_what(a):
    b = len(a)
    while len(a) > 0:
        s = a.pop()
        if s > b:
            return "No"
        elif s < b - 1:
            a.append(s)
            a[s:] = a[s:][::-1]
            print(a)
            s = a.pop()

            if s != b - 1:
                return "No"
            else:
                b = b - 1
        elif s == b - 1:
            b = b - 1
        else:
            return "No"
    return "Yes"


print(get_what(a))

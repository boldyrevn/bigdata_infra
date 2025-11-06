from math import factorial

def c(n, k):
    return factorial(n) / factorial(n - k) / factorial(k)

print(c(39, 6) + c(39, 5) * 13 + c(39, 4) * c(13, 2))

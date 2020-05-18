xk = 1.
a = float(input())
epsilon = float(input())
while True:
    print(xk)
    xk = xk - (xk*xk - a) / (2 * xk)
    if abs(xk*xk - a) <= epsilon:
        break

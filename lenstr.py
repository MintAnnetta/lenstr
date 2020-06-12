from ecmod import EllipticCurveMod, PointMod
import numpy as np
from numpy import gcd
from sage.all import next_prime

#n - факторизуемое число
def lenstr(n):
    #Для выбора модуля, над которым построим эллиптическую кривую,
    #найдём список простых чисел от 1 до n
    i = 1
    pr_list = []
    while i < n:
        i = next_prime(i)
        pr_list.append(i)

    # while gcd(4*a**3+27*b**2, n) == n:
    #     p = np.random.choice(pr_list)
    #     a = np.random.randint(1, p)
    #     b = np.random.randint(1, p)

    #     #Генерируем эллиптическую кривую над модулем p
    #     E = EllipticCurveMod(a, b, p)
    #     print("E:", E)

    #     #Выбираем случайную точку
    #     P = E.random_point()
    #     print("P:", P)

    #Выбираем параметры B и C:
    C = np.random.choice(pr_list)
    B = np.random.choice(pr_list)
    print("Выбраны B={},C={}".format(B, C))

    d = n

    while True:
        a = np.random.randint(1, n)
        b = np.random.randint(1, n)
        E = EllipticCurveMod(a, b, n)
        print("E:", E)

        P = E.random_point()
        print("P:", P)

        if gcd(4*a**3 + 27*b**2, n) !=  1:
            if gcd(4*a**3 + 27*b**2, n) ==  n:
                continue #выбираем другие (E,P)
            d = gcd(4*a**3+27*b**2, n)
            print("Сразу нашли делитель! d =", d)
            return d

        #Найдём k:
        print("Ищем k...")
        i = 3
        i_list = []
        while i < B:
            i_list.append(i)
            i = next_prime(i)

        alpha_i = 0
        alpha_i_list = []
        for i in i_list:
            j = i
            alpha_i = 1
            while j < C:
                alpha_i = alpha_i+1
                j = j*i
            alpha_i_list.append(alpha_i-1)

        k = list(map(lambda x, y: x**y, i_list, alpha_i_list))
        k = np.prod(k, dtype=np.int32)

        print("i:", i_list)
        print("alpha_i", alpha_i_list)
#        k = np.prod(alpha_i_list)
        print("k:", k)

        #kP = k*P
        j = 1
        Q = P
        R = P
        while j <= k:
            try:
                print("Q+P={}+{}".format(Q, P))
                R = Q+P
            #Если не можем найти обратный элемент к знаменателю:
            except ZeroDivisionError:
                if P == Q:
                    d = P.y - Q.y
                    print("{}P=Q+P={}+{}".format(j + 1, Q, P))
                    print("Не найден обратный к (Q.x-P.x)={} по модулю {} при вычислении {}+{}".format(d, E.n, P, Q))

                    if gcd(d, n) == n or gcd(d, n) == 1:
                        print("Найден тривиальный делитель. Выбираем заново (E,P)...\n")
                        break #переходим снова к выбору (E,P)
                    else:
                        print("Нашли делитель! Это НОД(d,n)=НОД({},{})={}".format(d, n, gcd(d, n)))
                        return gcd(d, n)

                else:
                    d = 2*P.y
                    print("{}P=Q+P={}+{}".format(j, Q, P))
                    print("Не найден обратный к 2*Q.y={} по модулю {} при вычислении {}+{}".format(d, E.n, P, Q))
                    if gcd(d, n) == n or gcd(d, n) == 1:
                        print("Найден тривиальный делитель. Выбираем заново (E,P)...\n")
                        break #переходим снова к выбору (E,P)
                    else:
                        print("Нашли делитель! Это НОД(d,n)=НОД({},{})={}".format(d, n, gcd(d, n)))
                        return gcd(d, n)

            #продолжаем обработку исключения
            else:
                print("\b={}".format(Q))
                Q = R
                j = j+1

        # if Q == E.point(0, 1):
        #     break

    return d

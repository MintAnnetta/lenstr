from sage.all import mod, inverse_mod
import numpy as np

class EllipticCurveMod:
    """Задаёт формальную эллиптическую кривую над кольцом (не над полем)"""

    def __init__(self, a, b, n):
        """Конструктор эллиптической кривой.

        a, b - параметры, n - модуль

        """
        self.a = a % n
        self.b = b % n
        self.n = n

    def __repr__(self):
        """Возвращает уравнение в форме Вейерштрасса"""
        return "EllipticCurveMod: y^2=x^3+{}x+{} over {}".format(self.a, self.b, self.n)

    def __str__(self):
        """Выводит уравнение в форме Вейерштрасса"""
        return "y^2=x^3+{}x+{}".format(self.a, self.b)

    def fun(self, x):
        """Вычисление значения уравнения, которым задана эллиптическая кривая"""
        return (x**3+self.a*x+self.b) % self.n

    def point(self, x, y):
        """Создание точки на эллиптической кривой с координатами (x,y)"""
        return PointMod(self.a, self.n, x, y)

    def short_weierstrass_model(self):
        """Выводит уравнение в форме Вейерштрасса"""
        return "y^2=x^3+{}x+{}".format(a, b)

    def is_point(self, point):
        """Возвращает bool значение

        Выясняет, лежит ли точка на данной эллиптической кривой.

        """
        if self.fun(point.x) == (point.y**2 % self.n):
            return True
        return False

    def points(self):
        """Возвращает список точек эллиптической кривой"""
        #Добавим бесконечно удалённую
        p_list = [PointMod(self.a, self.n, 0, 1)]
        for i in range(1, self.n):
            for j in mod(self.fun(i), self.n).sqrt(all=True):
                new_point = PointMod(self.a, self.n, i, j)
                p_list.append(new_point)
        return p_list

    def random_point(self):
        """Возвращает случайную точку на эллиптической кривой"""
        return np.random.choice(self.points())

class PointMod(EllipticCurveMod):
    def __init__(self, a, n, x, y):
        """Конструктор точки на эллиптической кривой"""
        self.a = a #Нужно для удвоения точки
        self.n = n #Модуль
        self.x = int(x) % self.n
        self.y = int(y) % self.n

    def __repr__(self):
        return "PointMod({},{})".format(self.x, self.y)

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __add__(self, other):
        """Оператор сложения точек на эллиптической кривой

        Бесконечно удалённая точка обозначается как (0,1)

        """
        #(x,y)+(0,1)=(x,y)
        if other.x == 0 and other.y == 1:
            return PointMod(self.a, self.n, self.x, self.y)

        #(0,1)+(x,y)=(x,y)
        if self.x == 0 and self.y == 1:
            return PointMod(self.a, self.n, other.x, other.y)

        #(x,y)+(x,-y)=(0,1)
        if self.x == other.x and self.y==-other.y:
            return PointMod(self.a, self.n, 0, 1)

        #(x_1,y_1)+(x_2,y_2), x_1!=x_2
        if other.x != self.x:
            #plambda=((other.y-self.y)//(other.x-self.x)%self.n)
            plambda = ((other.y-self.y)*inverse_mod(other.x-self.x, self.n)) % self.n
            x = -self.x-other.x+plambda**2
            y = -(self.y+(x-self.x)*plambda) #-y_3
            return PointMod(self.a, self.n, x, y)

        #(x_0,y_1)+(x_0,y_2), y_1!=-y_2 => y_1=y_2
        if self.y != -other.y % self.n:
            #x_0=self.x=other.x
            #y_1!=-y_2=>y_0=y_1=y_2

            #(3*(x_0)^2+a)//2*y_0
            plambda = ((3*self.x**2+self.a)*inverse_mod(2*self.y, self.n)) % self.n
            #x_3=-2*x_0+plambda^2
            x = -2*self.x+plambda**2
            #y_0+plambda*(x_3-x_0)
            y = -(self.y+plambda*(x-self.x))
            return PointMod(self.a,self.n,x,y)

        return PointMod(self.a,self.n,0,1)

    def __mul__(self, other):
        """Возвращает точку, умноженную на число

        Второй аргумент может быть только числом.

        """
        if type(other) != int:
            return self
        i = 1
        res = self
        while i < other:
            res = res+self
            i = i+1
        return res

    def __eq__(self, other):
        """Проверяет две точки на равенство"""
        if self.x == other.x and self.y == other.y:
            return True
        return False

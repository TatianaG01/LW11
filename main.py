from math import gcd

# 7.3.1 - Власний виняток
class RationalError(ZeroDivisionError):
    pass

# 7.3.2 - Інший виняток
class RationalValueError(ValueError):
    pass

class Rational:
    def __init__(self, *args):
        if len(args) == 2:
            n, d = args
        elif len(args) == 1 and isinstance(args[0], str):
            n, d = map(int, args[0].split('/'))
        else:
            raise RationalValueError("Некоректні дані для створення Rational")

        if d == 0:
            raise RationalError("Знаменник не може дорівнювати нулю")

        common = gcd(n, d)
        self.n = n // common
        self.d = d // common

    def __add__(self, other):
        if isinstance(other, Rational):
            n = self.n * other.d + other.n * self.d
            d = self.d * other.d
            return Rational(n, d)
        elif isinstance(other, int):
            return Rational(self.n + other * self.d, self.d)
        else:
            raise RationalValueError("Некоректне додавання")

    def __sub__(self, other):
        if isinstance(other, Rational):
            n = self.n * other.d - other.n * self.d
            d = self.d * other.d
            return Rational(n, d)
        elif isinstance(other, int):
            return Rational(self.n - other * self.d, self.d)
        else:
            raise RationalValueError("Некоректне віднімання")

    def __mul__(self, other):
        if isinstance(other, Rational):
            return Rational(self.n * other.n, self.d * other.d)
        elif isinstance(other, int):
            return Rational(self.n * other, self.d)
        else:
            raise RationalValueError("Некоректне множення")

    def __truediv__(self, other):
        if isinstance(other, Rational):
            if other.n == 0:
                raise RationalError("Ділення на нуль")
            return Rational(self.n * other.d, self.d * other.n)
        elif isinstance(other, int):
            if other == 0:
                raise RationalError("Ділення на нуль")
            return Rational(self.n, self.d * other)
        else:
            raise RationalValueError("Некоректне ділення")

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == 'n':
            return self.n
        elif key == 'd':
            return self.d
        else:
            raise KeyError("Доступ тільки за ключами 'n' та 'd'")

    def __setitem__(self, key, value):
        if not isinstance(value, int):
            raise RationalValueError("Чисельник і знаменник повинні бути цілими числами")

        if key == 'n':
            self.n = value
        elif key == 'd':
            if value == 0:
                raise RationalError("Знаменник не може бути нулем")
            self.d = value
        else:
            raise KeyError("Доступ тільки за ключами 'n' та 'd'")

        common = gcd(self.n, self.d)
        self.n //= common
        self.d //= common

    def __str__(self):
        return f"{self.n}/{self.d}"

class RationalList:
    def __init__(self):
        self.data = []

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self.data[index] = value
        else:
            raise RationalValueError("У список можна додавати лише Rational")

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        new_list = RationalList()
        new_list.data = self.data.copy()

        if isinstance(other, RationalList):
            new_list.data += other.data
        elif isinstance(other, Rational):
            new_list.data.append(other)
        elif isinstance(other, int):
            new_list.data.append(Rational(other, 1))
        else:
            raise RationalValueError("Некоректне додавання до списку")

        return new_list

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            self.data += other.data
        elif isinstance(other, Rational):
            self.data.append(other)
        elif isinstance(other, int):
            self.data.append(Rational(other, 1))
        else:
            raise RationalValueError("Некоректне додавання до списку")

        return self

    def append(self, value):
        if isinstance(value, Rational):
            self.data.append(value)
        else:
            raise RationalValueError("У список можна додавати лише Rational")

    def sum(self):
        result = Rational(0, 1)
        for r in self.data:
            result += r
        return result

# Додано для обробки вхідного файлу і запису у вихідний

def evaluate_expression(expr):
    tokens = expr.strip().split()
    stack = []
    op = None

    for token in tokens:
        if '/' in token:
            num = Rational(token)
        elif token in ('+', '-', '*', '/'):
            op = token
            continue
        else:
            num = Rational(int(token), 1)

        if not stack:
            stack.append(num)
        elif op:
            a = stack.pop()
            if op == '+':
                stack.append(a + num)
            elif op == '-':
                stack.append(a - num)
            elif op == '*':
                stack.append(a * num)
            elif op == '/':
                stack.append(a / num)

            op = None

    return stack[0]

# Зчитування виразів та запис результатів
with open('input.txt', 'r', encoding='utf-8') as fin, open('output.txt', 'w', encoding='utf-8') as fout:
    for line in fin:
        try:
            result = evaluate_expression(line)
            fout.write(f"{line.strip()} = {result}\n")
        except Exception as e:
            fout.write(f"{line.strip()} => Помилка: {e}\n")
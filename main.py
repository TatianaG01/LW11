def generate_sequence(n):
    # Ініціалізуємо список з n елементів
    a = [0] * n
    # Початкові умови
    a[0] = a[1] = a[2] = 1
    # Генерація послідовності за рекурентною формулою
    for k in range(3, n):
        a[k] = a[k - 1] + a[k - 3]
    return a


def calculate_sum(n):
    a = generate_sequence(n)
    S_n = 0
    for k in range(n):
        S_n += a[k] / (2 ** (k + 1))  # Враховуємо, що k починається з 0
    return S_n


# Зчитування значення n з файлу
with open('input.txt', 'r', encoding='utf-8') as f:
    n = int(f.read().strip())

# Обчислення суми
result = calculate_sum(n)

# Запис результату у файл
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(f"S_{n} = {result}\n")
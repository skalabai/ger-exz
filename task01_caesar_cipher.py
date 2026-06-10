"""
Задание 1. Шифр Цезаря (русский алфавит).

Идея шифра:
    Каждая буква заменяется на букву, стоящую на k позиций дальше в алфавите.
    Если выходим за конец алфавита — продолжаем с начала (операция mod).

Пример:
    При сдвиге 3 буква 'а' (позиция 0) становится 'г' (позиция 3).

Расшифровка:
    Это то же шифрование, но со сдвигом -k (или +30 при 33 буквах).
"""

# Строчный русский алфавит из 33 букв (включая 'ё' после 'е')
RU_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

# Заглавный русский алфавит — тот же порядок букв
RU_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# Размер алфавита нужен для операции mod при сдвиге
ALPHABET_SIZE = len(RU_LOWER)  # 33


def caesar_encrypt(text: str, shift: int, verbose: bool = False) -> str:
    """
    Шифрует текст шифром Цезаря для русского алфавита.

    Параметры:
        text   — исходный текст
        shift  — величина сдвига (ключ шифрования)
        verbose — если True, печатает каждый шаг вычисления

    Возвращает:
        Зашифрованную строку
    """
    result = []  # сюда собираем зашифрованные символы

    # Нормализуем сдвиг: например, сдвиг 35 при алфавите 33 = сдвиг 2
    shift = shift % ALPHABET_SIZE

    if verbose:
        print(f"\n[Переменные]")
        print(f"  text  = '{text}'           — исходный текст (ввод пользователя)")
        print(f"  shift = {shift} % {ALPHABET_SIZE} = {shift % ALPHABET_SIZE}  — нормализованный ключ")
        print(f"  ALPHABET_SIZE = {ALPHABET_SIZE}  — длина русского алфавита")
        print(f"  Алфавит: {RU_LOWER}")
        print("\n[Поиск каждой буквы] pos -> (pos+shift) mod 33 -> новая буква:")

    # Обрабатываем каждый символ текста по отдельности
    for char in text:
        if char in RU_UPPER:
            # Заглавная русская буква: ищем позицию в RU_UPPER
            pos = RU_UPPER.index(char)
            # Новая позиция = (старая + сдвиг) mod 33
            new_char = RU_UPPER[(pos + shift) % ALPHABET_SIZE]
            if verbose:
                new_pos = (pos + shift) % ALPHABET_SIZE
                print(f"  '{char}': ищем pos в алфавите -> pos={pos}")
                print(f"         new_pos = (pos+shift) mod {ALPHABET_SIZE} = ({pos}+{shift}) mod {ALPHABET_SIZE} = {new_pos}")
                print(f"         new_char = алфавит[{new_pos}] = '{new_char}'")
            result.append(new_char)

        elif char in RU_LOWER:
            # Строчная русская буква — аналогично, но в RU_LOWER
            pos = RU_LOWER.index(char)
            new_char = RU_LOWER[(pos + shift) % ALPHABET_SIZE]
            if verbose:
                new_pos = (pos + shift) % ALPHABET_SIZE
                print(f"  '{char}': ищем pos в алфавите -> pos={pos}")
                print(f"         new_pos = (pos+shift) mod {ALPHABET_SIZE} = ({pos}+{shift}) mod {ALPHABET_SIZE} = {new_pos}")
                print(f"         new_char = алфавит[{new_pos}] = '{new_char}'")
            result.append(new_char)

        else:
            # Пробелы, цифры, знаки препинания, латиница — не шифруем
            if verbose:
                print(f"  '{char}' -> не русская буква, без изменений")
            result.append(char)

    # Склеиваем список символов в одну строку
    return "".join(result)


def caesar_decrypt(text: str, shift: int, verbose: bool = False) -> str:
    """
    Расшифровывает текст шифром Цезаря.

    Расшифровка = шифрование с обратным сдвигом (-shift).
    Это работает потому что: (pos + k - k) mod 33 = pos.
    """
    if verbose:
        print(f"\nРасшифровка: сдвиг на {-shift % ALPHABET_SIZE}")
    return caesar_encrypt(text, -shift, verbose=verbose)


# Точка входа программы — запускается при вызове: python task01_caesar_cipher.py
if __name__ == "__main__":
    print("=== Шифр Цезаря (русский алфавит) ===")

    # Запрашиваем данные у пользователя через консоль
    text = input("Введите текст: ")
    shift = int(input("Введите ключ (сдвиг): "))
    action = input("Действие (1 — шифровать, 2 — расшифровать): ").strip()

    if action == "1":
        print("\n--- ШИФРОВАНИЕ ---")
        result = caesar_encrypt(text, shift, verbose=True)
        print(f"\nИтоговый шифротекст: {result}")
    else:
        print("\n--- РАСШИФРОВАНИЕ ---")
        result = caesar_decrypt(text, shift, verbose=True)
        print(f"\nИтоговый текст: {result}")

"""
Задание 1. Шифр Цезаря (русский алфавит).
Сдвигаем каждую русскую букву на фиксированное число позиций (mod 33).
"""

RU_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_SIZE = len(RU_LOWER)


def caesar_encrypt(text: str, shift: int) -> str:
    """Шифрует текст шифром Цезаря."""
    result = []
    shift = shift % ALPHABET_SIZE
    for char in text:
        if char in RU_UPPER:
            pos = RU_UPPER.index(char)
            result.append(RU_UPPER[(pos + shift) % ALPHABET_SIZE])
        elif char in RU_LOWER:
            pos = RU_LOWER.index(char)
            result.append(RU_LOWER[(pos + shift) % ALPHABET_SIZE])
        else:
            result.append(char)
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """Расшифровка — сдвиг в обратную сторону."""
    return caesar_encrypt(text, -shift)


if __name__ == "__main__":
    print("=== Шифр Цезаря (русский алфавит) ===")
    text = input("Введите текст: ")
    shift = int(input("Введите ключ (сдвиг): "))
    action = input("Действие (1 — шифровать, 2 — расшифровать): ").strip()

    norm_shift = shift % ALPHABET_SIZE
    print(f"\nСдвиг (нормализованный): {norm_shift}")

    if action == "1":
        result = caesar_encrypt(text, shift)
        print(f"Шифротекст: {result}")
    else:
        result = caesar_decrypt(text, shift)
        print(f"Расшифрованный текст: {result}")

"""
Задание 1. Шифр Цезаря.
Сдвигаем каждую букву алфавита на фиксированное число позиций.
"""


def caesar_encrypt(text: str, shift: int, verbose: bool = False) -> str:
    """Шифрует текст шифром Цезаря."""
    result = []
    shift = shift % 26

    if verbose:
        print(f"\nНормализованный сдвиг: {shift}")
        print("Пошаговое шифрование:")

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            pos = ord(char) - base
            new_pos = (pos + shift) % 26
            encrypted_char = chr(new_pos + base)
            if verbose:
                print(f"  '{char}' -> позиция {pos} + {shift} = {new_pos} mod 26 -> '{encrypted_char}'")
            result.append(encrypted_char)
        else:
            if verbose:
                print(f"  '{char}' -> не буква, без изменений")
            result.append(char)

    return ''.join(result)


def caesar_decrypt(text: str, shift: int, verbose: bool = False) -> str:
    """Расшифровка — сдвиг в обратную сторону."""
    if verbose:
        print(f"\nРасшифровка: сдвиг на {-shift % 26}")
    return caesar_encrypt(text, -shift, verbose=verbose)


if __name__ == "__main__":
    print("=== Шифр Цезаря ===")
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

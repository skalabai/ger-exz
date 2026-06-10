"""
Задание 1. Шифр Цезаря.
Сдвигаем каждую букву алфавита на фиксированное число позиций.
"""


def caesar_encrypt(text: str, shift: int) -> str:
    """
    Шифрует текст шифром Цезаря.
    shift — величина сдвига (ключ).
    """
    result = []
    # Нормализуем сдвиг в диапазон 0..25
    shift = shift % 26

    for char in text:
        if char.isalpha():
            # Определяем базу: 'A' для заглавных, 'a' для строчных
            base = ord('A') if char.isupper() else ord('a')
            # Переводим букву в номер 0..25, сдвигаем и обратно в символ
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted_char)
        else:
            # Пробелы, цифры и знаки препинания не меняем
            result.append(char)

    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """
    Расшифровка — это шифрование со сдвигом в обратную сторону.
    """
    return caesar_encrypt(text, -shift)


if __name__ == "__main__":
    message = "Hello, World!"
    key = 3

    encrypted = caesar_encrypt(message, key)
    decrypted = caesar_decrypt(encrypted, key)

    print("Исходный текст:", message)
    print("Зашифрованный:", encrypted)
    print("Расшифрованный:", decrypted)

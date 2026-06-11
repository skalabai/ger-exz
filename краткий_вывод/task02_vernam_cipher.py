"""
Задание 2. Шифр Вернама (одноразовый блокнот, XOR).
Каждый символ текста XOR-ится с символом ключа той же длины.
"""


def vernam_encrypt(text: str, key: str) -> str:
    """Шифрует текст методом Вернама."""
    if len(text) != len(key):
        raise ValueError("Длина ключа должна совпадать с длиной сообщения")
    return "".join(chr(ord(t) ^ ord(k)) for t, k in zip(text, key))


def vernam_decrypt(ciphertext: str, key: str) -> str:
    """Расшифровка — повторный XOR с тем же ключом."""
    return vernam_encrypt(ciphertext, key)


if __name__ == "__main__":
    print("=== Шифр Вернама ===")
    text = input("Введите текст: ")
    key = input("Введите ключ (той же длины): ")
    action = input("Действие (1 — шифровать, 2 — расшифровать): ").strip()

    if len(text) != len(key):
        print(f"Ошибка: длина текста ({len(text)}) != длина ключа ({len(key)})")
    elif action == "1":
        result = vernam_encrypt(text, key)
        print(f"\nШифротекст: {result}")
        print(f"Коды: {[ord(c) for c in result]}")
    else:
        result = vernam_decrypt(text, key)
        print(f"\nРасшифрованный текст: {result}")

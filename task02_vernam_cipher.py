"""
Задание 2. Шифр Вернама (одноразовый блокнот, XOR).
Каждый символ текста XOR-ится с символом ключа.
"""


def vernam_encrypt(text: str, key: str, verbose: bool = False) -> str:
    """Шифрует текст методом Вернама."""
    if len(text) != len(key):
        raise ValueError("Длина ключа должна совпадать с длиной сообщения")

    result = []
    if verbose:
        print("\nПошаговое XOR-шифрование:")
        print(f"{'Символ':<8} {'Код':<6} {'Ключ':<8} {'Код':<6} {'XOR':<6} {'Результат'}")

    for t_char, k_char in zip(text, key):
        t_code = ord(t_char)
        k_code = ord(k_char)
        encrypted_byte = t_code ^ k_code
        enc_char = chr(encrypted_byte)
        if verbose:
            print(f"'{t_char}'     {t_code:<6} '{k_char}'     {k_code:<6} {encrypted_byte:<6} '{enc_char}'")
        result.append(enc_char)

    return ''.join(result)


def vernam_decrypt(ciphertext: str, key: str, verbose: bool = False) -> str:
    """Расшифровка — повторный XOR с тем же ключом."""
    if verbose:
        print("\nРасшифровка (повторный XOR):")
    return vernam_encrypt(ciphertext, key, verbose=verbose)


if __name__ == "__main__":
    print("=== Шифр Вернама ===")
    text = input("Введите текст: ")
    key = input("Введите ключ (той же длины): ")
    action = input("Действие (1 — шифровать, 2 — расшифровать): ").strip()

    if len(text) != len(key):
        print(f"Ошибка: длина текста ({len(text)}) != длина ключа ({len(key)})")
    elif action == "1":
        print("\n--- ШИФРОВАНИЕ ---")
        result = vernam_encrypt(text, key, verbose=True)
        print(f"\nШифротекст (символы): {result}")
        print(f"Шифротекст (коды):    {[ord(c) for c in result]}")
    else:
        print("\n--- РАСШИФРОВАНИЕ ---")
        result = vernam_decrypt(text, key, verbose=True)
        print(f"\nРасшифрованный текст: {result}")

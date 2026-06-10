"""
Задание 2. Шифр Вернама (одноразовый блокнот, XOR).
Каждый символ текста складывается по модулю 2 (XOR) с символом ключа.
Ключ должен быть случайным и той же длины, что и сообщение.
"""


def vernam_encrypt(text: str, key: str) -> str:
    """
    Шифрует текст методом Вернама.
    text и key должны быть одинаковой длины.
    """
    if len(text) != len(key):
        raise ValueError("Длина ключа должна совпадать с длиной сообщения")

    result = []
    for t_char, k_char in zip(text, key):
        # XOR кодов символов даёт зашифрованный байт/символ
        encrypted_byte = ord(t_char) ^ ord(k_char)
        result.append(chr(encrypted_byte))

    return ''.join(result)


def vernam_decrypt(ciphertext: str, key: str) -> str:
    """
    Расшифровка идентична шифрованию: повторный XOR с тем же ключом
  возвращает исходный текст.
    """
    return vernam_encrypt(ciphertext, key)


if __name__ == "__main__":
    message = "SECRET"
    # В реальности ключ генерируют криптографически стойким ГПСЧ
    key = "Xk9#mQ"

    encrypted = vernam_encrypt(message, key)
    decrypted = vernam_decrypt(encrypted, key)

    print("Исходный текст:", message)
    print("Ключ:", key)
    print("Зашифрованный (коды):", [ord(c) for c in encrypted])
    print("Расшифрованный:", decrypted)

import time
import random
from Lab1 import lab1
from Lab2 import lab2


class RC5:
    # Конструктор класу з основними параметрами: розмір слова, кількість раундів, та ключем
    def __init__(self, w, R, key, init_vector, strip_extra_nulls=False):
        self.w = w  # Розмір слова. Розмір блоку буде вдвіччі більший за розмір слова (32б 64б 128 бітів)
        self.R = R  # Кількість раундів (0 - 255)
        self.key = key  # Ключ
        self.strip_extra_nulls = strip_extra_nulls
        # Додаткові корисні константи
        self.T = 2 * (R + 1)
        self.w4 = w // 4
        self.w8 = w // 8
        self.mod = 2 ** self.w
        self.mask = self.mod - 1
        self.b = len(key)

        self.init_vector = init_vector

        # Методи розширення ключа
        self.__keyAlign()  # Вирівнювання
        self.__keyExtend()  # Розширення
        self.__shuffle()  # Перемішування

    # Логічний зсув вліво
    def __lshift(self, val, n):
        n %= self.w
        return ((val << n) & self.mask) | ((val & self.mask) >> (self.w - n))

    # Логічний зсув вправо
    def __rshift(self, val, n):
        n %= self.w
        return ((val & self.mask) >> n) | (val << (self.w - n) & self.mask)

    # Вирівнювання ключа
    def __keyAlign(self):
        if self.b == 0:  # Пустий ключ
            self.c = 1
        elif self.b % self.w8:  # Не кратний w / 8
            self.key += b'\x00' * (self.w8 - self.b % self.w8)  # Доповнюємо ключ нульовими байтами \x00
            self.b = len(self.key)
            self.c = self.b // self.w8
        else:
            self.c = self.b // self.w8
        L = [0] * self.c
        for i in range(self.b - 1, -1, -1):  # Заповнюємо масив L
            L[i // self.w8] = (L[i // self.w8] << 8) + self.key[i]
        self.L = L

    # Розширення ключа
    def __keyExtend(self):
        # Генеруємо масив за допомогою генератора псевдовипадкових чисел
        numbers = lab1.random_num_generator(600, self.init_vector, 6 ** 5, 5, 2 ** 14 - 1)
        self.S = [numbers[i] for i in range(self.T)]  # Заповнюємо масив S
        # print(self.S)

    # Перемішування L та S
    def __shuffle(self):
        i, j, A, B = 0, 0, 0, 0
        for k in range(3 * max(self.c, self.T)):
            A = self.S[i] = self.__lshift((self.S[i] + A + B), 3)
            B = self.L[j] = self.__lshift((self.L[j] + A + B), A + B)
            i = (i + 1) % self.T
            j = (j + 1) % self.c

    def encryptBlock(self, data):
        A = int.from_bytes(data[:self.w8], byteorder='little')
        B = int.from_bytes(data[self.w8:], byteorder='little')
        A = (A + self.S[0]) % self.mod
        B = (B + self.S[1]) % self.mod
        for i in range(1, self.R + 1):
            A = (self.__lshift((A ^ B), B) + self.S[2 * i]) % self.mod
            B = (self.__lshift((A ^ B), A) + self.S[2 * i + 1]) % self.mod
        return A.to_bytes(self.w8, byteorder='little') + B.to_bytes(self.w8, byteorder='little')

    def decryptBlock(self, data):
        A = int.from_bytes(data[:self.w8], byteorder='little')
        B = int.from_bytes(data[self.w8:], byteorder='little')
        for i in range(self.R, 0, -1):
            B = self.__rshift(B - self.S[2 * i + 1], A) ^ A
            A = self.__rshift(A - self.S[2 * i], B) ^ B
        B = (B - self.S[1]) % self.mod
        A = (A - self.S[0]) % self.mod
        return A.to_bytes(self.w8, byteorder='little') + B.to_bytes(self.w8, byteorder='little')

    # Шифрування фалу
    def encryptFile(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            run = True
            while run:
                text = inp.read(self.w4)
                if not text:
                    break
                if len(text) != self.w4:
                    text = text.ljust(self.w4, b'\x00')
                    run = False
                text = self.encryptBlock(text)
                out.write(text)

    # Дешифрування файлу
    def decryptFile(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            while True:
                text = inp.read(self.w4)
                if not text:
                    break
                text = self.decryptBlock(text)
                if self.strip_extra_nulls:
                    text = text.rstrip(b'\x00')
                out.write(text)


if __name__ == '__main__':
    while True:
        init_vector = random.randint(1, 10000)
        print("Please, choose action: ")
        print("(1) - Cipher file")
        print("(2) - Decipher file")
        print("(3) - Exit")
        command = int(input())
        if command == 1:
            user_key = input("Please enter KEY: ")
            user_key = user_key.encode()
            hashed_key = lab2.md5_hashing(user_key)
            hashed_key = hashed_key.encode()
            rc5_obj = RC5(32, 8, hashed_key, init_vector)
            start_time1 = time.time()
            rc5_obj.encryptFile('message.txt', 'encrypted.txt')
            end_time1 = time.time()
        elif command == 2:
            check_key = input('Please re-enter KEY: ')
            check_key = check_key.encode()
            hashed_checked_key = lab2.md5_hashing(check_key)
            hashed_checked_key = hashed_checked_key.encode()
            rc5_check_obj = RC5(32, 8, hashed_checked_key, init_vector, True)
            start_time2 = time.time()
            rc5_check_obj.decryptFile('encrypted.txt', 'decrypted.txt')
            end_time2 = time.time()
        else:
            time = (end_time2 - start_time2) + (end_time1 - start_time1)
            print("Working time: " + str(time))
            print("Thanks for using our product!")
            break

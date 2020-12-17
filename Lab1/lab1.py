# def period(random_list):  # Функція для обрахунку періоду
#     period = "Not Found"
#     for i in range(1, len(random_list)):  # Шукаємо перше співпадіння з першим елементом
#         if random_list[0] == random_list[i]:
#             period = str(i)
#             break
#     return period


def random_num_generator(length, x0, a, c, m):  # Основна функція генерування псевдовипадкових чисел
    random_list = []
    random_list.append(x0)
    x_temp = (a * x0 + c) % m
    for i in range(length):
        x_temp = (a * x_temp + c) % m  # Генерування числа, використовуючи алгоритм лінійного порівняння
        random_list.append(x_temp)
    # while len(random_list) != length:
    #     with open(file, 'w') as f:  # Записування чисел та періоду у файл
    #         f.write("Random numbers: ")
    #         for elem in random_list:
    #             f.write(str(elem) + " ")
    #         f.write("\nPeriod: " + period(random_list))
    return random_list


# print("Please, input length of the random number:")
# length = int(input())
# x0 = 32  # Початкове значення
# a = 6 ** 5  # Множник
# c = 5  # Приріст
# m = 2 ** 14 - 1  # Модуль порівняння
# random_list = random_num_generator(length, x0, a, c, m, "random_number.txt")
# print("Random numbers:" + str(random_list))
# print("Period: " + period(random_list))

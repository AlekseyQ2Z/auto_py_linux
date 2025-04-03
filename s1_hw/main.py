#Задание 1.
#Условие:
#Написать функцию на Python, которой передаются в качестве параметров команда и текст. 
#Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае. 
#Передаваться должна только одна строка, разбиение вывода использовать не нужно.

#Задание 2. (повышенной сложности)
#Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы, 
#в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка string.punctuation модуля string). 
#В этом режиме должно проверяться наличие слова в выводе.

import subprocess
import string


def checkout1(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkout2(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    # Deleting characters
    result_deleted_chars = ''.join(c for c in result.stdout if c not in string.punctuation)
    print(result_deleted_chars)
    if text in result_deleted_chars and result.returncode == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    # Package Installation Test1
    if checkout1("dpkg -s python3", "installed"):
        print("test1 SUCCESS")
    else:
        print("test1 FAIL")

    # Package Installation Test2
    if checkout2("dpkg -s python3", "Status install ok installed"):
        print("test2 SUCCESS")
    else:
        print("test2 FAIL")
import os
import subprocess
import yaml
from checkout import checkout_positive

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step1(make_folders, clear_folders, make_files, make_stat, make_stat2):
    """Тест создания архива"""
    # Создаем архив с указанием типа
    cmd = f"cd {data['folder_in']}; 7z a -t{data['archive_type']} {data['folder_out']}/arx1.7z"
    res1 = checkout_positive(cmd, "Everything is Ok")
    # Проверяем наличие архива
    res2 = checkout_positive(f"ls {data['folder_out']}", "arx1.7z")
    assert res1 and res2, "Не удалось создать архив или архив не найден"


def test_step2(clear_folders, make_files, make_stat, make_stat2):
    """Тест извлечения файлов из архива"""
    res = []
    # Создаем архив
    cmd_create = f"cd {data['folder_in']}; 7z a -t{data['archive_type']} {data['folder_out']}/arx1.7z"
    res.append(checkout_positive(cmd_create, "Everything is Ok"))
    # Извлекаем файлы
    cmd_extract = f"cd {data['folder_out']}; 7z e -t{data['archive_type']} arx1.7z -o{data['folder_ext']} -y"
    res.append(checkout_positive(cmd_extract, "Everything is Ok"))
    # Проверяем извлеченные файлы
    for item in make_files:
        res.append(checkout_positive(f"ls {data['folder_ext']}", item))
    assert all(res), "Ошибка при извлечении файлов из архива"


def test_step3(make_files, make_stat, make_stat2):
    """Проверка целостности архива"""
    archive_path = f"{data['folder_out']}/arx1.7z"
    assert os.path.exists(archive_path), f"Архив {archive_path} не найден"

    # Проверяем содержимое архива
    res = subprocess.run(
        f"7z l -t{data['archive_type']} {archive_path}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'
    )
    assert "4 files" in res.stdout, f"В архиве должно быть 4 файла. Вывод: {res.stdout}"

    # Проверяем целостность
    cmd_check = f"7z t -t{data['archive_type']} {archive_path}"
    assert checkout_positive(cmd_check, "Everything is Ok"), "Ошибка проверки целостности архива"


def test_step4(make_stat, make_stat2):
    """Тест обновления архива"""
    cmd = f"cd {data['folder_in']}; 7z u -t{data['archive_type']} {data['folder_out']}/arx1.7z"
    assert checkout_positive(cmd, "Everything is Ok"), "Ошибка обновления архива"


def test_step5(clear_folders, make_files, make_stat, make_stat2):
    """Тест просмотра содержимого архива"""
    res = []
    # Создаем архив
    cmd_create = f"cd {data['folder_in']}; 7z a -t{data['archive_type']} {data['folder_out']}/arx1.7z"
    res.append(checkout_positive(cmd_create, "Everything is Ok"))
    # Проверяем список файлов в архиве
    for item in make_files:
        cmd_list = f"cd {data['folder_out']}; 7z l -t{data['archive_type']} arx1.7z"
        res.append(checkout_positive(cmd_list, item))
    assert all(res), "Ошибка при проверке содержимого архива"


def test_step7(make_stat, make_stat2):
    """Тест удаления файлов из архива"""
    cmd = f"7z d -t{data['archive_type']} {data['folder_out']}/arx1.7z"
    assert checkout_positive(cmd, "Everything is Ok"), "Ошибка удаления файлов из архива"
import random
import string
import subprocess
import pytest
import yaml
from datetime import datetime
import os
from pathlib import Path
from checkout import checkout_negative

# Создаём папку для отчётов
REPORTS_DIR = Path(__file__).parent / "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

from checkout import checkout_positive
with open('config.yaml') as f:
    data = yaml.safe_load(f)

# Создаёт директории
@pytest.fixture()
def make_folders():
    """Фикстура для создания всех необходимых директорий"""
    folders = [
        data["folder_in"],
        data["folder_out"],
        data["folder_ext"],
        data["folder_badarx"]
    ]
    for folder in folders:
        checkout_positive(f"mkdir -p {folder}", "")
    return True

# Очищает директории
@pytest.fixture()
def clear_folders():
    folders = [
        data["folder_in"],
        data["folder_out"],
        data["folder_ext"],
        data["folder_badarx"]
    ]
    for folder in folders:
        checkout_positive(f"rm -rf {folder}/*", "")
    yield
    for folder in folders:
        checkout_positive(f"rm -rf {folder}/*", "")

# Генерирует файлы и архив (с указанием типа архива)
@pytest.fixture()
def make_files():
    # Очищаем папки
    checkout_positive(f"mkdir -p {data['folder_in']} {data['folder_out']}", "")
    checkout_positive(f"rm -rf {data['folder_in']}/* {data['folder_out']}/*", "")

    # Создаём текстовые тестовые файлы вместо бинарных
    for i in range(data["count_file"]):
        filename = f"testfile_{i}.txt"
        checkout_positive(
            f"cd {data['folder_in']}; "
            f"echo 'Test file content {i}' > {filename}", "")

    # Создаём архив
    cmd = f"cd {data['folder_in']}; 7z a -t{data['archive_type']} {data['folder_out']}/arx1.7z *.txt"
    assert checkout_positive(cmd, "Everything is Ok"), "Ошибка создания архива"

    return [f"testfile_{i}.txt" for i in range(data["count_file"])]

# Создание поддиректории с файлом
@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout_positive(f"cd {data['folder_in']}; mkdir {subfoldername}", ""):
        return None, None
    if not checkout_positive(
            f"cd {data['folder_in']}/{subfoldername}; "
            f"dd if=/dev/urandom of={testfilename} bs=1M count=1", ""):
        return subfoldername, None
    return subfoldername, testfilename

# Создание повреждённого архива
@pytest.fixture()
def make_badarx(make_folders):
    """Фикстура для создания действительно повреждённого архива"""
    bad_archive = f"{data['folder_badarx']}/badarx.7z"

    # 1. Создаём полностью случайный бинарный файл
    checkout_positive(
        f"dd if=/dev/urandom of={bad_archive} bs=1K count=10",
        "")

    # 2. Проверяем, что архив действительно повреждён
    if not checkout_negative(f"7z t {bad_archive}", "ERROR"):
        pytest.fail("Созданный архив не повреждён, тесты будут невалидными")

    return True

# Фикстура для записи статистики (усовершенствованная)
@pytest.fixture()
def make_stat():
    stat_file = REPORTS_DIR / "stat.txt"
    with open(stat_file, "a") as f:
        f.write(f"\n=== Test at {datetime.now()} ===\n")
        f.write(f"Files count: {data['count_file']}\n")
        f.write(f"File size: {data['size_file']}\n")
        with open("/proc/loadavg") as load_file:
            f.write(f"CPU load: {load_file.read()}\n")

# Альтернативная фикстура статистики
@pytest.fixture()
def make_stat2():
    stat_file = Path(data["stat_alt"]) / "stat_alt.txt"
    os.makedirs(data["stat_alt"], exist_ok=True)
    with open(stat_file, "a") as f:
        f.write(f"\n=== Test at {datetime.now()} ===\n")
        f.write(f"Files count: {data['count_file']}\n")
        f.write(f"File size: {data['size_file']}\n")
        with open("/proc/loadavg") as load_file:
            f.write(f"CPU load: {load_file.read()}\n")
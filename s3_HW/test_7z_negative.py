import os
import subprocess
import pytest
import yaml
from checkout import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step1(clear_folders, make_files, make_badarx):
    """Тест извлечения из повреждённого архива"""
    bad_archive = f"{data['folder_badarx']}/badarx.7z"
    assert os.path.exists(bad_archive), "Повреждённый архив не найден"

    cmd = f"7z e -t{data['archive_type']} {bad_archive} -o{data['folder_ext']} -y"
    result = subprocess.run(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    # Проверяем конкретные сообщения об ошибках
    error_messages = [
        "Can not open the file as [7z] archive",
        "Is not archive",
        "ERROR"
    ]

    output = result.stdout + result.stderr
    assert any(err in output for err in error_messages), (
        f"Не получена ожидаемая ошибка. Вывод:\n{output}"
    )


def test_step2(clear_folders, make_files, make_badarx):
    """Тест проверки повреждённого архива"""
    bad_archive = f"{data['folder_badarx']}/badarx.7z"
    assert os.path.exists(bad_archive), "Повреждённый архив не найден"

    cmd = f"7z t -t{data['archive_type']} {bad_archive}"
    result = subprocess.run(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8')

    # Проверяем конкретные сообщения об ошибках
    error_messages = [
        "Can not open the file as [7z] archive",
        "Is not archive",
        "ERROR"
    ]

    output = result.stdout + result.stderr
    assert any(err in output for err in error_messages), (
        f"Не получена ожидаемая ошибка. Вывод:\n{output}"
    )
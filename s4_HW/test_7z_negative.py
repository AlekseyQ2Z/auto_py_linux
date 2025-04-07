import os
import pytest
import yaml
from checkout import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)

def test_step1(clear_folders, make_files, make_badarx):
    """Тест извлечения из повреждённого архива"""
    bad_archive = f"{data['folder_badarx']}/badarx.7z"
    assert checkout_positive(f"test -f {bad_archive}", ""), "Повреждённый архив не найден"

    cmd = f"7z e -t{data['archive_type']} {bad_archive} -o{data['folder_ext']} -y"
    assert checkout_negative(cmd, "ERROR"), "Не получена ожидаемая ошибка"

def test_step2(clear_folders, make_files, make_badarx):
    """Тест проверки повреждённого архива"""
    bad_archive = f"{data['folder_badarx']}/badarx.7z"
    assert checkout_positive(f"test -f {bad_archive}", ""), "Повреждённый архив не найден"

    cmd = f"7z t -t{data['archive_type']} {bad_archive}"
    assert checkout_negative(cmd, "ERROR"), "Не получена ожидаемая ошибка"
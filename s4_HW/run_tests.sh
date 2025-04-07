#!/bin/bash
cd ~/Desktop/s3_HW

# Полная очистка перед тестами
rm -rf ~/tst/* reports/*
mkdir -p reports

# Запуск тестов
pytest -v --html=reports/report.html

# Перемещаем статистику
[ -f stat_alt.txt ] && mv stat_alt.txt reports/

echo "Готово! Отчёт: file://$(pwd)/reports/report.html"
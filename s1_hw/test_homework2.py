import subprocess

tst = "/home/ubuntu/testo"

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False

def checkout2(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result

def test_listing():
    # Проверяем вывод списка файлов в архиве
    assert checkout("cd {}; 7z l archive.7z".format(tst), "Listing archive"), "test_listing FAIL"

def test_unpacking():
    # Проверяем вывод списка файлов в архиве
    assert checkout("cd {}; 7z x archive.7z y y".format(tst), "Everything is Ok"), "test_unpacking FAIL"

def test_fresh_hash():
   assert checkout("cd {}; 7z h archive.7z".format(tst), "f8339fbd\n"), "test_hash FAIL"
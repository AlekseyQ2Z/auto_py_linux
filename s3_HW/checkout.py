import subprocess


def checkout_positive(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if result.returncode == 0 and text in result.stdout:
        return True
    else:
        return False


def checkout_negative(cmd, text):
    result = subprocess.run(cmd, shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding="utf-8")
    full_output = result.stdout + result.stderr
    # Проверяем либо текст ошибки, либо ненулевой код возврата
    return (text in full_output) or (result.returncode != 0)
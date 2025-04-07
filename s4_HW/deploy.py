from sshcheckers import ssh_checkout
import yaml
import sys

with open('config.yaml') as f:
    data = yaml.safe_load(f)

def deploy():
    print("Обновляем пакеты и устанавливаем p7zip-full...")
    cmd = f"""
        echo '{data['ssh']['passwd']}' | sudo -S apt update &&
        sudo apt install -y p7zip-full &&
        dpkg -s p7zip-full
    """
    success = ssh_checkout(
        data['ssh']['host'],
        data['ssh']['user'],
        data['ssh']['passwd'],
        cmd,
        "Status: install ok installed",
        data['ssh']['port']
    )
    return success

if deploy():
    print("Деплой успешен!")
    sys.exit(0)
else:
    print("Ошибка деплоя!")
    sys.exit(1)
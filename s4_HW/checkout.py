from sshcheckers import ssh_checkout, ssh_checkout_negative

def checkout_positive(cmd, text):
    with open('config.yaml') as f:
        data = yaml.safe_load(f)
    return ssh_checkout(data['ssh']['host'], data['ssh']['user'], data['ssh']['passwd'], cmd, text, data['ssh']['port'])

def checkout_negative(cmd, text):
    with open('config.yaml') as f:
        data = yaml.safe_load(f)
    return ssh_checkout_negative(data['ssh']['host'], data['ssh']['user'], data['ssh']['passwd'], cmd, text, data['ssh']['port'])
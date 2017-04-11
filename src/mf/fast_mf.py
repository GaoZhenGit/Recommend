import os


def run():
    command = 'java -jar '
    jar_path = './mf/fast_mf.jar '
    param_path = './mf/config.json'
    exec_commend = command + jar_path + ' ' + param_path
    print exec_commend
    os.system(exec_commend)


if __name__ == '__main__':
    run()

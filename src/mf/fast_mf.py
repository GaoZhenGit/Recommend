import os


def run(param_path = './mf/config.json'):
    command = 'java -jar '
    jar_path = './mf/fast_mf.jar '
    exec_commend = command + jar_path + ' ' + param_path
    print exec_commend
    os.system(exec_commend)


if __name__ == '__main__':
    run()

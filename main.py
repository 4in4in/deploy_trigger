from flask import Flask
from flask import jsonify

app = Flask(__name__)

import subprocess, re

project_names = ['mycandidate', 'exclusivespecialist']

def escape_ansi(line): # удалить из вывода ANSI-коды (например, которые меняют цвет текста в терминале)
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def normalize_output(subprocess_result): # разбить вывод на список по символу новой строки, удалить пустые значения
    normalized_output = list(filter(None, escape_ansi(subprocess_result).split('\n')))
    return normalized_output

def deploy_trigger(project_name):
    if project_name in project_names:
        commands = [
            # f'cd /ess_data/{project_name}/deployment && git pull',
            f'cd /ess_data/{project_name}/deployment && sudo docker-compose down',
            f'cd /ess_data/{project_name}/deployment && sudo docker-compose pull', 
            f'true && yes | sudo docker image prune',
            f'cd /ess_data/{project_name}/deployment && sudo docker-compose up -d'
            ]
        results = [normalize_output(subprocess.getoutput(command)) for command in commands]
        return results
    else:
        return 'No such project'

@app.route('/deploy/<project_name>')
def deploy(project_name):
    results = deploy_trigger(project_name)
    return {'output': [results]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)

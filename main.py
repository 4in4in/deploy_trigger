from flask import Flask
from flask import jsonify

app = Flask(__name__)

import subprocess, re

def escape_ansi(line): # удалить из вывода ANSI-коды (например, которые меняют цвет текста в терминале)
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def normalize_output(subprocess_result): # разбить вывод на список по символу новой строки, удалить пустые значения
    normalized_output = list(filter(None, escape_ansi(subprocess_result).split('\n')))
    return normalized_output

@app.route('/deploy_trigger')
def deploy_trigger():
    commands = [
        # 'cd /ess_data/mycandidate/deployment && git pull',
        'cd /ess_data/mycandidate/deployment && sudo docker-compose down',
        'cd /ess_data/mycandidate/deployment && sudo docker-compose pull', 
        'true && yes | sudo docker image prune',
        'cd /ess_data/mycandidate/deployment && sudo docker-compose up -d'
        ]
    results = [normalize_output(subprocess.getoutput(command)) for command in commands]
    return {'output': [results]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
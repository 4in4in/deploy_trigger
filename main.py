from flask import Flask, jsonify, request, send_from_directory
import requests
import subprocess, re
import os

app = Flask(__name__, static_url_path='')

project_names = ['mycandidate', 'exclusive', 'questionnaires']

def escape_ansi(line): # удалить из вывода ANSI-коды (например, которые меняют цвет текста в терминале)
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def normalize_output(subprocess_result): # разбить вывод на список по символу новой строки, удалить пустые значения
    normalized_output = list(filter(None, escape_ansi(subprocess_result).split('\n')))
    return normalized_output

def deploy_trigger(project_name):
    if project_name not in project_names:
        return f'No project {project_name}'

    depl_prefix = 'q_' if project_name == 'questionnaires' else ''
    cd_command = f'cd /ess_data/{project_name}/{depl_prefix}deployment'

    commands = [
        f'eval "$(ssh-agent -s)"',
        f'ssh-add /nfshome/alex_thunder/.ssh/4in4in_ssh_git',
        f'{cd_command} && git pull origin master',
        f'{cd_command} && sudo docker-compose down',
        f'{cd_command} && sudo docker-compose pull', 
        f'true && yes | sudo docker image prune',
        f'{cd_command} && sudo docker-compose up -d'
        ]
    results = [ normalize_output(subprocess.getoutput(command)) for command in commands ]
    return results

@app.route('/deploy/<project_name>')
def deploy(project_name):
    mode = request.args.get('mode')
    results = deploy_trigger(project_name)
    if mode == 'str':
        return '\n'+'\n'.join(['\n'.join(x) for x in results])+'\n'
    if mode == 'list':
        return jsonify(*results)
    else:
        return '<br>'.join(['<br>'.join(x) for x in results])

@app.route('/api/_deploy', methods=['POST'])
def _deploy_ex():
    code = request.form.get('code')
    project = request.form.get('project')
    key = os.environ.get('deploy_key')
    if key and code == key:
        results = deploy_trigger(project)
        return '<br>'.join(['<br>'.join(x) for x in results])
    return 'Neverniy kod'

@app.route('/api/deploy')
def return_deploy_page():
    return send_from_directory('', 'deploy.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)

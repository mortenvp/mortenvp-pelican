from fabric.api import *
import fabric.contrib.project as project
import os
import sys
import glob
import SimpleHTTPServer
import SocketServer

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

PUBLISH_DIR = '/home/mvp/dev/mortenvp.github.io'
PELICAN_DIR = '/home/mvp/dev/mortenvp-pelican'
OUTPUT_DIR = os.path.join(PELICAN_DIR, 'output')

base_cmd = ('docker run --name pelican '
            '-v ~/dev/mortenvp-pelican:/pelican '
            '--rm mortenvp/mortenvp-docker {}')

def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    local(base_cmd.format('pelican -s pelicanconf.py'))
    chown()

def chown():

    l = []
    for root, dirs, files in os.walk('output'):
        for d in dirs:
            l.append(os.path.join(root,d))
        for f in files:
            l.append(os.path.join(root,f))

    local('sudo chown -R mvp:mvp {}'.format(' '.join(l)))

def rebuild():
    clean()
    build()

def serve():
    rebuild()

    os.chdir(env.deploy_path)

    PORT = 8000
    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        ('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    local('xdg-open http://localhost:8000')
    server.serve_forever()


def publish():

    local(base_cmd.format('pelican -s publishconf.py'))
    chown()

    with lcd(PUBLISH_DIR):
        local('git pull')
        local('cp -R {}/* .'.format(OUTPUT_DIR))
        local('git add -A')
        local('git commit -am "publish"')
        local('git push')

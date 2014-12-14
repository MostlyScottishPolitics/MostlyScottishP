__author__ = 'laura'
from fabric.api import local
from fabric.context_managers import lcd

from scottviz.settings import PROJECT_PATH


def prepare_deployment(branch_name):
    local('python manage.py test msp')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)


def deploy():
    #path to production
    with lcd(PROJECT_PATH):
        local('git pull '+PROJECT_PATH)
        local('python manage.py migrate msp')
        local('python manage.py test msp')
        #command to restart webserver
        local('python manage.py runserver')
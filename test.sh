#/bin/bash
pip freeze
coverage run --source='django_excel' manage.py test

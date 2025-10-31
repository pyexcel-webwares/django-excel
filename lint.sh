pip install flake8
flake8 --exclude=.venv,.moban.d,docs,setup.py --ignore=F401,E402,E501,W503  --builtins=unicode,xrange,long .  && python setup.py checkdocs
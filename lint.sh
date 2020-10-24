pip install flake8

flake8 --exclude=.moban.d,docs,setup.py --ignore=F401,E402  --builtins=unicode,xrange,long .  && python setup.py checkdocs


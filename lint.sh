pip install flake8
flake8 --exclude=.moban.d,docs,setup.py,venv/   --builtins=unicode,xrange,long . && python setup.py checkdocs

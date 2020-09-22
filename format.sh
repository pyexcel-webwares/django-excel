isort $(find django_excel -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 django_excel
black -l 79 tests

pip freeze
nosetests --with-coverage --cover-package django_excel --cover-package tests tests --with-doctest --doctest-extension=.rst README.rst docs/source django_excel

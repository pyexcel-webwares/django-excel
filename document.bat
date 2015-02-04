python setup.py install
rem del doc\source\generated\*.rst
rem sphinx-autogen -o doc\source\generated doc\source\index.rst
sphinx-build -b html doc\source doc\build

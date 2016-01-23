from os import path, system

config_dir = 'commons/config'
template_dir = 'commons/templates'

if not path.exists("commons"):
    system("git clone https://github.com/pyexcel/pyexcel-commons.git commons")

system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates .moban.d -t README.rst -o README.rst -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates .moban.d -t setup.py -o setup.py -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates .moban.d -t docs/source/conf.py -o doc/source/conf.py -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates .moban.d -t travis.yml -o .travis.yml -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td .moban.d -t requirements.txt -o requirements.txt -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates -t LICENSE.jj2 -o LICENSE -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates .moban.d -t tests/requirements.txt -o tests/requirements.txt -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates .moban.d -t MANIFEST.in.jj2 -o MANIFEST.in -c moban.yaml")
system("moban -cd ../pyexcel-config/config -td ../pyexcel-config/templates .moban.d -t docs/source/index.rst.jj2 -o doc/source/index.rst -c moban.yaml")

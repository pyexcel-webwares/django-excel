{% extends 'docs/source/conf.py.jj2' %}

{%block SPHINX_EXTENSIONS%}
    'sphinxcontrib.excel'
{%endblock%}


{%block custom_doc_theme%}
import os  # noqa
import sys  # noqa
sys.path.append(os.path.abspath('_themes'))
html_theme_path = ['_themes']
html_theme = 'djangodocs'
{%endblock%}

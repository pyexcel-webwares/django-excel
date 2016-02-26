{% extends 'docs/source/conf.py.jj2' %}

{%block custom_doc_theme%}
sys.path.append(os.path.abspath('_themes'))
html_theme_path = ['_themes']
html_theme = 'djangodocs'
{%endblock%}

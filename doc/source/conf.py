# -*- coding: utf-8 -*-
DESCRIPTION = (
    'A django middleware that provides one application programming interfac' +
    'e to read and write data in different excel file formats' +
    ''
)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.spelling',
    'sphinxcontrib.excel'
]

intersphinx_mapping = {
    'pyexcel': ('http://pyexcel.readthedocs.org/en/latest/', None),
}
spelling_word_list_filename = 'spelling_wordlist.txt'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'django-excel'
copyright = u'2015-2017 Onni Software Ltd.'
version = '0.0.7'
release = '0.0.7'
exclude_patterns = []
pygments_style = 'sphinx'
import os  # noqa
import sys  # noqa
sys.path.append(os.path.abspath('_themes'))
html_theme_path = ['_themes']
html_theme = 'djangodocs'
html_static_path = ['_static']
htmlhelp_basename = 'django-exceldoc'
latex_elements = {}
latex_documents = [
    ('index', 'django-excel.tex',
     'django-excel Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'django-excel',
     'django-excel Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'django-excel',
     'django-excel Documentation',
     'Onni Software Ltd.', 'django-excel',
     DESCRIPTION,
     'Miscellaneous'),
]

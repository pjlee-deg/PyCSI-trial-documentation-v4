# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'PyCSI'
copyright = '2024, Degenkolb Engineers'
author = 'Luis Pancardo, Daniel Gaspar, Peter Lee'

release = '0.1'
version = '0.1.0'

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'nbsphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']


templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

nbsphinx_allow_errors = True
nbsphinx_execute = 'never'

# Napoleon docstrings
napoleon_google_docstring = True
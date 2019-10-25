# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../keyoscacquire/'))


# -- Project information -----------------------------------------------------

project = 'Keysight oscilloscope acquire'
copyright = '2019, Andreas Svela'
author = 'Andreas Svela'

# The full version, including alpha/beta/rc tags
version = '3.0.0'
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
'sphinx.ext.autodoc',
'sphinx.ext.todo',
'sphinx.ext.intersphinx',
'recommonmark',
'sphinx_rtd_theme',
'sphinx.ext.napoleon',
'numpydoc',
'sphinx.ext.viewcode',
'sphinx-prompt',
]
autosummary_generate = True
todo_include_todos = True
napoleon_numpy_docstring = True
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pyvisa': ('https://pyvisa.readthedocs.io/en/latest/', None),
    'numpy':  ('https://docs.scipy.org/doc/numpy/', None)}
# autodoc_default_options = {
#     'special-members': '__init__',
# }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"

# import guzzle_sphinx_theme
# html_theme_path = guzzle_sphinx_theme.html_theme_path()
# html_theme = 'guzzle_sphinx_theme'
# # Register the theme as an extension to generate a sitemap.xml
# extensions.append("guzzle_sphinx_theme")
# # Guzzle theme options (see theme.conf for more information)
# html_theme_options = {
#     # Set the name of the project to appear in the sidebar
#     "project_nav_name": project,
# }


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

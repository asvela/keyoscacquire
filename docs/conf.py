# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# the source is in ../keyoscacquire
source_dir = os.path.abspath('..')
print("source directory for package:", source_dir)
sys.path.insert(0, source_dir)

# Get the version from the version file
with open(os.path.join(source_dir, 'keyoscacquire', 'VERSION')) as version_file:
    ver = version_file.read().strip()

# -- Project information -----------------------------------------------------

project = 'keyoscacquire'
copyright = '2020, Andreas Svela'
author = 'Andreas Svela'

# The full version, including alpha/beta/rc tags
version = ver.rsplit(".", 1)[0] # get only major.minor
release = ver

html_title = f"{project} v{version}"

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
#'numpydoc',
'sphinx.ext.viewcode',
'sphinx-prompt',
]
autosummary_generate = True
todo_include_todos = True
napoleon_numpy_docstring = True
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pyvisa': ('https://pyvisa.readthedocs.io/en/latest/', None),
    'numpy':  ('https://docs.scipy.org/doc/numpy/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None)}
# autodoc_default_options = {
#     'special-members': '__init__',
# }

# standard is 'contents' from verson 2.0
master_doc = 'index'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# Uncomment for standard theme
# html_theme = 'alabaster'

# Uncomment for
# import furo
html_theme = "furo"

# Uncomment for read the docs theme
# import sphinx_rtd_theme
# html_theme = "sphinx_rtd_theme"

# Uncomment for Guzzle theme
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
# html_static_path = ['_static']

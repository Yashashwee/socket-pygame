# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0,os.path.abspath('..'))
sys.path.insert(0,os.path.abspath('../Client'))
sys.path.insert(0,os.path.abspath('../Server'))
sys.path.insert(0,os.path.abspath('../tests'))
sys.path.insert(0,os.path.abspath('../NetCode'))
sys.path.insert(0,os.path.abspath('../Game'))
sys.path.insert(0,os.path.abspath('../tests/Game_conclusion'))
sys.path.insert(0,os.path.abspath('../tests/Collision_test'))
sys.path.insert(0,os.path.abspath('../tests/serverEvents.py'))
#for x in os.walk('../../src'):
# sys.path.insert(0, x[0])

project = 'MazeGame'
copyright = '2022, VYD'
author = 'VYD'
release = '1.000'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc'
,'sphinx.ext.doctest'
,'sphinx.ext.intersphinx'
,'sphinx.ext.todo'
,'sphinx.ext.coverage'
,'sphinx.ext.mathjax'
,'sphinx.ext.ifconfig'
,'sphinx.ext.viewcode'
,'sphinx.ext.githubpages'
,'sphinx.ext.napoleon']

#templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
#html_static_path = ['_static']

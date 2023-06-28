import sys
import os


sys.path.extend([os.path.abspath("../../src")])
import aliases


project = "Aliases"
copyright = "2023, Koen Baak"
author = "Koen Baak"
version = aliases.__version__


extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = []
html_theme = "furo"
html_static_path = ["_static"]
html_show_sphinx = False
html_show_copyright = False

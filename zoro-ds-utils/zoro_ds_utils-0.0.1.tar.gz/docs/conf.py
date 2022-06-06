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

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../"))

import zoro_ds_utils

# -- Project information -----------------------------------------------------

project = zoro_ds_utils.__name__
copyright = zoro_ds_utils.__copyright__
author = zoro_ds_utils.__author__

# The full version, including alpha/beta/rc tags
release = zoro_ds_utils.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinxcontrib.apidoc",
    "sphinxcontrib.confluencebuilder",
]

# Defaults to only .rst
source_suffix = source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The root toctree document.
root_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Specify the language the docs are written in.
language = "en"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Options for autodoc extension ----------------------------------------------

# Include Python objects as they appear in source files
# http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_member_order
# Default: alphabetically ('alphabetical' or 'groupwise' or 'bysource')
autodoc_member_order = "groupwise"

# Default flags used by autodoc directives
# autodoc_default_flags = ['members', 'undoc-members', 'private-members',
#                          'special-members', 'show-inheritance']

autodoc_inherit_docstrings = (
    True  # This is already the default behavior; here for explicitness
)


# -- Options for autosummary extension ----------------------------------------------

# Generate autodoc stubs with summaries from code
autosummary_generate = True


# -- Options for napoleon extension ----------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True


# -- Options for apidoc extension ----------------------------------------------

# Auto runs the equivalent of sphinx-apidoc -o ./docs/_source ./zoro_ds_utils -f on build
# See https://github.com/sphinx-contrib/apidoc#configuration
apidoc_module_dir = "../zoro_ds_utils"
apidoc_output_dir = "_source"
apidoc_excluded_paths = []
apidoc_separate_modules = True
# apidoc_toc_file = None
# apidoc_module_first = False
# apidoc_extra_args = []


# -- Options for Confluence Builder -------------------------------------------------
# See https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/configuration/

# Essential Configuration
confluence_publish = True
confluence_space_key = "AKB"  # Analytics Knowledge Base
confluence_server_url = "https://zorotools.atlassian.net/wiki/"
confluence_server_user = os.getenv("CONFLUENCE_SERVER_USER")
# This should be an API token, created at https://id.atlassian.com/manage-profile/security/api-tokens
confluence_server_pass = os.getenv("CONFLUENCE_SERVER_PASS")
# Token version doesn't appear to work as documented
# confluence_publish_token = os.getenv("CONFLUENCE_PUBLISH_TOKEN")

# Generic Configuration
confluence_page_hierarchy = True

# Publishing Configuration
confluence_parent_page = "zuds library"
confluence_parent_page_id_check = 3145760943
# Ensures unique confluence page names, otherwise unrelated pages might get overwritten
confluence_publish_postfix = "(zuds)"
# confluence_sourcelink

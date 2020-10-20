from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Automatically captured required modules for install_requires in requirements.txt and as well as configure
# dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
	all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

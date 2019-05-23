import os
from setuptools import setup

# Load project version
with open(os.path.join('./', 'VERSION')) as version_file:
    project_version = version_file.read().strip()

requirements = [
    'deprecated',
    'semantic_version'
]

setup(
    name='kayak',
    version=project_version,
    description='Genetic Encoding Space Description Framework',
    author='Chair of Data Science',
    author_email='julian.stier@uni-passau.de',
    packages=['kayak'],
    py_modules=['kayak'],
    install_requires=requirements,
    extras_require={
        'NetworkX': ['networkx']
    }
)

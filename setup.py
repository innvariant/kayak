import os
import yaml
from setuptools import setup

# Load project version
with open(os.path.join('./', 'VERSION')) as version_file:
    project_version = version_file.read().strip()

# Load requirements from environment file
environment = yaml.load('environment.yml')
environment_requirements = list()
for elem in environment['dependencies']:
    if isinstance(elem, str):
        # TODO: convert package=0.0 to package==0.0
        environment_requirements.append(elem)
    elif isinstance(elem, dict) and 'pip' in elem:
        environment_requirements.extend(elem['pip'])
print('\n'.join(environment_requirements))

setup(
    name='kayak',
    version=project_version,
    description='Genetic Encoding Space Description Framework',
    author='Chair of Data Science',
    author_email='julian.stier@uni-passau.de',
    packages=['kayak'],
    py_modules=['kayak'],
    install_requires=environment_requirements,
    dependency_links=[],
    extras_require={
        'NetworkX': ['networkx']
    }
)

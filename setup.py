import runpy
from pathlib import Path

from setuptools import find_packages, setup

name = 'emitime'
descriprion = 'Emit time from time!'
version_path = Path(__file__).resolve().parent / name / '__version__.py'
version = runpy.run_path(version_path)['__version__']

with open('requirements.txt', encoding='utf-8') as file:
    requirements = file.read().splitlines()

setup(
    name=name,
    packages=find_packages(include=(name,)),
    descriprion=descriprion,
    version=version,
    install_requires=requirements,
    python_requires='>3.6',
)

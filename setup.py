import runpy
from pathlib import Path

from setuptools import find_packages, setup

name = "emitime"
descriprion = "Emit time from any time!"
author = "Vladislav A. Proskurov"
author_email = "rilshok@pm.me"
classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

version_path = Path(__file__).resolve().parent / name / "__version__.py"
version = runpy.run_path(str(version_path))["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as file:
    requirements = file.read().splitlines()

setup(
    name=name,
    descriprion=descriprion,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author=author,
    author_email=author_email,
    version=version,
    url="https://github.com/rilshok/emitime",
    packages=find_packages(include=(name,)),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    classifiers=classifiers,
    python_requires=">=3.6",
)

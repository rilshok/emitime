import runpy
from pathlib import Path

from setuptools import find_packages, setup

name = "emitime"
descriprion = "Emit time from any time!"
author = "Vladislav A. Proskurov"
author_email = "rilshok@pm.me"

version_path = Path(__file__).resolve().parent / name / "__version__.py"
version = runpy.run_path(version_path)["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as file:
    requirements = file.read().splitlines()

package_data={name: ["py.typed", *map(lambda x: x.name, Path("emitime").rglob("*.pyi"))]}

setup(
    name=name,
    descriprion=descriprion,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    version=version,
    url="https://github.com/rilshok/emitime",
    packages=[name],
    package_data=package_data,
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

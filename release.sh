#!/usr/bin/env bash

stubgen ./emitime -o .
python setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
find emitime -name "*.pyi" -type f -delete
rm -r dist build

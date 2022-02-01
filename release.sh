python setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
rm -r dist
rm -r build

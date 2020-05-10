# Release Tools

Scripts to help with releasing a version to PyPI.

## Instructions

1. Grab last version, `X.Y.Z`
1. Generate changelog: `python scripts/generate_changelog.py -v X.Y.Z`
1. Cut a release on GitHub
1. Upload to PyPI

## PyPI Workflow

### Set up ~/.pypirc

```text
[distutils]
index-servers=
  pypi
  testpypi

[pypi]
repository=https://upload.pypi.org/legacy/
username=alysivji
password=[password]

[testpypi]
repository: https://test.pypi.org/legacy/
username=alysivji
password=[password]
```

### Test it on TestPyPI

```console
pip install twine
pip install wheel
python setup.py sdist bdist_wheel
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ sivtools
```

### Release to PyPI

```console
twine upload --repository pypi dist/*
```

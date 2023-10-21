# Development

Some extra details for developers

## Publish to pypi

### Requirements

```bash
pip install twine
```

### Upload

Ensure you have updated the version number in `setup.py` 
and that you have updated the change log in `README.md`

Then run the following.

```bash
python setup.py sdist
twine upload dist/*
```

Finally create a release in github and upload the tar.gz file

```bash
git tag v[version]
e.g.
git tag v0.6
```


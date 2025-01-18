# Development

Some extra details for developers

## Publish to pypi from github action (Preferred)

* Ensure you have updated the version number in `setup.py` and that you have updated the change log in `CHANGELOG.md`
* In github go to "Releases" and "Draft a new Release" 
* Set Release Title as the version number e.g "v0.7"
* In choose a tag type the version number e.g. "v0.7" and select "Create new tag"
* In Description enter details from the change log.
* Tick "Set as latest release"
* Click publish "Release"
* Watch GitHub Action to ensure it builds and publishes


## Publish to pypi manually

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


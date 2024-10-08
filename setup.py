from setuptools import setup

version = '0.21'

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='pyblustream',
    packages=['pyblustream'],
    version=version,
    license='Apache 2.0',
    description='Control Blustream and Elan HDBaseT Matrix',
    long_description=long_descr,
    long_description_content_type='text/markdown',    
    author='foxy82',
    author_email='foxy82.github@gmail.com',
    url='https://github.com/designer-living/pyblustream',
    download_url=f'https://github.com/foxy82/designer-living/archive/{version}.tar.gz',
    keywords=['Blustream', 'Elan', 'HDBaseT'],
    install_requires=[
        "aiohttp>=3.8.3",
        "xmltodict>=0.11.0"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10'
    ],
)

from distutils.core import setup

version = '0.3'


setup(
    name='pyblustream',
    packages=['pyblustream'],
    version= version,
    license='Apache 2.0',
    description='Control Blustream and Elan HDBaseT Matrix',
    author='foxy82',
    author_email='foxy82.github@gmail.com',
    url='https://github.com/foxy82/pyblustream',
    download_url= f'https://github.com/foxy82/pyblustream/archive/{version}.tar.gz',
    keywords=['Blustream', 'Elan', 'HDBaseT'],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10'
    ],
)

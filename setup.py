import os
from codecs import open  # To use a consistent encoding

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().split('\n')

with open(os.path.join(here, 'VERSION'), encoding='utf-8') as f:
    __version__ = f.read().strip()

setup(
    name='aftership',

    python_requires='>=3.5.0',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=__version__,

    description='Python SDK of AfterShip API',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/AfterShip/aftership-python',

    # Download path
    download_url='https://github.com/AfterShip/aftership-python/tarball/{}'.format(__version__),

    # Author details
    author='AfterShip',
    author_email='support@aftership.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Production',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    # What does your project relate to?
    keywords='aftership api binding tracking track post mail airmail logistics shipping',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['aftership'],
    install_requires=install_requires,
)

"""See README.md for package documentation."""

from setuptools import setup, find_packages

from io import open
from os import path

from kivy_garden.animationbuilder import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

URL = 'https://github.com/kivy-garden/animationbuilder'

setup(
    name='kivy_garden.animationbuilder',
    version=__version__,
    description='Easy way of writing Kivy Animations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Gotta Dive Into Python',
    author_email='flow4re2c@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Kivy kivy-garden',

    packages=['kivy_garden.animationbuilder'],
    install_requires=[],
    extras_require={
        'dev': ['pytest>=3.6', 'wheel', 'pytest-cov', 'pycodestyle'],
        'travis': ['coveralls'],
    },
    package_data={},
    data_files=[],
    entry_points={},
    project_urls={
        'Bug Reports': URL + '/issues',
        'Source': URL,
    },
)

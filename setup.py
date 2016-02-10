#!/usr/bin/env python

from distutils.core import setup

install_requires = [
    'distance==0.1.3',
    'feedparser>=5.2.1,<5.3.0',
    'pyCLI>=2.0.3,<2.1.0',
    'requests>=2.9.1,<3.0.0',
    'wikia>=1.4.3,<1.5.0'
]

setup(
    # Package
    name='rs-tools',
    version='1.0.0',
    description='RuneScape CLI Tools',
    url='https://github.com/connordavison/rs-tools',
    packages=['runescape'],
    scripts=['scripts/rs'],
    
    # Author
    author='C. Davison',
    author_email='connorpdavison@gmail.com',
    
    # Requires
    install_requires=install_requires
)

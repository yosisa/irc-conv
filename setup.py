# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

name = 'irc-conv'
version = '0.1.0'
readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme).read()

classifiers = [
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: System :: Networking'
]

setup(name=name,
      version=version,
      author='Yoshihisa Tanaka',
      author_email='yt.hisa@gmail.com',
      url='https://github.com/yosisa/irc-conv',
      description='A proxy server for converting irc encoding',
      long_description=long_description,
      classifiers=classifiers,
      keywords=['irc', 'codecs'],
      install_requires=[],
      tests_require=[],
      packages=find_packages(exclude=['tests']),
      entry_points="""\
      [console_scripts]
      ircconv = ircconv:main
      """)

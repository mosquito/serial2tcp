#!/usr/bin/python

from distutils.core import setup

setup(
    name='serial2tcp',
    version='0.5.2',
    url='https://github.com/mosquito/serial2tcp',
    download_url='https://github.com/mosquito/serialtcp/archive/master.zip',
    description='Convert serial device to tcp socket.',
    license='GNU GPL v3',
    package_data={'': ['README']},
    long_description=open('README').read(),
    author='Dmitry Orlov',
    author_email='me@mosquito.su',
    platforms=['linux', 'windows', 'darwin'],
    scripts=['bin/serial2tcp'],
    install_requires=[
        'pyserial',
    ],
)

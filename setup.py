from distutils.core import setup

setup(
    name = 'pyfoobot',
    packages = ['pyfoobot'],
    version = '0.1',
    description = 'A module to read from a Foobot device',
    long_description=open('README.rst').read(),
    author = 'Philip Lundrigan',
    author_email = 'philiplundrigan@gmail.com',
    url = 'https://github.com/philipbl/pyfoobot',
    download_url='https://github.com/philipbl/pyfoobot/tarball/master',
    keywords = ['air quality', 'sensor', 'IoT'],
    classifiers = [],
    install_requires=[
        'requests>=2.7'
    ],
)

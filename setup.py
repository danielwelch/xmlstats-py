from setuptools import setup


def read(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

long_description = u'\n\n'.join([read('README.rst'),
                                 read('CHANGES.rst')])

setup(
    name='Xmlstats-py',
    version='1.0.0',
    description='Python client for xmlstats API',
    url='https://github.com/dwelch2101/Xmlstats-py',
    author='Daniel Welch',
    author_email='dwelch2012@gmail.com',
    packages=['xmlstats'],
    scripts=[],
    long_description=long_description,
    license='MIT',
    install_requires=['requests'],
)

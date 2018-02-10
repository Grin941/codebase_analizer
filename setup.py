from setuptools import setup, find_packages
from setuptools.command.install import install as _install

__version__ = '0.2.0'


class NLTKInstall(_install):
    def run(self):
        _install.do_egg_install(self)

        import nltk
        nltk.download('averaged_perceptron_tagger')


setup(
    cmdclass={'install': NLTKInstall},
    name='Code base analizer',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    version=__version__,
    install_requires=['nltk'],
    setup_requires=['nltk']
)

from codecs import open
from os import path
from setuptools import setup, find_packages
from setuptools.command.install import install


class InstallWithBabel(install):
    def run(self):
        self.install_hbmqtt()
        install.run(self)

    def install_hbmqtt(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)
        option_dict = self.distribution.get_option_dict('compile_catalog')
        compiler.domain = [option_dict['domain'][1]]
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()


def get_version():
    filehash = {}
    with open("{}/version.py".format(NAME)) as fp:
        exec(fp.read(), filehash)
    return filehash['__version__']


def read(fname):
    with open(path.join(here, fname), encoding='utf-8', mode='r') as f:
        return f.read()


NAME = "mockquitto"
here = path.abspath(path.dirname(__file__))

setup(
    name=NAME,
    version=get_version(),
    description='A sample Python project',
    long_description=read("README.rst"),
    url='https://github.com/Samsung-IoT-Academy/mockquitto',
    author='Georgiy Odisharia',
    author_email='math.kraut.cat@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Topic :: Education',
        'Topic :: Communications',
        'Topic :: Internet',
    ],
    keywords='mqtt',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    cmdclass={
        'install': InstallWithBabel,
    },

    install_requires=[
        'hbmqtt_samsung>0.9.0'
    ],
    python_requires="~=3.4",
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'mqtt-broker = mockquitto.scripts.broker:main',
            'mqtt-async-generator = mockquitto.scripts.mqtt_generator_asyncio:main',
        ],
    },
)

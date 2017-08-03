from codecs import open
from os import path
from setuptools import setup, find_packages
from setuptools.command.install import install


# class PostInstallCommand(install):
#     def run(self):
#         self.install_hbmqtt()
#         install.run(self)
#
#     @staticmethod
#     def install_hbmqtt():
#         import pip
#         import os
#         git_links = {
#             "hbmqtt": "git+https://github.com/beerfactory/hbmqtt.git@f4330985115e3ffb3ccbb102230dfd15bb822a72",
#         }
#         pip_cli_args = []
#         try:
#             pip_cli_args += ['--proxy'] + os.environ['http_proxy']
#         except KeyError:
#             pass
#         pip_cli_args += ['install'] + [_ for _ in git_links.values()]
#
#         print("Installing prerequirements packages :{0}".format(" ".join(git_links.keys())))
#         pip.main(pip_cli_args)


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

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # cmdclass={
    #     'install': PostInstallCommand,
    # },
    setup_requires=[
        'pip'
    ],
    install_requires=[
        'hbmqtt_samsung>0.9.0'
    ],

    python_requires="~=3.4",

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    entry_points={
        'console_scripts': [
            'mqtt-broker = mockquitto.scripts.broker:main',
            'mqtt-async-generator = mockquitto.scripts.mqtt_generator_asyncio:main',
        ],
    },
)

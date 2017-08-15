from codecs import open
from os import path, listdir
import re
from setuptools import setup, find_packages
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))
NAME = "mockquitto"

class InstallWithBabel(install):
    def run(self):
        self.babel_compile()
        super().run()

    def babel_compile(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)
        option_dict = self.distribution.get_option_dict('compile_catalog')
        compiler.domain = [option_dict['domain'][1]]
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        # super().run()

def get_release() -> str:
    version = get_version()
    return ".".join(version.split('.')[:2])

def get_version() -> str:
    filehash = {}
    with open("{}/version.py".format(get_name())) as fp:
        exec(fp.read(), filehash)
    return filehash['__version__']

def get_name() -> str:
    return NAME

def read(fname):
    with open(path.join(here, fname), encoding='utf-8', mode='r') as f:
        return f.read()

setup(
    name=get_name(),
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
    command_options={
        'build_sphinx': {
            'project': ('setup.py', get_name()),
            'release': ('setup.py', get_release()),
            'version': ('setup.py', get_version()),
        },
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
            'mockquitto-server = mockquitto.scripts.broker:main',
            'mockquitto-async-generator = mockquitto.scripts.mqtt_generator_asyncio:main',
        ],
    },
)

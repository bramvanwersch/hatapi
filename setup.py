
from setuptools import setup

setup(
    name='hatapi',
    version='0.1',
    packages=['hatapi', 'hatapi.src', 'hatapi.src.q_learner_saver'],
    url='https://github.com/bramvanwersch/hatapi.git',
    scripts=["bin/hatapi"],
    license='MIT',
    author='bramv',
    author_email='bramvanwersch@live.nl',
    description='Command line interface for doing some simple things on the pi sensehat'
)

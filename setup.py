from setuptools import setup

from os import path

def get_long_description():
    with open(
        path.join(path.dirname(path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(name='ouseful_jupyterlite_utils',
      author='Tony Hirst',
      author_email='tony.hirst@open.ac.uk',
      install_requires=[],
      version='0.0.1',
      description='OUseful JupyterLite utlities.',
      long_description=get_long_description(),
      long_description_content_type="text/markdown",
      license='MIT License',
      packages=['ouseful_jupyterlite_utils']
)
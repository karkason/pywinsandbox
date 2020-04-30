from codecs import open as codecs_open
from setuptools import setup, find_packages

# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='pywinsandbox',
      version='1.2.0',
      description=u"Python Utilities for Windows Sandbox",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[],
      keywords='',
      author=u"Yiftach Karkason",
      author_email='ykarkason@gmail.com',
      url='https://github.com/karkason/pywinsandbox',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'yattag',
          'rpyc',
          'cached-property',
          'recordclass',
          'IPython',
          'wmi'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      winsandbox=winsandbox.cli:main
      wsb=winsandbox.cli:main
      """
      )

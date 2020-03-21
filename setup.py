from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='windows_sandbox',
      version='0.0.1',
      description=u"Utilities For Windows Sandbox",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Yiftach Karkason",
      author_email='ykarkason@gmail.com',
      url='https://github.com/karkason/windows-sandbox',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'yattag',
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      #windows_sandbox=windows_sandbox.scripts.cli:cli
      """
      )
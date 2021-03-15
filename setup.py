from setuptools import setup

with open('requirements.txt') as f:
   requirements = f.readlines()

with open('README.md') as f:
   long_description = f.read()

setup(
   name='speedtest-monitor',
   version='0.0.2',
   description='Monitor your speed test automatically using speedtest.net',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Haroune Mohammedi',
   author_email='mohammedi.haroun@gmail.com',
   url="https://github.com/mohammedi-haroune/speedtest-monitor",
   licence="MIT",
   packages=['speedtest_monitor'],
   entry_points={'console_scripts': ['speedtest-monitor=speedtest_monitor.main:main']},
   install_requires=requirements,
)

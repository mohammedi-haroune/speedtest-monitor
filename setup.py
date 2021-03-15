from setuptools import setup

with open('requirements.txt') as f:
   requirements = f.readlines()

setup(
   name='speedtest-monitor',
   version='0.0.1',
   description='Monitor your speed test automatically using speedtest.net',
   author='Haroune Mohammedi',
   author_email='mohammedi.haroun@gmail.com',
   packages=['speedtest_monitor'],
   entry_points={'console_scripts': ['speedtest-measure=speedtest_monitor.main:main']},
   install_requires=requirements,
)

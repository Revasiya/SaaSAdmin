from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in setup_app/__init__.py
from setup_app import __version__ as version

setup(
	name="setup_app",
	version=version,
	description="App to setup new sites",
	author="OneHash",
	author_email="digital@onehash.ai",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

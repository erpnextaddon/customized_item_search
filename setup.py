from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in customized_item_search/__init__.py
from customized_item_search import __version__ as version

setup(
	name="customized_item_search",
	version=version,
	description="Search Item",
	author="kunhimohamed6@gmail.com",
	author_email="kunhimohamed6@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

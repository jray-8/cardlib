from setuptools import setup, find_packages

setup(
	name='cardlib',
	version='1.0.0',
	packages=find_packages(),
	description='Reusable card and dice library for text-based games',
	author='Jeffrey Ray',
	url='https://github.com/jray-8/cardlib',
	license='MIT',
	python_requires='>=3.8',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
)
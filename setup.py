from setuptools import setup, find_packages

setup(
	name='cardlib',
	version='1.0.0',
	author='Jeffrey Ray',
	author_email='jeffrey.ray@bell.net',
	description='Reusable card and dice library for text-based games',
	long_description=open('README.md', encoding='utf-8').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/jray-8/cardlib',
	license='MIT',
	packages=find_packages(),
	python_requires='>=3.8',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
)
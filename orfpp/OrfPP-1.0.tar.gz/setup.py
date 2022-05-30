import setuptools

with open ("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "OrfPP",
	version = "1.0",
	author = "Bo Song",
	author_email = "songbo446@yeah.net",
	description = "An ORF predictor from SNPs",
	long_description = long_description,
	url = "https://github.com/songbo446",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	
	entry_points={
		'console_scripts':['OrfPP=OrfPP.OrfPP:main'],
	},
)

import setuptools

with open("README1.md", "r") as fh:
    long_description = fh.read()
    

setuptools.setup(
     name='vision_aided_loss',  
     version='0.1.0',
     author="Nupur Kumari",
     author_email="nupurkmr9@gmail.com",
     description="Vision-aided GAN training",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/nupurkmr9/vision_aided_loss",
     packages=setuptools.find_packages(include=['vision_aided_loss', 'vision_aided_loss.*']),
     include_package_data=True,
     install_requires=[
                       "torch>=1.8.0",
                       "torchvision>=0.9.0",
                       "numpy>=1.14.3", 
                       "requests",
                       "timm",
                       "antialiased_cnns",
                       "gdown==4.4.0",
                       "ftfy",
                       "regex", 
                       "tqdm",      ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: BSD License",
         "Operating System :: OS Independent",
     ],
 )
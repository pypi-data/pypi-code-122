from distutils.core import setup
setup(
  name = 'LibSerial77',       
  packages = ['LibSerial77'],   
  version = '0.1',      
  license='MIT',       
  description = 'Biblioteca LibSerial77 ',   
  author = 'Nome do Autor',                  
  author_email = 'Email@gmail.com',     
  url = 'https://github.com/path/LibSerial77',  
  download_url = 'https://github.com/path/LibSerialx/archive/0.1.tar.gz',    
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=[           
          'datetime',
          'random',         
      ],
  classifiers=[
    #"3 - Alpha", "4 - Beta" or "5 - Production/Stable"   
    'Development Status :: 5 - Production/Stable',   
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)
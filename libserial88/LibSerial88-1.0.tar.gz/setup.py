from distutils.core import setup
setup(
  name = 'LibSerial88',       
  packages = ['LibSerial'],   
  version = '1.0',      
  license='MIT',       
  description = 'Biblioteca LibSerial88',   
  author = 'Fernando Simplicio',                  
  author_email = 'fernando@microgenios.com.br',     
  url = 'https://github.com/microgenios/libserial88',  
  download_url = 'https://github.com/microgenios/libserial88/archive/refs/heads/main.zip',    
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=[           
          'datetime',         
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
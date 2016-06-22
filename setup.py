from distutils.core import setup

# hack for vagrant based environment
import os
del os.link

setup(
    name='pysllo',
    version='0.1',
    packages=['pysllo'],
    url='http://pysllo.readthedocs.io/',
    license='BSD',
    author='Marcin Karkocha',
    author_email='kivio@kivio.pl',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Logging',
        'Topic :: Utilities'
         ],
    keywords='logging development utilities administrative monitoring',
    description='Make your python logging more '
                'structured and easy to aggregate'
)

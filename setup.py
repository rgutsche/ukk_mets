from setuptools import setup


setup(name='ukk_mets',
      version='1.0',
      packages=["ukk_mets"],
      description='Tool for radiomics',
      url='https://github.com/rgutsche/ukk_mets',
      python_requires='>=3.5',
      author='Robin Gutsche',
      author_email='r.gutsche@fz-juelich.de',
      license='Apache 2.0',
      zip_safe=False,
      install_requires=[
          'pyradiomics',
          'nipype'
      ],
      entry_points={
          'console_scripts': [
                'predict = ukk_mets:main',
        ],
      },
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Operating System :: Unix'
      ]
      )
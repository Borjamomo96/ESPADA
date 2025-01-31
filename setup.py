from setuptools import setup, find_packages

setup(
    name="adp_alma_pipeline",
    version="1.0",
    description="ADPAlmap either downloads data via the TAP service or uses ALMA's own data and "
    "performs source searches using SOFIA software and produces images for publication or quick "
    "inspection using SIP software.",
    url="https://gitlab.com/adp-group1/adp-alma-pipeline",
    author="Borja Montoro Molina",
    author_email= "borjamomo96@gmail.com",
    packages=find_packages(where='adplib'),
    package_dir={'': 'adplib'},
    install_requires=[
        "numpy >= 2.1.2", 
        "pandas >= 2.2.3", 
        "pyyaml >= 6.0.2", 
        "astropy >= 6.1.4",
        "astroquery >= 0.4.8.dev9474",
        "pyvo >= 1.5.3",
        "matplotlib >= 3.9.2"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'adpalmap=adplib.adpalmap:main',
        ],
    },
)
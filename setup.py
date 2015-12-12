try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

dependencies = [
    'pyexcel>=0.1.5',
    'pyexcel-webio>=0.0.2',
    'Django>=1.7.1'
]
extras = {
    'xls': ['pyexcel-xls>=0.0.7'],
    'xlsx': ['pyexcel-xlsx>=0.0.7'],
    'ods3': [
        'pyexcel-ods3>=0.0.8',
        'https://github.com/T0ha/ezodf/archive/2c69103e6c0715adb0e36562cb2e6325fd776112.zip',
    ],
}

setup(
    name='django-excel',
    author="C. W.",
    version='0.0.3',
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/django-excel",
    description='A django middleware that provides one application programming interface to read and write data in different excel file formats',
    install_requires=dependencies,
    extras_require=extras,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'mysite', 'polls', 'migrations']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose'],
    keywords=['API', 'Django', 'Excel'],
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)

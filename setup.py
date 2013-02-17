from setuptools import setup

#ext_modules = [Extension("cmwlib", ["cmwlib.pyx"])]
#ext_modules = [Extension("cedgecache", ["cedgecache.pyx"])]

setup(
    name = "wiki-network",
    description = 'VinDieselism: A Wikipedia anti-vandalism bot',
    version = "0.1",
    install_requires = ('lxml', 'celery', 'wirebin', 'sqlalchemy', 'nose', 'nose-exclude'),
    #cmdclass = {'build_ext': build_ext},
    #ext_modules = ext_modules
)

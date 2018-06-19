import setuptools

PACKAGE = 'loopus'
VERSION = '0.1.0'
NAME = "loopus"
DESCRIPTION = ""
AUTHOR = "Gabriele  Barbieri"
AUTHOR_EMAIL = "gabriele.barbieri83@gmail.com"
URL = "https://github.com/gabrielebarbieri/" + NAME


install_requires = ['mido']

setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='',
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=install_requires
)

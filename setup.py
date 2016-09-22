try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Spyonweb API wrapper',
    'author': 'Kyle R Maxwell',
    'url': 'https://github.com/krmaxwell/spyonweb',
    'download_url': 'https://github.com/krmaxwell/spyonweb',
    'author_email': 'krmaxwell@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'pre-commit'],
    'packages': ['spyonweb'],
    'scripts': [],
    'name': 'spyonweb'
}

setup(**config)

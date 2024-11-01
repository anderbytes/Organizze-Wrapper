from setuptools import setup, find_packages

setup(
    name='Organizze-Wrapper',
    version='1.1.2',
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "PyMultiHelper>=1.1.4"
    ],
    description='Biblioteca Python de Wrapper para a API do Organizze.com.br',
    author='Anderson',
    author_email='anderbytes@gmail.com',
    url='https://github.com/anderbytes/Organizze-Wrapper',

    long_description_content_type="text/markdown",
    long_description=open('README.md').read()
)

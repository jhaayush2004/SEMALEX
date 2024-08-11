from setuptools import setup, find_packages

setup(
    name='SEMALEX',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'numpy',
        'scikit-learn',
        'sentence_transformers',
        'torch'
    ],
    author='Ayush Shaurya Jha',
    author_email='shauryasphinx@gmail.com',
    description="A comprehensive evaluation metric designed to measure the weighted similarity score by prioritizing semantic capture while also considering lexical alignment."
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jhaayush2004/SemaLex',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
# Designed on Python version: 3.10.9
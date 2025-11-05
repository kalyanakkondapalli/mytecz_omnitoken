"""
Setup configuration for MyTecZ OmniToken.

This file defines the package configuration for installation and distribution.
"""

from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
def get_version():
    """Extract version from __init__.py file."""
    version_file = os.path.join(os.path.dirname(__file__), 'omnitoken', '__init__.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
        version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', content, re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError('Unable to find version string.')

# Read long description from README
def get_long_description():
    """Read long description from README file."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name="mytecz-omnitoken",
    version=get_version(),
    author="MyTecZ",
    author_email="contact@mytecz.com",
    description="Universal tokenizer with modular architecture supporting multiple tokenization strategies",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/mytecz/omnitoken",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies - keeping minimal for broad compatibility
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
        "examples": [
            "jupyter>=1.0",
            "matplotlib>=3.0",
            "pandas>=1.0",
        ],
        "performance": [
            "numpy>=1.20",
            "cython>=0.29",
        ]
    },
    entry_points={
        "console_scripts": [
            "omnitoken=omnitoken.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "omnitoken": [
            "data/*.json",
            "data/*.txt",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/mytecz/omnitoken/issues",
        "Source": "https://github.com/mytecz/omnitoken",
        "Documentation": "https://mytecz-omnitoken.readthedocs.io/",
    },
    keywords=[
        "tokenizer",
        "nlp",
        "natural language processing",
        "bpe",
        "wordpiece", 
        "sentencepiece",
        "subword",
        "machine learning",
        "text processing",
        "unicode",
        "multilingual"
    ],
    zip_safe=False,
)
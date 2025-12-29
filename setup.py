
"""
Setup configuration for NCERT Notes Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ncert-notes-generator",
    version="1.0.0",
    author="NCERT Notes Generator Team",
    description="AI-powered study notes generator for NCERT textbooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.39.0",
        "langgraph>=0.2.0",
        "langchain>=0.1.0",
        "PyPDF2>=3.0.0",
        "reportlab>=4.0.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "pdfplumber>=0.10.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "colorama>=0.4.6",
        "tqdm>=4.66.0",
        "pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ncert-notes=main:main",
        ],
    },
)
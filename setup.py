from setuptools import setup, find_packages

setup(
    name="temperature-forecasting",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A project for forecasting temperature trends using historical data.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/temperature-forecasting",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
        "flask",  # or "streamlit" if using Streamlit for UI
        "scikit-learn"  # if using machine learning for forecasting
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
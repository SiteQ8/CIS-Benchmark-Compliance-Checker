from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cis-benchmark-checker",
    version="1.0.0",
    author="SiteQ8",
    author_email="site@hotmail.com",
    description="Automated CIS Benchmark compliance auditing and remediation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SiteQ8/CIS-Benchmark-Compliance-Checker",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "jinja2>=3.0.0",
        "colorama>=0.4.4",
        "tabulate>=0.9.0",
        "python-dateutil>=2.8.0",
        "pandas>=1.3.0",
        "plotly>=5.0.0",
        "openpyxl>=3.0.0",
        "psutil>=5.9.0",
        "distro>=1.7.0",
    ],
    entry_points={
        "console_scripts": [
            "cis-checker=cis_checker.cli:main",
        ],
    },
)

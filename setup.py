from setuptools import setup, find_packages

setup(
    name="counterfactual-flip-cost",
    version="1.0.0",
    description="Counterfactual Flip-Cost Analysis for Assessing Ordering Sensitivity in Constraint-Valid Event Timelines",
    author="Kamalesh N., Varun Dubey",
    author_email="kamalesh.n2024@vitstudent.ac.in",
    url="https://github.com/Disgusting-Orange/counterfactual-flip-cost",
    packages=find_packages(where="experiments_suite"),
    package_dir={"": "experiments_suite"},
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
        "networkx>=3.0",
        "scikit-learn>=1.2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    python_requires=">=3.9"
)

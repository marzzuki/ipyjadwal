from setuptools import setup, find_packages

setup(
    name="ipyjadwal",
    version="0.1.3",
    python_requires=">=3.7",
    description="A clean, interactive Google Sheet explorer for Colab (Jadwal)",
    long_description=open("README.md").read() if "README.md" in globals() else "",
    long_description_content_type="text/markdown",
    author="Mustafa Marzouk",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "gspread>=5.0.0",
        "pandas",
        "ipywidgets",
        "google-auth",
        "ipython",
    ],
    keywords=["jupyter", "widget", "google sheets", "colab", "jadwal"],
)

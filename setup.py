from setuptools import setup, find_packages

setup(
    name="ipyjadwal",
    version="0.1.2",
    python_requires=">=3.7",
    description="A clean, interactive Google Sheet explorer for Colab (Jadwal)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mustafa Marzouk",
    license="MIT",
    packages=find_packages(),
    install_requires=["gspread", "pandas", "ipywidgets", "google-auth"],
    keywords=["jupyter", "widget", "google sheets", "colab", "jadwal"],
)

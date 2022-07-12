from setuptools import setup, find_packages

def read_files(files):
    data = []
    for file in files:
        with open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)

long_description = read_files(['README.md'])
requirements = ['requests', 'click', 'redis', 'urllib3', 'mysql-connector-python', 'pika', 'python-dotenv']

setup(
    name = 'health-util',
    description = 'A cli package for providing healthcheck',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = '0.0.9',
    author = 'mogu4iy',
    author_email = 'mogu4iy.kotygoroshko@gmail.com',
    license = 'MIT',
    url = "https://github.com/mogu4iy/health-util/",
    packages=find_packages(where="src"),
    package_dir={'':"src"},
    install_requires = [requirements],
    python_requires='>=3.7',
    entry_points = {
        "console_scripts": [
            "healthcheck=healthcheck.__main__:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
from setuptools import find_packages, setup

requirements_list: list[str] = []


def get_requirements() -> list[str]:
    try:
        with open("requirements.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirements_list.append(requirement)

    except FileNotFoundError:
        print("requirements.txt not found")

    return requirements_list


setup(
    name="NetworkSecurity",
    packages=find_packages(),
    version="0.0.1",
    description="Detecting phishing in a network",
    author="Shubhranshu Arya",
    install_requires=get_requirements(),
)

from glob import glob

from setuptools import find_packages, setup

package_name = "smart_factory_mrs"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/worlds", glob("worlds/*.world")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="choejunhee",
    maintainer_email="student@example.com",
    description="Smart factory multi-robot scheduling and simulation demo.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "factory_sim = smart_factory_mrs.factory_sim_node:main",
            "gazebo_factory_sim = smart_factory_mrs.gazebo_factory_sim_node:main",
        ],
    },
)

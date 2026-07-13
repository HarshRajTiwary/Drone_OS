from setuptools import find_packages, setup

package_name = 'drone_utils'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='DroneOS Platform Team',
    maintainer_email='harishpatel1005@gmail.com',
    description=(
        'Central logger, YAML configuration loader, and shared utility '
        'functions used across DroneOS.'
    ),
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={'console_scripts': []},
)

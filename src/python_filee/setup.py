from setuptools import find_packages, setup

package_name = 'python_filee'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='adityaros',
    maintainer_email='adityaros@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "position_node = python_filee.position_node:main" ,
            "destination_node = python_filee.destination_node:main",
            "user_node = python_filee.user_node:main",
            "monitor_node = python_filee.monitor_node:main"
        ],
    },
)

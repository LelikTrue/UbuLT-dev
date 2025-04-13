from setuptools import setup, find_packages
import os

setup(
    name='face_recognition_system',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
        'pydantic>=1.8.0',
        'loguru>=0.5.3',
    ],
    entry_points={
        'console_scripts': [
            'face_recognition_system=src.main:main',
        ],
    },
    author='Lelik',
    author_email='your.email@example.com',
    description='A face recognition system using FastAPI',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/face_recognition_system',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

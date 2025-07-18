from setuptools import setup, find_packages

setup(
    name="gemini_agent",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gemini-cli = interfaces.cli:main',
            'gemini-telegram = interfaces.telegram_bot:main',
        ],
    },
)

from setuptools import setup, find_packages

setup(
    name="peakflo_project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "groq>=0.4.0",
        "openai-whisper>=20231117",
        "gtts>=2.5.0",
        "sounddevice>=0.4.6",
        "soundfile>=0.12.1",
        "pydub>=0.25.1",
        "httpx>=0.26.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0",
        "loguru>=0.7.0",
        "rich>=13.7.0",
    ],
    python_requires=">=3.8",
    author="Utkarsh Singh",
    author_email="utkarsh.workmail.1@gmail.com",
    description="Voice-enabled AR automation agent using MCP",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hustple/peakflo_project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

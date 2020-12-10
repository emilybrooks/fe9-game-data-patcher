import setuptools

setuptools.setup(
	name="fe9LZ77",
	version="0.0.1",
	author="Emily Brooks",
	description="Encoder and decoder for the LZ77 compression used in Fire Emblem: Path of Radiance",
	packages=setuptools.find_packages(),
	ext_modules=[setuptools.Extension("fe9LZ77", ["fe9lZ77\\fe9LZ77.c"])],
)

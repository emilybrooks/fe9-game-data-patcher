/*
Copyright (c) 2020 Emily Brooks

Originally part of "PyFastGBALZ77" by LagoLunatic

The MIT License (MIT)

Copyright (c) 2020 LagoLunatic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

// resource on how LZ77 compression works
// https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-wusp/fb98aa28-5cd7-407f-8869-a6cef1ff1ccb

#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* fe9LZ77_SizeTooLargeError;

//------------------------------------------------------------------------------
// iterate backwards through every byte in the window
//
// using each byte as a starting position, check how many bytes from the window
// match the lookahead buffer
//
// set BestOffset to the start of the longest match found (how many bytes
// backwards from the coding position)
//
// set BestLength to the length of the longest match found
//------------------------------------------------------------------------------
void FindBestMatch(unsigned char* Lookahead,
				   int LookaheadSize,
				   unsigned char* Window,
				   int WindowSize,
				   int* BestOffset,
				   int* BestLength)
{
	*BestOffset = 0;
	*BestLength = 0;

	if (LookaheadSize == 0)
	{
		return;
	}

	// Offset is how many bytes backwards from the coding position
	for (int Offset = 1; Offset <= WindowSize; Offset++)
	{
		// window index is how many bytes forward from the start of the window
		int WindowIndex = WindowSize - Offset;

		// How many bytes starting from WindowIndex match the lookahead buffer?
		// Note: the window bytes and the lookahead bytes are allowed to overlap
		// for example, if you're encoding 8 bytes that are the same
		// "go backwards 1 byte and copy 7 bytes" is a valid match

		// Note: this is a "brute force" approach
		// I've read that you can do something with a hash map to keep track of
		// offsets based on their first 3 bytes
		// system.cmp is 1.66 MB and it only takes about 5 seconds to compress
		// so optimizing this seems unnecessary for now
		int MatchLength;
		for (MatchLength = 0; MatchLength < LookaheadSize; MatchLength++)
		{
			if (Window[WindowIndex + MatchLength] != Lookahead[MatchLength])
			{
				break;
			}
		}

		if (MatchLength > *BestLength)
		{
			*BestOffset = Offset;
			*BestLength = MatchLength;

			// if the longest possible match has been found, stop searching
			if (*BestLength == LookaheadSize)
			{
				break;
			}
		}
	}
}

//------------------------------------------------------------------------------
// Take an uncompressed bytearray and return it compressed
//------------------------------------------------------------------------------
static PyObject* fe9LZ77_compress(PyObject* self, PyObject* args)
{
	PyObject* InputByteArray;

	// char arrays are unsigned to prevent annoying things from happening
	// for example:
	// when decompressing, you read the filesize. the first byte is 0xC0
	// as a signed char, this is interpreted as -64
	// when assigning it to an integer, it gets "promoted" to 4 bytes, making 0xC0 into 0xFFFFFFC0
	unsigned char* Input;

	if (!PyArg_ParseTuple(args, "Y", &InputByteArray))
	{
		return NULL; // Error already raised
	}

	Input = PyByteArray_AsString(InputByteArray);
	if (!Input)
	{
		return NULL; // Error already raised
	}

	int InputSize = (int)PyByteArray_Size(InputByteArray);
	if (InputSize > 0xFFFFFF)
	{
		PyErr_SetString(fe9LZ77_SizeTooLargeError, "Data larger than 0xFFFFFF bytes cannot be compressed.");
		return NULL;
	}

	unsigned char* Output;

	// The final compressed size is unknown, so this buffer is twice the
	// input size just to be safe
	// the size will be corrected when it's converted back into a bytearray
	Output = malloc(InputSize*2);
	if(!Output)
	{
		return PyErr_NoMemory();
	}
	int InputIndex = 0;
	int OutputIndex = 0;

	// the first byte is 0x10
	Output[OutputIndex++] = 0x10;
	// the next 3 bytes are the uncompressed filesize (in little endian)
	Output[OutputIndex++] = (InputSize & 0x0000FF);
	Output[OutputIndex++] = (InputSize & 0x00FF00) >> 8;
	Output[OutputIndex++] = (InputSize & 0xFF0000) >> 16;

	// Each "block" keeps track of 8 pieces of data
	// the first byte is a bitfield
	// the first bit determines if the first piece of data is compressed or not
	// 1 = compressed, 0 = uncompressed
	int BlockIndex = 0;
	unsigned char* CurrentBitField = &Output[OutputIndex++];
	*CurrentBitField = 0;

	// iterate through every byte in the input file
	while (InputIndex < InputSize)
	{
		// if the block is completed, start a new block
		if (BlockIndex == 8)
		{
			CurrentBitField = &Output[OutputIndex++];
			*CurrentBitField = 0;
			BlockIndex = 0;
		}

		int BestLength, BestOffset;
		int WindowSize = 4096;
		int LookaheadBufferSize = 18;

		//the lookahead buffer shrinks as it approaches the end of the file
		int CurrentLookaheadSize = min(InputSize - InputIndex, LookaheadBufferSize);
		unsigned char* CurrentLookahead = &Input[InputIndex];
		//the window grows until the coding position is past the max window size
		int CurrentWindowSize = min(InputIndex, WindowSize);
		unsigned char* CurrentWindow = &Input[InputIndex - CurrentWindowSize];

		FindBestMatch(CurrentLookahead,
					  CurrentLookaheadSize,
					  CurrentWindow,
					  CurrentWindowSize,
					  &BestOffset,
					  &BestLength);

		// it takes a minimum of 3 bytes to encode data
		// therefore, if the match length is less than 3 it should be
		// uncompressed data.
		// in this case, just copy the byte.
		if (BestLength < 3)
		{
			Output[OutputIndex++] = Input[InputIndex++];
		}
		else
		{
			InputIndex += BestLength;

			// mark the bitflag for this data as 1
			*CurrentBitField += (1 << (7 - BlockIndex));

			// the first 4 bits are the length
			// it starts counting from 3
			BestLength -= 3;
			Output[OutputIndex] = BestLength << 4;
			// the next 12 bits are the offset
			// it starts counting from 1
			BestOffset -= 1;
			Output[OutputIndex++] += BestOffset >> 8;
			Output[OutputIndex++] = BestOffset & 0xFF;
		}
		BlockIndex++;
	}

	int OutputSize = OutputIndex;
	PyObject* OutputByteArray = PyByteArray_FromStringAndSize(Output, OutputSize);
	free(Output);
	return OutputByteArray;
}

//------------------------------------------------------------------------------
// Take a compressed bytearray and return it decompressed
//------------------------------------------------------------------------------
static PyObject* fe9LZ77_decompress(PyObject* self, PyObject* args)
{
	PyObject* InputByteArray;
	unsigned char* Input;

	if (!PyArg_ParseTuple(args, "Y", &InputByteArray))
	{
		return NULL; // Error already raised
	}

	Input = PyByteArray_AsString(InputByteArray);
	if (!Input)
	{
		return NULL; // Error already raised
	}

	int InputSize = (int)PyByteArray_Size(InputByteArray);
	int InputIndex = 0;

	// first byte should be 0x10 for compressed data
	if (Input[InputIndex++] != 0x10)
	{
		PyErr_SetString(PyExc_RuntimeError, "The first byte is not 0x10");
		return NULL;
	}

	// the next three bytes are the length of the uncompressed file (in little endian)
	int OutputSize;
	OutputSize = Input[InputIndex++];
	OutputSize += Input[InputIndex++] << 8;
	OutputSize += Input[InputIndex++] << 16;

	unsigned char* Output;

	Output = malloc(OutputSize);
	if(!Output)
	{
		return PyErr_NoMemory();
	}

	int OutputIndex = 0;

	// Each "block" keeps track of 8 pieces of data
	// the first byte is a bitfield that keeps track of whether
	// a piece of data is compressed or not
	int BlockIndex = 0;
	unsigned char* CurrentBitField = &Input[InputIndex++];

	// iterate through every byte in the input file
	while (InputIndex < InputSize)
	{
		// if the block is completed, move to the next block
		if (BlockIndex == 8)
		{
			CurrentBitField = &Input[InputIndex++];
			BlockIndex = 0;
		}
		// check if the first bit is 1
		if (*CurrentBitField & 0x80)
		{
			// this data is compressed
			// the first 4 bits are the length
			int Length;
			Length = Input[InputIndex] >> 4;
			// it starts counting from 3
			Length += 3;

			// the next 12 bytes are the offset
			int Offset;
			Offset = (Input[InputIndex++] & 0xF) << 8;
			Offset += Input[InputIndex++];
			// it starts counting from 1
			Offset += 1;

			// go back Offset amount of bytes and copy Length amount of bytes
			for (int i = 0; i < Length; i++)
			{
				Output[OutputIndex] = Output[OutputIndex - Offset];
				OutputIndex++;
			}
		}
		else
		{
			// this data is uncompressed
			// just copy the byte
			Output[OutputIndex++] = Input[InputIndex++];
		}
		// shift the bitfield left by 1 bit
		// the bit we just checked gets discarded
		// and the second bit becomes the first bit, which will be checked next loop
		*CurrentBitField <<= 1;
		BlockIndex++;
	}

	PyObject* OutputByteArray = PyByteArray_FromStringAndSize(Output, OutputSize);
	free(Output);
	return OutputByteArray;
}

static PyMethodDef fe9LZ77Methods[] =
{
	{"compress", fe9LZ77_compress, METH_VARARGS, NULL},
	{"decompress", fe9LZ77_decompress, METH_VARARGS, NULL},
	{NULL, NULL, 0, NULL} // Sentinel
};

static struct PyModuleDef fe9LZ77_module =
{
	PyModuleDef_HEAD_INIT,
	"fe9LZ77", // Module name
	NULL, // Documentation
	-1, // Size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
	fe9LZ77Methods
};

PyMODINIT_FUNC PyInit_fe9LZ77(void)
{
	PyObject* module;

	module = PyModule_Create(&fe9LZ77_module);
	if (module == NULL)
	{
		return NULL;
	}

	fe9LZ77_SizeTooLargeError = PyErr_NewException("fe9LZ77.SizeTooLargeError", NULL, NULL);
	Py_XINCREF(fe9LZ77_SizeTooLargeError);
	if (PyModule_AddObject(module, "SizeTooLargeError", fe9LZ77_SizeTooLargeError) < 0)
	{
		Py_XDECREF(fe9LZ77_SizeTooLargeError);
		Py_CLEAR(fe9LZ77_SizeTooLargeError);
		Py_DECREF(module);
		return NULL;
	}

	return module;
}

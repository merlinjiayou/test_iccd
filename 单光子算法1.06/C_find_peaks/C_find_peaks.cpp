// C_find_peaks.cpp : 定义 DLL 应用程序的导出函数。

#include "stdafx.h"
#include"C_find_peaks.h"
#include<Windows.h>
#include<iostream>

GENCALLBACK_API void _stdcall find_peak_8(UINT8 * data,UINT16 * image, int c_size,int v_size,int minvalue,int threshold)
{
	int x = 0;
	int y = 0;
	for (x = 2; x < c_size - 2; x++)
	{
		for (y = 2; y < v_size - 2; y++)
		{
			if (*(data + x * v_size + y) > minvalue)
			{
				if ((*(data + x * v_size + y) > *(data + (x - 2) * v_size + y - 2) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y - 1) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + (x - 1) * v_size + y - 2) and
					*(data + x * v_size + y) >= *(data + (x - 1) * v_size + y - 1) and
					*(data + x * v_size + y) >= *(data + (x - 1) * v_size + y) and
					*(data + x * v_size + y) >= *(data + (x - 1) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x - 1) * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + x * v_size + y - 2) and
					*(data + x * v_size + y) >= *(data + x * v_size + y - 1) and
					*(data + x * v_size + y) >= *(data + x * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + x * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + (x + 1) * v_size + y - 2) and
					*(data + x * v_size + y) >= *(data + (x + 1) * v_size + y - 1) and
					*(data + x * v_size + y) >= *(data + (x + 1) * v_size + y) and
					*(data + x * v_size + y) >= *(data + (x + 1) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x + 1) * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y - 2) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y - 1) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y + 2)) or
					(*(data + x * v_size + y) > *(data + (x - 1) * v_size + y - 1) and
						*(data + x * v_size + y) > *(data + (x - 1) * v_size + y) and
						*(data + x * v_size + y) > *(data + (x - 1) * v_size + y + 1) and
						*(data + x * v_size + y) > *(data + x * v_size + y - 1) and
						*(data + x * v_size + y) > *(data + x * v_size + y + 1) and
						*(data + x * v_size + y) > *(data + (x + 1) * v_size + y - 1) and
						*(data + x * v_size + y) > *(data + (x + 1) * v_size + y) and
						*(data + x * v_size + y) > *(data + (x + 1) * v_size + y + 1))
					)
				{
					if (
						(*(data + (x - 1) * v_size + y - 1) +
							*(data + (x - 1) * v_size + y) +
							*(data + (x - 1) * v_size + y + 1) +
							*(data + x * v_size + y - 1) +
							*(data + x * v_size + y + 1) +
							*(data + (x + 1) * v_size + y - 1) +
							*(data + (x + 1) * v_size + y) +
							*(data + (x + 1) * v_size + y + 1)) > minvalue * 8 and *(data + x * v_size + y)>threshold)
					{
						(*(image + x * v_size + y))++;
					}
				}
			}
		}
	}
}



GENCALLBACK_API void _stdcall find_peak_16(UINT16 * data, UINT16 * image, int c_size, int v_size, int minvalue, int threshold)
{
	int x = 0;
	int y = 0;
	for (x = 2; x < c_size - 2; x++)
	{
		for (y = 2; y < v_size - 2; y++)
		{
			if (*(data + x * v_size + y) > minvalue)
			{
				if ((*(data + x * v_size + y) > *(data + (x - 2) * v_size + y - 2) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y - 1) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x - 2) * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + (x - 1) * v_size + y - 2) and
					*(data + x * v_size + y) >= *(data + (x - 1) * v_size + y - 1) and
					*(data + x * v_size + y) >= *(data + (x - 1) * v_size + y) and
					*(data + x * v_size + y) >= *(data + (x - 1) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x - 1) * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + x * v_size + y - 2) and
					*(data + x * v_size + y) >= *(data + x * v_size + y - 1) and
					*(data + x * v_size + y) >= *(data + x * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + x * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + (x + 1) * v_size + y - 2) and
					*(data + x * v_size + y) >= *(data + (x + 1) * v_size + y - 1) and
					*(data + x * v_size + y) >= *(data + (x + 1) * v_size + y) and
					*(data + x * v_size + y) >= *(data + (x + 1) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x + 1) * v_size + y + 2) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y - 2) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y - 1) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x + 2) * v_size + y + 2)) or
					(*(data + x * v_size + y) > *(data + (x - 1) * v_size + y - 1) and
					*(data + x * v_size + y) > *(data + (x - 1) * v_size + y) and
					*(data + x * v_size + y) > *(data + (x - 1) * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + x * v_size + y - 1) and
					*(data + x * v_size + y) > *(data + x * v_size + y + 1) and
					*(data + x * v_size + y) > *(data + (x + 1) * v_size + y - 1) and
					*(data + x * v_size + y) > *(data + (x + 1) * v_size + y) and
					*(data + x * v_size + y) > *(data + (x + 1) * v_size + y + 1))
					)
				{
					if (
						(*(data + (x - 1) * v_size + y - 1)+ 
						*(data + (x - 1) * v_size + y)+ 
						*(data + (x - 1) * v_size + y + 1)+ 
						*(data + x * v_size + y - 1)+ 
						*(data + x * v_size + y + 1)+ 
						*(data + (x + 1) * v_size + y - 1)+
						*(data + (x + 1) * v_size + y)+
						*(data + (x + 1) * v_size + y + 1))> minvalue*8 and *(data + x * v_size + y) > threshold)
					{
						(*(image + x * v_size + y))++;
					}
					
				}
			}
		}
	}
}


GENCALLBACK_API void _stdcall add_arry_8(UINT8 * data, UINT32 * image, int height, int width)
{
	for (int i = 0; i < height; i++)
	{
		for (int k = 0; k < width; k++)
		{
			*(image + i * width + k) += *(data + i * width + k);
		}
	}
}



GENCALLBACK_API void _stdcall add_arry_16(UINT16 * data, UINT32 * image, int height, int width)
{
	for (int i = 0; i < height; i++)
	{
		for (int k = 0; k < width; k++)
		{
			*(image + i * width + k) += *(data + i * width + k);
		}
	}
}

GENCALLBACK_API void _stdcall get_spectral_16(UINT16 * data, UINT32 * spectral, int height, int width)
{
	for (int k = 0; k < width; k++)
	{
		for (int i = 0; i < height; i++)
		{
			*(spectral + k) += *(data + i * width + k);
		}
	}
}

GENCALLBACK_API void _stdcall get_spectral_8(UINT8 * data, UINT32 * spectral, int height, int width)
{
	for (int k = 0; k < width; k++)
	{
		for (int i = 0; i < height; i++)
		{
			*(spectral + k) += *(data + i * width + k);
		}
	}
}
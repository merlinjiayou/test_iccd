#pragma once

#ifdef GENCALLBACK_EXPORTS
#define GENCALLBACK_API __declspec(dllimport)
#else
#define GENCALLBACK_API __declspec(dllexport) 
#endif

extern "C" GENCALLBACK_API void _stdcall find_peak_8(UINT8 * data, UINT16 * image, int c_size, int v_size, int minvalue,int threshold);
extern "C" GENCALLBACK_API void _stdcall find_peak_16(UINT16 * data, UINT16 * image, int c_size, int v_size, int minvalue, int threshold);
extern "C" GENCALLBACK_API void _stdcall add_arry_8(UINT8 * data, UINT32 * image, int height, int width);
extern "C" GENCALLBACK_API void _stdcall add_arry_16(UINT16 * data, UINT32 * image, int height, int width);
extern "C" GENCALLBACK_API void _stdcall get_spectral_16(UINT16 * data, UINT32 * spectral, int height, int width);
extern "C" GENCALLBACK_API void _stdcall get_spectral_8(UINT8 * data, UINT32 * spectral, int height, int width);

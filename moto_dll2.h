//interface for 3rd party applications
//TODO: add all interface functions

#ifndef _MOTO_DLL_2_H_
#define _MOTO_DLL_2_H_

typedef void (__stdcall *READ_CALLBACK)(int, int, double, void *, int);

#define MOTO_DLL_2_API __declspec( dllimport )

MOTO_DLL_2_API int _cdecl InitParser();
MOTO_DLL_2_API int _cdecl EnumDevices(bool doClosePorts);
MOTO_DLL_2_API int _cdecl OpenPort(int num);
MOTO_DLL_2_API int _cdecl ClosePort(int num);
MOTO_DLL_2_API int _cdecl ReadVal(int inv,char *name,double *val);
MOTO_DLL_2_API int _cdecl WriteVal(int inv,char *name,double val);
MOTO_DLL_2_API int _cdecl StartPLC(int inv, int plcnum);
MOTO_DLL_2_API int _cdecl StopPLC(int inv);

MOTO_DLL_2_API int _cdecl LoadProgram(int motor,int bank, short *program, int *version);
MOTO_DLL_2_API int _cdecl WriteProgram(int motor,int bank,short *program,int len, int version);

MOTO_DLL_2_API int _cdecl GetPortName(int inv,char *buf);
MOTO_DLL_2_API int _cdecl AddParamToStream(int inv,char *name,READ_CALLBACK onPoint);
MOTO_DLL_2_API int _cdecl RemoveParamFromStream(int inv,char *name);
MOTO_DLL_2_API int _cdecl StartStream(int inv);
MOTO_DLL_2_API int _cdecl StopStream(int inv);

MOTO_DLL_2_API void _cdecl CloseParser();

#endif
#pragma once
// Imager IPC.h
// Definitions for Imager Interprocess Communication

#ifdef __cplusplus 
extern "C"
{
#endif

#ifdef IMAGERIPC_EXPORTS
#define IMAGERIPC_API __declspec(dllexport)
#else
#define IMAGERIPC_API __declspec(dllimport)
#endif

#ifndef WINAPI
#define WINAPI __stdcall 
#endif

#ifndef HRESULT
#define HRESULT long
#endif

struct FCOORD
{
   float  x;
   float  y;
};

struct FRANGE
{
	float  Min;
	float  Max;
};

enum TIPCMode { ipcColors, ipcTemps, ipcADUs };
enum TFlagState {fsFlagOpen, fsFlagClose, fsFlagOpening, fsFlagClosing, fsError};
enum MeasureAreaType { maUndefined = 0, maMeasureArea = 1, maCalculatedArea = 2, maMouseCursor = 3, maChip = 4, maInternal = 5, maReference = 6};
enum TFileCommand { fcNone, fcSnapshot, fcRecord, fcStop, fcPlay, fcPause, fcScreenshot, fcShow };	// moved to here with T#946

struct FrameMetadata
{
	unsigned short Size;	// size of this structure
	unsigned int Counter;	// frame counter
	unsigned int CounterHW;	// frame counter hardware
	long long Timestamp;	// time stamp in UNITS (10000000 per second)
	long long TimestampMedia;
	TFlagState FlagState;
	float TempChip;
	float TempFlag;
	float TempBox;
	WORD PIFin[2];			
	// DI = PIFin[0] & 0x8000
	// AI1 = PIFin[0] & 0x03FF
	// AI2 = PIFin[1] & 0x03FF
};

#pragma pack(push)
#pragma pack(2) // Part of T#571
struct FrameMetadata2
{
    unsigned short Size;	// size of this structure
    unsigned int Counter;	// frame counter
    unsigned int CounterHW;	// frame counter hardware
    long long Timestamp;	// time stamp in UNITS (10000000 per second)
    long long TimestampMedia;
    TFlagState FlagState;
    BOOL IsSameFrame;	 // Part of T#153,  is true if we have the same CounterHW and nothing changed in between since last time
    float TempChip;
    float TempFlag;
    float TempBox;
    float TempOptics;
    unsigned short LensPosition; // Lens position
    FCOORD HotSpot;     // Hot spot position
    FCOORD ColdSpot;    // Cold spot position

    WORD PIFnDI;        // PIF DI (digital input) number of inputs
    DWORD PIFDI;        // PIF DI (digital input), bit field
    WORD PIFnAI;        // PIF AI (analog input) number of inputs
    WORD PIFAI[1];       // PIF AI (analog input) flexible array
};
#pragma pack(pop)

struct VideoFormat
{
	int WidthIR;
	int HeightIR;
	int FramerateIR;
	int WidthVisible;
	int HeightVisible;
	int FramerateVisible;
};

enum TRotationMode {
	rmOff,		// off
	rmCW90,		// clockwise 90 degrees
	rmACW90,	// anti-clockwise 90 degrees
	rmCW180,	// clockwise 180 degrees
	rmCWH,		// clockwise horizontal diagonal
	rmCWV,		// clockwise vertical diagonal
	rmACWH,		// anti-clockwise horizontal diagonal
	rmACWV,		// anti-clockwise vertical diagonal
	rmUser		// user defined
};

enum TZoomMode {
	zmOff,		// off
	zmMax,		// maximal (diagonal to the square)
	zmUser		// user defined
};

struct IRArranging
{
	TRotationMode Rotation;
	float RotationAngle;
	BOOL Zoom;
	RECT ZoomRect;
};

//begin: part of T#167
enum MeasureAreaShape
{
	masOff,
	masMP1x1,
	masMP2x2,
	masMP3x3,
	masMP5x5,
	masUserDefRect,
	masEllipse,
	masPolygon,
	masCurve
};

enum MeasureAreaMode
{
	mamMin,
	mamMax,
	mamAvg,
	mamDist
};

struct MeasureArea
{		
	MeasureAreaShape	Shape;
	MeasureAreaMode		Mode;
	BOOL				BindToTempProfile;
	BOOL				UseEmissivity;
	float				Emissivity;
	BOOL				ShowInDigDispGroup;
	float				distMin;
	float				distMax;
	POINT				Location;
	SIZE				Size;
	BOOL				IsHotSpot;
	BOOL				IsColdSpot;	
};
//end: part of T#167

struct AlarmSetting
{	
	USHORT			Index;
	MeasureAreaType Type;
	FRANGE			AlarmRange;
	FRANGE			PreAlarmRange;
	FRANGE			DispRange;
	bool			DisplayWarning;
};

struct TTParams
{
    float T1, T3;
    short E1, E3;
    float Lambda; // the central wave length of the Planck function
    float Lambda2; // the central wave length of second range after TJunct (e.g. for PI1M)
    float TJunct; // crossover temperature of junction point between both ranges (e.g. planckian part and logaritmic-planckian part for PI1M)
    short EJunct; // energy of TJunct
    bool Normalize; // Part of NF1152
};

// IPC events (polling mode)
#define IPC_EVENT_INIT_COMPLETED	0x0001
#define IPC_EVENT_SERVER_STOPPED	0x0002
#define IPC_EVENT_CONFIG_CHANGED	0x0004
#define IPC_EVENT_FILE_CMD_READY	0x0008
#define IPC_EVENT_FRAME_INIT		0x0010
#define IPC_EVENT_VIS_FRAME_INIT	0x0020
#define IPC_EVENT_NEW_NMEA_STRING	0x0040
#define IPC_EVENT_FILE_COMMAND  	0x0080
#define IPC_EVENT_PLAY_METADATA	    0x0100
#define IPC_EVENT_LSSLIT_CENTER	    0x0200
#define IPC_EVENT_NEW_RAWFILESTATE  0x0400
#define IPC_EVENT_AREAS_INIT		0x0800

// groups of logging, for function SetLogging(int LogGroups)
#define LOGGRP_INIT			0x00000001
#define LOGGRP_ALIVE		0x00000002
#define LOGGRP_FRAME		0x00000004
#define LOGGRP_FRAMEINIT	0x00000008
#define LOGGRP_STRING		0x00000010
#define LOGGRP_STATE		0x00000020
#define LOGGRP_COMMAND		0x00000040
#define LOGGRP_DEVINFO		0x00000100
#define LOGGRP_DEVSETUP		0x00000200
#define LOGGRP_DEVDATA		0x00000400
#define LOGGRP_PIFSETUP		0x00000800
#define LOGGRP_PIFDATA		0x00001000
#define LOGGRP_SYSINFO		0x00002000

// logging levels, for function SetLogFile(wchar_t *LogFilename, int LogLevel, bool Append)
#define LOGLEV_INIT			1
#define LOGLEV_COMMAND		2
#define LOGLEV_FRAME		3
#define LOGLEV_FRAMEPLUS	4


// type definitions for function pointer
typedef HRESULT (WINAPI *fpOnServerStopped)(int reason);
typedef HRESULT (WINAPI *fpOnFrameInit)(int, int, int);
typedef HRESULT (WINAPI *fpOnAreasInit)(int, int); // T#1229
typedef HRESULT (WINAPI *fpOnNewFrame)(char*, int);
typedef HRESULT (WINAPI *fpOnNewFrameEx)(void*, FrameMetadata*);
typedef HRESULT (WINAPI *fpOnNewFrameEx2)(void*, FrameMetadata2*);
typedef HRESULT (WINAPI *fpOnInitCompleted)(void );
typedef HRESULT (WINAPI *fpOnConfigChanged)(long reserved);
typedef HRESULT (WINAPI *fpOnStringSend)(wchar_t *Path);
typedef HRESULT( WINAPI *fpOnBufferSend)(BYTE *Path);
typedef HRESULT( WINAPI *fpOnFileCommand)(TFileCommand Cmd);
typedef HRESULT(WINAPI *fpOnNewRawFileState)(CHAR State);

IMAGERIPC_API HRESULT WINAPI SetImagerIPCCount(WORD count);
IMAGERIPC_API HRESULT WINAPI InitImagerIPC(WORD index);
IMAGERIPC_API HRESULT WINAPI InitNamedImagerIPC(WORD index, wchar_t *InstanceName);
IMAGERIPC_API HRESULT WINAPI RunImagerIPC(WORD index);
IMAGERIPC_API HRESULT WINAPI StartImagerIPC(WORD index);
IMAGERIPC_API HRESULT WINAPI ReleaseImagerIPC(WORD index);
IMAGERIPC_API HRESULT WINAPI ImagerIPCProcessMessages(WORD index);
IMAGERIPC_API HRESULT WINAPI AcknowledgeFrame(WORD index);
IMAGERIPC_API HRESULT WINAPI GetFrameConfig(WORD index, int *pWidth, int *pHeight, int *pDepth);
IMAGERIPC_API HRESULT WINAPI GetVisibleFrameConfig(WORD index, int *pWidth, int *pHeight, int *pDepth);
IMAGERIPC_API HRESULT WINAPI GetFrame(WORD index, WORD timeout, void *pBuf, unsigned int  Size, FrameMetadata *pMetadata); //Get frame with metadata structure 1
IMAGERIPC_API HRESULT WINAPI GetVisibleFrame(WORD index, WORD timeout, void *pBuf, unsigned int Size, FrameMetadata *pMetadata); //Get frame with metadata structure 2
IMAGERIPC_API HRESULT WINAPI GetFrameMetadataSize(WORD index, int *pMetadataSize);
IMAGERIPC_API HRESULT WINAPI GetFrame2(WORD index, WORD timeout, void *pDataBuf, unsigned int DataSize, void *pMetadata, unsigned int MetadataSize); //Get frame with metadata structure 2
IMAGERIPC_API HRESULT WINAPI GetAreas(WORD index, WORD timeout, void *pDataBuf, unsigned int DataSize, void *pMetadata, unsigned int MetadataSize); //Get frame with metadata structure 2
IMAGERIPC_API HRESULT WINAPI GetVisibleFrame2(WORD index, WORD timeout, void *pDataBuf, unsigned int DataSize, void *pMetadata, unsigned int MetadataSize); //Get frame with metadata structure 2
IMAGERIPC_API HRESULT WINAPI SetLogFile(wchar_t *LogFilename, int LogLevel, bool Append);
IMAGERIPC_API HRESULT WINAPI SetLogging(int LogGroups);
IMAGERIPC_API HRESULT WINAPI Log(WORD index, char *logstring, int LogLevel);

//--------------------------------------------------------------------------------------
// Callback procedures:
IMAGERIPC_API HRESULT WINAPI SetCallback_OnServerStopped(WORD index, fpOnServerStopped OnServerStopped);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnFrameInit(WORD index, fpOnFrameInit OnFrameInit);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnAreasInit(WORD index, fpOnAreasInit OnAreasInit); // T#1229
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewFrame(WORD index, fpOnNewFrame OnNewFrame);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewFrameEx(WORD index, fpOnNewFrameEx OnNewFrameEx);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewFrameEx2(WORD index, fpOnNewFrameEx2 OnNewFrameEx);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnVisibleFrameInit(WORD index, fpOnFrameInit OnVisibleFrameInit);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewVisibleFrame(WORD index, fpOnNewFrame OnNewVisibleFrame);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewVisibleFrameEx(WORD index, fpOnNewFrameEx OnNewVisibleFrameEx);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewVisibleFrameEx2(WORD index, fpOnNewFrameEx2 OnNewVisibleFrameEx);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewAreasBuffer(WORD index, fpOnNewFrameEx2 OnNewAreasBuffer); // T#1229
IMAGERIPC_API HRESULT WINAPI SetCallback_OnInitCompleted(WORD index, fpOnInitCompleted OnInitCompleted);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnConfigChanged(WORD index, fpOnConfigChanged OnConfigChanged);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnFileCommand(WORD index, fpOnFileCommand OnFileCommand);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnFileCommandReady(WORD index, fpOnStringSend OnFileCommandReady);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewNMEAString(WORD index, fpOnStringSend OnNewNMEAString);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnPlayMetadata(WORD index, fpOnBufferSend OnPlayMetadata);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnLSSlitCenterLine(WORD index, fpOnBufferSend OnLSSlitCenterLine);
IMAGERIPC_API HRESULT WINAPI SetCallback_OnNewRawFileState(WORD index, fpOnNewRawFileState OnNewRawFileState);

//--------------------------------------------------------------------------------------
// Get & Set procedures: 
IMAGERIPC_API __int64 WINAPI GetVersionApplication(WORD index);
IMAGERIPC_API __int64 WINAPI GetVersionHID_DLL(WORD index);
IMAGERIPC_API __int64 WINAPI GetVersionCD_DLL(WORD index);
IMAGERIPC_API __int64 WINAPI GetVersionIPC_DLL(WORD index);

IMAGERIPC_API float WINAPI GetTempChip(WORD index);
IMAGERIPC_API float WINAPI GetTempFlag(WORD index);
IMAGERIPC_API float WINAPI GetTempProc(WORD index); 
IMAGERIPC_API float WINAPI GetTempBox(WORD index);
IMAGERIPC_API float WINAPI GetTempHousing(WORD index);	//deprecated
IMAGERIPC_API float WINAPI GetTempOptics(WORD index);
IMAGERIPC_API float WINAPI GetTempTarget(WORD index);
IMAGERIPC_API float WINAPI GetHumidity(WORD index); //deprecated
IMAGERIPC_API USHORT WINAPI GetTempRangeCount(WORD index);
IMAGERIPC_API USHORT WINAPI GetOpticsCount(WORD index);
IMAGERIPC_API USHORT WINAPI GetMeasureAreaCount(WORD index);
IMAGERIPC_API USHORT WINAPI GetVideoFormatCount(WORD index);
IMAGERIPC_API HRESULT WINAPI GetClippedFormatMaxPos(WORD index, PPOINT Pos);
IMAGERIPC_API float WINAPI GetTempMinRange(WORD index, ULONG Index);
IMAGERIPC_API float WINAPI GetTempMaxRange(WORD index, ULONG Index);
IMAGERIPC_API USHORT WINAPI GetOpticsFOV(WORD index, ULONG Index);
IMAGERIPC_API ULONG WINAPI GetOpticsSerialNumber(WORD index, ULONG Index); 
IMAGERIPC_API float WINAPI GetTempMeasureArea(WORD index, ULONG Index);
IMAGERIPC_API HRESULT WINAPI GetLocMeasureArea(WORD index, ULONG Index, PPOINT Loc);
IMAGERIPC_API HRESULT WINAPI SetLocMeasureArea(WORD index, ULONG Index, POINT Loc);
IMAGERIPC_API USHORT WINAPI GetInitCounter(WORD index);
IMAGERIPC_API USHORT WINAPI GetIPCState(WORD index, bool reset);
IMAGERIPC_API USHORT WINAPI GetIPCMode(WORD index);
IMAGERIPC_API USHORT WINAPI SetIPCMode(WORD index, USHORT Value);
IMAGERIPC_API USHORT WINAPI GetFrameQueue(WORD index);				
IMAGERIPC_API USHORT WINAPI GetVisibleFrameQueue(WORD index);
IMAGERIPC_API USHORT WINAPI GetAreasQueue(WORD index);
IMAGERIPC_API HRESULT WINAPI GetLinescannerSlitMin(WORD index, PPOINT point);
IMAGERIPC_API HRESULT WINAPI GetLinescannerSlitMax(WORD index, PPOINT point);
IMAGERIPC_API BOOL WINAPI GetLinescannerSlitOrientation(WORD index);
IMAGERIPC_API HRESULT WINAPI GetSourceResolutionIR(WORD index, PSIZE size);
IMAGERIPC_API HRESULT WINAPI GetVideoFormat(WORD index, ULONG Index, VideoFormat *videoFormat);
IMAGERIPC_API HRESULT WINAPI GetIRArranging(WORD index, IRArranging *irArranging); 
IMAGERIPC_API HRESULT WINAPI SetIRArranging(WORD index, IRArranging *irArranging); 
IMAGERIPC_API HRESULT WINAPI GetPathOfStoredFile(WORD index, wchar_t *path, int maxlen);
IMAGERIPC_API HRESULT WINAPI GetNewNMEAString(WORD index, wchar_t *path, int maxlen);
IMAGERIPC_API HRESULT WINAPI GetMeasureArea(WORD index, ULONG Index, MeasureArea *measureArea); //part of #T167
IMAGERIPC_API HRESULT WINAPI SetMeasureArea(WORD index, ULONG Index, MeasureArea *measureArea, bool addNew);  //part of #T167
IMAGERIPC_API HRESULT WINAPI RemoveMeasureArea(WORD index, ULONG Index);  //part of #T167
IMAGERIPC_API HRESULT WINAPI AddMeasureAreaPoint(WORD index, ULONG Index, POINT point);  //part of #T167
IMAGERIPC_API HRESULT WINAPI SetMeasureAreaName(WORD index, ULONG Index, wchar_t *name);  //part of #T167
IMAGERIPC_API HRESULT WINAPI GetMeasureAreaName(WORD index, ULONG Index, wchar_t *name, int *len, int maxLen);  //part of #T167
IMAGERIPC_API HRESULT WINAPI SetAlarmThreshold(WORD index, AlarmSetting setting);
IMAGERIPC_API HRESULT WINAPI GetAlarmThreshold(WORD index, MeasureAreaType type, ULONG Index, AlarmSetting* setting);

IMAGERIPC_API bool WINAPI GetFlag(WORD index);
IMAGERIPC_API bool WINAPI SetFlag(WORD index, bool Value);
IMAGERIPC_API USHORT WINAPI GetOpticsIndex(WORD index);
IMAGERIPC_API USHORT WINAPI SetOpticsIndex(WORD index, USHORT Value);
IMAGERIPC_API USHORT WINAPI GetTempRangeIndex(WORD index);
IMAGERIPC_API USHORT WINAPI SetTempRangeIndex(WORD index, USHORT Value);
IMAGERIPC_API USHORT WINAPI GetExtTempRangeMode(WORD index);	// T#1346
IMAGERIPC_API USHORT WINAPI SetExtTempRangeMode(WORD index, USHORT Value);	// T#1346
IMAGERIPC_API USHORT WINAPI GetVideoFormatIndex(WORD index);
IMAGERIPC_API USHORT WINAPI SetVideoFormatIndex(WORD index, USHORT Value);
IMAGERIPC_API HRESULT WINAPI GetClippedFormatPos(WORD index, PPOINT Pos);
IMAGERIPC_API HRESULT WINAPI SetClippedFormatPos(WORD index, POINT Pos);
IMAGERIPC_API USHORT WINAPI GetTempRangeDecimal(WORD index, bool Effective);
IMAGERIPC_API bool   WINAPI GetMainWindowEmbedded(WORD index);
IMAGERIPC_API bool   WINAPI SetMainWindowEmbedded(WORD index, bool Value);
IMAGERIPC_API USHORT WINAPI GetMainWindowLocX(WORD index);
IMAGERIPC_API USHORT WINAPI SetMainWindowLocX(WORD index, USHORT Value);
IMAGERIPC_API USHORT WINAPI GetMainWindowLocY(WORD index);
IMAGERIPC_API USHORT WINAPI SetMainWindowLocY(WORD index, USHORT Value);
IMAGERIPC_API USHORT WINAPI GetMainWindowWidth(WORD index);
IMAGERIPC_API USHORT WINAPI SetMainWindowWidth(WORD index, USHORT Value);
IMAGERIPC_API USHORT WINAPI GetMainWindowHeight(WORD index);
IMAGERIPC_API USHORT WINAPI SetMainWindowHeight(WORD index, USHORT Value);
IMAGERIPC_API float	 WINAPI GetFixedEmissivity(WORD index);
IMAGERIPC_API float	 WINAPI SetFixedEmissivity(WORD index, float Value);
IMAGERIPC_API float	 WINAPI GetFixedTransmissivity(WORD index);
IMAGERIPC_API float	 WINAPI SetFixedTransmissivity(WORD index, float Value);
IMAGERIPC_API float	 WINAPI GetFixedTempAmbient(WORD index);
IMAGERIPC_API float	 WINAPI SetFixedTempAmbient(WORD index, float Value);
IMAGERIPC_API float	 WINAPI GetFixedTempReference(WORD index);
IMAGERIPC_API float	 WINAPI SetFixedTempReference(WORD index, float Value);
IMAGERIPC_API float	 WINAPI SetPifOut(WORD index, WORD channel, float Value);
IMAGERIPC_API USHORT WINAPI GetPifAICount(WORD index);
IMAGERIPC_API USHORT WINAPI GetPifDICount(WORD index);
IMAGERIPC_API USHORT WINAPI GetPifAOCount(WORD index);
IMAGERIPC_API USHORT WINAPI GetPifDOCount(WORD index);
IMAGERIPC_API USHORT WINAPI GetPifFSCount(WORD index);
IMAGERIPC_API float	 WINAPI SetPifAO(WORD index, WORD PifChn, float Value);
IMAGERIPC_API bool 	 WINAPI SetPifDO(WORD index, WORD PifChn, bool Value);
IMAGERIPC_API float  WINAPI GetPifAI(WORD index, WORD PifChn);
IMAGERIPC_API ULONG  WINAPI GetPifDI(WORD index);
IMAGERIPC_API bool   WINAPI FailSafe(WORD index, bool Value);


IMAGERIPC_API UCHAR  WINAPI GetHardware_Spec(WORD index); // deprecated
IMAGERIPC_API ULONG  WINAPI GetSerialNumber(WORD index);
IMAGERIPC_API ULONG  WINAPI GetSerialNumberULIS(WORD index); // deprecated
IMAGERIPC_API ULONG  WINAPI GetAvgTimePerFrame(WORD index);
IMAGERIPC_API __int64 WINAPI GetRecordingStartTime(WORD index);
IMAGERIPC_API ULONG  WINAPI GetVisibleAvgTimePerFrame(WORD index);
IMAGERIPC_API USHORT WINAPI GetFirmware_MSP(WORD index); // deprecated
IMAGERIPC_API USHORT WINAPI GetFirmware_Cypress(WORD index); // deprecated
IMAGERIPC_API USHORT WINAPI GetHardwareRev(WORD index);
IMAGERIPC_API USHORT WINAPI GetFirmwareRev(WORD index);
IMAGERIPC_API USHORT WINAPI GetPID(WORD index);
IMAGERIPC_API USHORT WINAPI GetVID(WORD index);
IMAGERIPC_API ULONG  WINAPI GetPIFSerialNumber(WORD index);
IMAGERIPC_API USHORT WINAPI GetPIFVersion(WORD index);
IMAGERIPC_API USHORT WINAPI GetPifType(WORD index);
IMAGERIPC_API USHORT WINAPI GetFocusmotorMinPos(WORD index);
IMAGERIPC_API USHORT WINAPI GetFocusmotorMaxPos(WORD index);
IMAGERIPC_API USHORT WINAPI GetFocusmotorPos(WORD index);
IMAGERIPC_API USHORT WINAPI SetFocusmotorPos(WORD index, USHORT value);
//IMAGERIPC_API float	 WINAPI GetPlayrate(WORD index);
//IMAGERIPC_API float	 WINAPI SetPlayrate(WORD index, float Value);
IMAGERIPC_API int WINAPI GetPlayingCurrentPosition(WORD index);
IMAGERIPC_API int WINAPI SetPlayingCurrentPosition(WORD index, int CurPos);
IMAGERIPC_API int WINAPI GetPlayingStopPosition(WORD index);
IMAGERIPC_API __int64 WINAPI GetPlayingDuration(WORD index);

//--------------------------------------------------------------------------------------
// Control commands:
IMAGERIPC_API void WINAPI ResetFlag(WORD index);
IMAGERIPC_API bool WINAPI RenewFlag(WORD index);
IMAGERIPC_API void WINAPI CloseApplication(WORD index);
IMAGERIPC_API void WINAPI ReinitDevice(WORD index);
IMAGERIPC_API void WINAPI FileSnapshot(WORD index);
IMAGERIPC_API void WINAPI FileScreenshot(WORD index);
IMAGERIPC_API void WINAPI FileRecord(WORD index);
IMAGERIPC_API void WINAPI FileStop(WORD index); 
IMAGERIPC_API void WINAPI FilePlay(WORD index);
IMAGERIPC_API void WINAPI FilePause(WORD index); 
IMAGERIPC_API USHORT WINAPI FileOpen(WORD index, wchar_t * FileName);
IMAGERIPC_API void WINAPI RawFileRecord(WORD index); // internal use only
IMAGERIPC_API void WINAPI RawFileStop(WORD index); // internal use only
IMAGERIPC_API void WINAPI RawFilePlay(WORD index); // internal use only
IMAGERIPC_API void WINAPI RawFilePause(WORD index); // internal use only
IMAGERIPC_API USHORT WINAPI LoadLayout(WORD index, wchar_t * LayoutName);
IMAGERIPC_API void WINAPI LoadCurrentLayout(WORD index);
IMAGERIPC_API void WINAPI SaveCurrentLayout(WORD index);
IMAGERIPC_API USHORT WINAPI SaveLayout(WORD index, wchar_t * LayoutName);
IMAGERIPC_API void WINAPI SetStandardLayout(WORD index);
IMAGERIPC_API USHORT WINAPI MasterInstanceName(WORD index, wchar_t * InstanceName);

#ifdef __cplusplus 
}
#endif
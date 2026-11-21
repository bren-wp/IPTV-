!include "MUI2.nsh"
!ifndef VERSION
  !error "VERSION must be supplied"
!endif
!ifndef PAYLOAD
  !error "PAYLOAD must be supplied"
!endif
!ifndef OUTPUT
  !error "OUTPUT must be supplied"
!endif

Unicode True
Name "IPTV+"
OutFile "${OUTPUT}"
InstallDir "$LOCALAPPDATA\Programs\IPTVPlus"
RequestExecutionLevel user
ShowInstDetails show
ShowUninstDetails show
SetCompressor /SOLID lzma
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "IPTV+"
VIAddVersionKey "CompanyName" "Brendigo"
VIAddVersionKey "FileDescription" "IPTV+ Setup"
VIAddVersionKey "FileVersion" "${VERSION}"

!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Croatian"

Section "IPTV+" Main
  SetOutPath "$INSTDIR"
  File /r "${PAYLOAD}\*"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\IPTV+"
  CreateShortcut "$SMPROGRAMS\IPTV+\IPTV+.lnk" "$INSTDIR\iptvplus.exe"
  CreateShortcut "$SMPROGRAMS\IPTV+\Deinstaliraj.lnk" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\IPTVPlus" "DisplayName" "IPTV+"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\IPTVPlus" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\IPTVPlus" "DisplayVersion" "${VERSION}"
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\IPTV+\IPTV+.lnk"
  Delete "$SMPROGRAMS\IPTV+\Deinstaliraj.lnk"
  RMDir "$SMPROGRAMS\IPTV+"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\IPTVPlus"
  RMDir /r "$INSTDIR"
SectionEnd

!include "MUI2.nsh"
!include "LogicLib.nsh"

!ifndef VERSION
  !error "VERSION must be provided"
!endif
!ifndef EDITION
  !error "EDITION must be provided"
!endif
!ifndef PAYLOAD
  !error "PAYLOAD directory must be provided"
!endif
!ifndef OUTPUT
  !error "OUTPUT file must be provided"
!endif

Unicode True
Name "IPTV+ ${EDITION}"
OutFile "${OUTPUT}"
InstallDir "$LOCALAPPDATA\\Programs\\IPTVPlus\\${EDITION}"
RequestExecutionLevel user
ShowInstDetails show
ShowUninstDetails show
SetCompressor /SOLID lzma
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "IPTV+ ${EDITION}"
VIAddVersionKey "CompanyName" "Brendigo"
VIAddVersionKey "FileDescription" "IPTV+ ${EDITION} Setup"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "LegalCopyright" "IPTV+ downstream changes © 2026 Brendigo"

!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Croatian"

Section "IPTV+ ${EDITION}" Main
  SetOutPath "$INSTDIR"
  File /r "${PAYLOAD}\\*"
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\\IPTV+ ${EDITION}"
  CreateShortcut "$SMPROGRAMS\\IPTV+ ${EDITION}\\IPTV+ ${EDITION}.lnk" "$INSTDIR\\iptvplus.exe"
  CreateShortcut "$SMPROGRAMS\\IPTV+ ${EDITION}\\Deinstaliraj.lnk" "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\IPTVPlus${EDITION}" "DisplayName" "IPTV+ ${EDITION}"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\IPTVPlus${EDITION}" "UninstallString" '"$INSTDIR\\Uninstall.exe"'
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\IPTVPlus${EDITION}" "DisplayVersion" "${VERSION}"
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\\IPTV+ ${EDITION}\\IPTV+ ${EDITION}.lnk"
  Delete "$SMPROGRAMS\\IPTV+ ${EDITION}\\Deinstaliraj.lnk"
  RMDir "$SMPROGRAMS\\IPTV+ ${EDITION}"
  DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\IPTVPlus${EDITION}"
  RMDir /r "$INSTDIR"
SectionEnd

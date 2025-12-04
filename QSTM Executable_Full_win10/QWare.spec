# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['F:\\PHD Semesters IUPUI (2022_2027)\\Q-Ware Software Venv\\Q-Ware_modified23\\QWare.py'],
             pathex=['F:\\PHD Semesters IUPUI (2022_2027)\\Q-Ware Software Venv\\Executable_Full'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='QWare',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

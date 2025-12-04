# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['D:\\Q-Ware Software Venv_win11\\Q-Ware_modified23\\QwarePRS_Open.py'],
             pathex=['D:\\Q-Ware Software Venv_win11\\QSTM Exec_win11'],
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
          name='QwarePRS_Open',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

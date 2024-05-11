# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import rapidocr_openvino


block_cipher = None

package_name = 'rapidocr_openvino'
install_dir = Path(rapidocr_openvino.__file__).resolve().parent

onnx_paths = list(install_dir.rglob('*.onnx'))
yaml_paths = list(install_dir.rglob('*.yaml'))

onnx_add_data = [(str(v.parent), f'{package_name}/{v.parent.name}')
                 for v in onnx_paths]

yaml_add_data = []
for v in yaml_paths:
    if package_name == v.parent.name:
        yaml_add_data.append((str(v.parent / '*.yaml'), package_name))
    else:
        yaml_add_data.append(
            (str(v.parent / '*.yaml'), f'{package_name}/{v.parent.name}'))

add_data = list(set(yaml_add_data + onnx_add_data))

excludes = ['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter', 'resources', 'matplotlib']
add_data.append(('icon.ico', '.'))
print(f"add_data {add_data}")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=add_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ok-baijing',
    icon='icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

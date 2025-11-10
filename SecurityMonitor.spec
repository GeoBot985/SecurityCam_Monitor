# SecurityMonitor.spec
# --------------------
# PyInstaller build configuration for SecurityMonitor
from PyInstaller.utils.hooks import collect_submodules
import os

block_cipher = None

# Paths
project_root = os.path.abspath("src")
main_script = os.path.join(project_root, "SecurityMonitor", "main.py")
utils_src = os.path.join(project_root, "SecurityMonitor", "utils")

# Include all utils as data (config stays editable)
datas = [
    (utils_src, "SecurityMonitor/utils"),
]

# Collect ultralytics + simpleaudio submodules if used
hiddenimports = collect_submodules("ultralytics") + collect_submodules("simpleaudio")

a = Analysis(
    [main_script],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SecurityMonitor",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # set False if you want silent background mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="SecurityMonitor",
)

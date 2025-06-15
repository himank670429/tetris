# generate the build

```bash
pip install pyinstaller
```

```bash
pyinstaller --onefile --windowed --icon=Assets/icon/icon.ico --add-data "Assets;Assets" main.py

```
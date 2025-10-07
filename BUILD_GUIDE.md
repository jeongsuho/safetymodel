# Windows 실행 파일 빌드 가이드

## 🔨 자동 빌드 방법 (권장)

### 1. 자동 빌드 스크립트 실행

```bash
# Windows
python build_exe.py

# 또는 배치 파일 사용
build.bat
```

### 2. 빌드 프로세스

```
🛡️ 육군 안전 예측 시스템 - 실행 파일 빌드
==================================================

📋 의존성 패키지 확인 중...
✅ PyInstaller
✅ pandas
✅ numpy
✅ openpyxl

빌드 방식을 선택하세요:
1. 간단 빌드 (권장)
2. 고급 빌드 (spec 파일 사용)

선택 (1 또는 2, 기본값: 1): 1

🔨 간단한 빌드 시작...
✅ 간단 빌드 성공!

🎉 빌드 완료!
📁 실행 파일이 dist/ 폴더에 생성되었습니다.
```

### 3. 생성 파일

```
dist/
├── SafetyPredictionSystem.exe  (약 50-100MB)
└── README_실행파일.txt          (사용 설명서)
```

---

## 📋 수동 빌드 방법

### 1. PyInstaller 설치

```bash
pip install pyinstaller
```

### 2. 간단한 빌드

```bash
pyinstaller --onefile --windowed \
  --name=SafetyPredictionSystem \
  --add-data="models;models" \
  --hidden-import=pandas \
  --hidden-import=numpy \
  --hidden-import=openpyxl \
  --hidden-import=sklearn \
  --clean \
  main.py
```

### 3. 고급 빌드 (spec 파일 사용)

#### 3-1. spec 파일 생성

```bash
pyi-makespec --onefile --windowed main.py
```

#### 3-2. spec 파일 편집

`SafetyPredictionSystem.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('models', 'models'),  # 모델 폴더 포함
    ],
    hiddenimports=[
        'pandas',
        'numpy',
        'openpyxl',
        'sklearn',
        'joblib',
        'torch',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SafetyPredictionSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 모드 (콘솔 창 숨김)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # 아이콘 파일 (선택)
)
```

#### 3-3. 빌드 실행

```bash
pyinstaller --clean --noconfirm SafetyPredictionSystem.spec
```

---

## 🎨 아이콘 추가 (선택 사항)

### 1. 아이콘 파일 준비

- 파일명: `icon.ico`
- 형식: Windows ICO (256x256 권장)
- 위치: 프로젝트 루트 폴더

### 2. 아이콘 생성 방법

#### 온라인 변환기 사용
- https://convertio.co/kr/png-ico/
- PNG 이미지를 ICO로 변환

#### Python으로 생성
```python
from PIL import Image

img = Image.open('logo.png')
img.save('icon.ico', format='ICO', sizes=[(256, 256)])
```

---

## ⚙️ 빌드 옵션 설명

### 기본 옵션

| 옵션 | 설명 | 사용 예 |
|------|------|---------|
| `--onefile` | 단일 실행 파일로 패키징 | 권장 |
| `--windowed` | 콘솔 창 숨김 (GUI 모드) | GUI 프로그램 필수 |
| `--console` | 콘솔 창 표시 | 디버깅 시 유용 |
| `--name` | 실행 파일 이름 지정 | `--name=MyApp` |
| `--icon` | 아이콘 파일 지정 | `--icon=icon.ico` |
| `--clean` | 이전 빌드 폴더 정리 | 권장 |
| `--noconfirm` | 덮어쓰기 확인 없음 | 자동 빌드 시 |

### 데이터 포함 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--add-data` | 추가 파일/폴더 포함 | `--add-data="models;models"` (Windows)<br>`--add-data="models:models"` (Linux/Mac) |
| `--add-binary` | 바이너리 파일 포함 | `--add-binary="libcuda.so;."` |

### 모듈 포함 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--hidden-import` | 숨겨진 모듈 포함 | `--hidden-import=pandas` |
| `--collect-all` | 패키지 전체 수집 | `--collect-all=torch` |
| `--exclude-module` | 모듈 제외 | `--exclude-module=matplotlib` |

### 최적화 옵션

| 옵션 | 설명 | 권장 |
|------|------|------|
| `--upx` | UPX 압축 사용 (파일 크기 감소) | ✅ |
| `--strip` | 디버그 심볼 제거 | ✅ |
| `--optimize` | 최적화 레벨 (0-2) | `--optimize=2` |

---

## 🐛 빌드 문제 해결

### 문제 1: PyInstaller 미설치

```
❌ ModuleNotFoundError: No module named 'PyInstaller'

✅ 해결:
pip install pyinstaller
```

### 문제 2: 모듈 누락 오류

```
❌ ModuleNotFoundError: No module named 'xxx'

✅ 해결:
pyinstaller --hidden-import=xxx main.py
```

### 문제 3: 파일 크기 너무 큼

```
❌ 실행 파일 크기: 500MB+

✅ 해결:
1. 불필요한 패키지 제외
   --exclude-module=matplotlib
   --exclude-module=scipy

2. UPX 압축 활성화
   --upx

3. 가상환경 사용
   python -m venv venv
   venv\Scripts\activate
   pip install 필수패키지만
```

### 문제 4: GPU 라이브러리 오류

```
❌ CUDA/cuDNN 라이브러리 누락

✅ 해결:
1. CPU 전용 버전 빌드
   torch.device('cpu')

2. CUDA 라이브러리 포함
   --add-binary="cudnn64_8.dll;."
```

### 문제 5: 실행 시 즉시 종료

```
❌ 실행 파일이 바로 닫힘

✅ 해결:
1. 콘솔 모드로 빌드 (오류 확인)
   pyinstaller --console main.py

2. 오류 메시지 확인 후 수정

3. 다시 windowed 모드로 빌드
   pyinstaller --windowed main.py
```

---

## 📦 배포 준비

### 1. 테스트

```bash
# 실행 파일 테스트
dist/SafetyPredictionSystem.exe

# 다른 컴퓨터에서 테스트 (Python 미설치 환경)
```

### 2. 배포 패키지 생성

```
Release/
├── SafetyPredictionSystem.exe
├── README_실행파일.txt
├── 사용설명서.pdf (선택)
└── 샘플데이터/ (선택)
```

### 3. 압축 파일 생성

```bash
# Windows
Compress-Archive -Path dist/SafetyPredictionSystem.exe -DestinationPath SafetyPredictionSystem_v1.0.zip

# 또는 7-Zip 사용
7z a SafetyPredictionSystem_v1.0.zip dist/SafetyPredictionSystem.exe
```

---

## 🚀 자동화 스크립트

### Windows 배치 파일 (build.bat)

```batch
@echo off
echo 육군 안전 예측 시스템 빌드 스크립트
echo.

echo [1/3] 의존성 패키지 설치 중...
pip install -r requirements.txt

echo [2/3] PyInstaller 빌드 시작...
python build_exe.py

echo [3/3] 빌드 완료!
echo.
echo 실행 파일: dist\SafetyPredictionSystem.exe
pause
```

### Linux/Mac 쉘 스크립트 (build.sh)

```bash
#!/bin/bash
echo "육군 안전 예측 시스템 빌드 스크립트"
echo

echo "[1/3] 의존성 패키지 설치 중..."
pip install -r requirements.txt

echo "[2/3] PyInstaller 빌드 시작..."
python build_exe.py

echo "[3/3] 빌드 완료!"
echo
echo "실행 파일: dist/SafetyPredictionSystem"
```

---

## 📊 성능 최적화

### 빌드 시간 단축

1. **캐시 활용**: 첫 빌드 후 생성된 `build/` 폴더 유지
2. **부분 빌드**: `--clean` 옵션 제거
3. **병렬 처리**: 가능한 경우 멀티코어 활용

### 파일 크기 최적화

1. **가상환경 사용**: 필수 패키지만 설치
2. **UPX 압축**: `--upx` 옵션 사용
3. **모듈 제외**: 불필요한 라이브러리 제외
4. **디버그 제거**: `--strip` 옵션 사용

### 실행 속도 최적화

1. **최적화 레벨**: `--optimize=2` 사용
2. **사전 컴파일**: `.pyc` 파일 포함
3. **런타임 훅**: 커스텀 초기화 로직

---

**문서 작성일**: 2025-10-07
**빌드 도구**: PyInstaller 5.10+
**대상 환경**: Windows 10/11 (64-bit)

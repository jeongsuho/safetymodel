#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 빌드 스크립트
육군 안전 예측 시스템을 독립 실행 가능한 .exe 파일로 패키징

사용법:
    python build_exe.py
    
생성 파일:
    dist/SafetyPredictionSystem.exe
"""

import os
import sys
import subprocess
from pathlib import Path

def create_spec_file():
    """PyInstaller spec 파일 생성"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('models', 'models'),  # 모델 폴더 포함
        ('data', 'data'),      # 데이터 폴더 포함 (있는 경우)
    ],
    hiddenimports=[
        'pandas',
        'numpy', 
        'openpyxl',
        'sklearn',
        'joblib',
        'torch',
        'tkinter',
        'threading'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy', 
        'IPython',
        'jupyter'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    console=False,  # GUI 모드
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # 아이콘 파일 (옵션)
)
'''
    
    with open('SafetyPrediction.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ PyInstaller spec 파일 생성 완료: SafetyPrediction.spec")

def create_icon():
    """기본 아이콘 생성 (선택사항)"""
    # 실제로는 .ico 파일을 준비하거나 PIL로 생성
    pass

def build_executable():
    """실행 파일 빌드"""
    print("🔨 PyInstaller로 실행 파일 빌드 시작...")
    
    try:
        # spec 파일을 사용하여 빌드
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',           # 이전 빌드 정리
            '--noconfirm',       # 덮어쓰기 확인 없음
            'SafetyPrediction.spec'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 빌드 성공!")
            print(f"📁 실행 파일 위치: {Path('dist/SafetyPredictionSystem.exe').absolute()}")
            
            # 파일 크기 확인
            exe_path = Path('dist/SafetyPredictionSystem.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📊 파일 크기: {size_mb:.1f} MB")
        else:
            print("❌ 빌드 실패!")
            print("오류 출력:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 빌드 중 오류: {e}")
        return False
    
    return True

def create_simple_build():
    """간단한 빌드 (spec 파일 없이)"""
    print("🔨 간단한 빌드 시작...")
    
    try:
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',              # 단일 파일로 패키징
            '--windowed',             # 콘솔 창 숨김
            '--name=SafetyPredictionSystem',
            '--add-data=models;models',  # Windows 경로 구분자
            '--hidden-import=pandas',
            '--hidden-import=numpy',
            '--hidden-import=openpyxl',
            '--hidden-import=sklearn',
            '--clean',
            'main.py'
        ]
        
        # Linux/Mac에서는 경로 구분자를 : 로 변경
        if os.name != 'nt':
            cmd = [arg.replace(';', ':') if 'add-data' in arg else arg for arg in cmd]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 간단 빌드 성공!")
            return True
        else:
            print("❌ 간단 빌드 실패!")
            print("오류:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 빌드 오류: {e}")
        return False

def check_dependencies():
    """의존성 패키지 확인"""
    print("📋 의존성 패키지 확인 중...")
    
    required_packages = ['PyInstaller', 'pandas', 'numpy', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower())
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 미설치")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 다음 패키지를 설치해주세요:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_batch_files():
    """편의용 배치 파일 생성"""
    
    # Windows 배치 파일
    batch_content = '''@echo off
echo 육군 안전 예측 시스템 빌드 스크립트
echo.

echo [1/3] 의존성 패키지 설치 중...
pip install -r requirements.txt

echo [2/3] PyInstaller 빌드 시작...
python build_exe.py

echo [3/3] 빌드 완료!
echo.
echo 실행 파일: dist\\SafetyPredictionSystem.exe
pause
'''
    
    with open('build.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    # Linux/Mac 쉘 스크립트  
    shell_content = '''#!/bin/bash
echo "육군 안전 예측 시스템 빌드 스크립트"
echo

echo "[1/3] 의존성 패키지 설치 중..."
pip install -r requirements.txt

echo "[2/3] PyInstaller 빌드 시작..."
python build_exe.py

echo "[3/3] 빌드 완료!"
echo
echo "실행 파일: dist/SafetyPredictionSystem"
'''
    
    with open('build.sh', 'w', encoding='utf-8') as f:
        f.write(shell_content)
    
    # 실행 권한 부여 (Linux/Mac)
    if os.name != 'nt':
        os.chmod('build.sh', 0o755)
    
    print("✅ 배치 파일 생성 완료: build.bat, build.sh")

def main():
    """메인 빌드 프로세스"""
    print("🛡️ 육군 안전 예측 시스템 - 실행 파일 빌드")
    print("=" * 50)
    
    # 1. 의존성 확인
    if not check_dependencies():
        print("\n❌ 의존성 패키지 부족으로 빌드를 중단합니다.")
        print("다음 명령으로 패키지를 설치하세요:")
        print("pip install -r requirements.txt")
        return
    
    # 2. 빌드 방식 선택
    print("\n빌드 방식을 선택하세요:")
    print("1. 간단 빌드 (권장)")
    print("2. 고급 빌드 (spec 파일 사용)")
    
    choice = input("선택 (1 또는 2, 기본값: 1): ").strip()
    
    if choice == '2':
        # 고급 빌드
        create_spec_file()
        success = build_executable()
    else:
        # 간단 빌드
        success = create_simple_build()
    
    if success:
        print("\n🎉 빌드 완료!")
        print("📁 실행 파일이 dist/ 폴더에 생성되었습니다.")
        print("\n📋 테스트 방법:")
        print("1. dist/SafetyPredictionSystem.exe 실행")
        print("2. 사용자 정보 입력 후 '안전 예측 실행' 클릭")
        print("3. 결과 확인 후 '엑셀로 저장' 테스트")
        
        # 배치 파일도 생성
        create_batch_files()
    else:
        print("\n❌ 빌드 실패!")
        print("requirements.txt의 패키지들이 모두 설치되었는지 확인하세요.")

if __name__ == "__main__":
    main()
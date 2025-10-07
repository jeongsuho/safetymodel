"""
육군 종합정비창 안전 예측 시스템 - 메인 프로그램
ML/DL 모델 통합 실행 엔트리 포인트
"""

import os
import sys
from pathlib import Path

def print_banner():
    """프로그램 배너 출력"""
    print("=" * 60)
    print("🛡️  육군 종합정비창 안전 예측 시스템")
    print("=" * 60)
    print("📊 ML 모델: 시간대별 안전 예측 (3,672시간)")
    print("🤖 DL 모델: 실시간 위험 키워드 생성 및 안전대책 추천")
    print("=" * 60)
    print()

def check_environment():
    """실행 환경 확인"""
    print("🔍 실행 환경 확인 중...")

    # Python 버전 확인
    python_version = sys.version.split()[0]
    print(f"   Python 버전: {python_version}")

    # 필수 라이브러리 확인
    required_packages = {
        'torch': 'PyTorch',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'sklearn': 'Scikit-learn',
        'openpyxl': 'OpenPyXL'
    }

    missing_packages = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - 설치 필요")
            missing_packages.append(name)

    if missing_packages:
        print(f"\n⚠️  누락된 패키지: {', '.join(missing_packages)}")
        print("💡 설치 방법: pip install -r requirements.txt")
        return False

    # GPU 확인 (선택 사항)
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"   🚀 GPU 사용 가능: {gpu_name}")
        else:
            print("   💻 CPU 모드로 실행됩니다")
    except:
        pass

    print()
    return True

def get_base_paths():
    """ML/DL 폴더 경로 설정"""
    desktop = Path.home() / "OneDrive" / "Desktop"

    # OneDrive가 없는 경우 일반 Desktop
    if not desktop.exists():
        desktop = Path.home() / "Desktop"

    ml_path = desktop / "ML"
    dl_path = desktop / "DL"

    return ml_path, dl_path

def run_ml_system():
    """ML 시스템 실행"""
    print("=" * 60)
    print("📊 ML 시스템: 시간대별 안전 예측")
    print("=" * 60)

    ml_path, _ = get_base_paths()

    if not ml_path.exists():
        print(f"❌ ML 폴더를 찾을 수 없습니다: {ml_path}")
        print("💡 ML 폴더가 Desktop에 있는지 확인해주세요.")
        return False

    print(f"📁 ML 폴더: {ml_path}")
    print("\n실행 가능한 기능:")
    print("1. GPU 최적화 시간대별 예측 시스템")
    print("2. 모델 성능 평가 시스템")
    print()
    print("💡 직접 실행 방법:")
    print(f"   cd {ml_path}")
    print("   python GPU_최적화_시간대별_예측시스템.py")
    print()

    return True

def run_dl_system():
    """DL 시스템 실행"""
    print("=" * 60)
    print("🤖 DL 시스템: 실시간 안전 예측")
    print("=" * 60)

    _, dl_path = get_base_paths()

    if not dl_path.exists():
        print(f"❌ DL 폴더를 찾을 수 없습니다: {dl_path}")
        print("💡 DL 폴더가 Desktop에 있는지 확인해주세요.")
        return False

    print(f"📁 DL 폴더: {dl_path}")
    print("\n실행 가능한 기능:")
    print("1. 통합 안전 예측 시스템")
    print("2. 실시간 위험 키워드 생성")
    print("3. AI 안전대책 추천")
    print()
    print("💡 직접 실행 방법:")
    print(f"   cd {dl_path}")
    print("   venv\\Scripts\\activate")
    print("   python integrated_safety_system.py")
    print()

    return True

def show_menu():
    """메인 메뉴 표시"""
    print("\n📋 메뉴를 선택하세요:")
    print("1. ML 시스템 안내")
    print("2. DL 시스템 안내")
    print("3. 프로젝트 정보")
    print("4. 종료")
    print()

    choice = input("선택 (1-4): ").strip()
    return choice

def show_project_info():
    """프로젝트 정보 표시"""
    print("=" * 60)
    print("📖 프로젝트 정보")
    print("=" * 60)
    print()
    print("🎯 프로젝트 목표:")
    print("   - ML/DL 모델을 Windows GUI 프로그램으로 변환")
    print("   - 독립 실행 가능한 .exe 파일 생성")
    print()
    print("📊 ML 시스템:")
    print("   - 시간대별 위험지수 예측 (3,672시간)")
    print("   - 안전 임무 순위 추천")
    print("   - 안전 멘토 추천")
    print("   - GPU 최적화 배치 처리")
    print()
    print("🤖 DL 시스템:")
    print("   - 실시간 위험 키워드 10개 생성")
    print("   - 자연어 기반 위험요인 추측")
    print("   - AI 안전대책 추천")
    print("   - PyTorch Seq2Seq 모델")
    print()
    print("📚 문서:")
    print("   - README.md: 프로젝트 개요")
    print("   - PROJECT_GUIDE.md: 상세 개발 가이드")
    print()
    print("🌐 GitHub:")
    print("   https://github.com/jeongsuho/safetymodel")
    print()

def main():
    """메인 함수"""
    print_banner()

    # 환경 확인
    if not check_environment():
        print("\n⚠️  환경 설정이 필요합니다.")
        print("💡 requirements.txt 파일로 필수 패키지를 설치해주세요:")
        print("   pip install -r requirements.txt")
        return

    # 메인 루프
    while True:
        choice = show_menu()

        if choice == '1':
            run_ml_system()
        elif choice == '2':
            run_dl_system()
        elif choice == '3':
            show_project_info()
        elif choice == '4':
            print("\n👋 프로그램을 종료합니다.")
            break
        else:
            print("\n❌ 잘못된 선택입니다. 1-4 사이의 숫자를 입력해주세요.")

        input("\n계속하려면 Enter를 누르세요...")
        print("\n" * 2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("💡 문제가 지속되면 GitHub Issues에 리포트해주세요.")

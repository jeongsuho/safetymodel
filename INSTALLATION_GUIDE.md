# 🛡️ 육군 안전 예측 시스템 설치 및 실행 가이드

## 📋 개요

이 가이드는 **Windows 환경**에서 육군 안전 예측 시스템 프로토타입을 설치하고 실행하는 방법을 설명합니다.

**⚠️ 중요**: 현재는 프로토타입이므로 더미 데이터를 사용합니다. 실제 ML/DL 모델은 추후 통합 예정입니다.

---

## 🎯 1단계: 환경 준비

### Windows 10/11 시스템 요구사항
- **운영체제**: Windows 10 이상 (64bit)
- **Python**: 3.8 이상 (3.12 권장)
- **메모리**: 최소 4GB RAM (8GB 권장)
- **저장공간**: 최소 1GB 여유공간
- **GPU**: 선택사항 (CUDA 11.8+ 지원 시 고성능)

### Python 설치 확인
```cmd
# 명령 프롬프트에서 실행
python --version
# 또는
python3 --version

# 결과 예시: Python 3.12.0
```

**Python이 없다면**: [python.org](https://www.python.org/downloads/)에서 최신 버전 다운로드

---

## 🚀 2단계: 프로젝트 다운로드

### GitHub에서 다운로드
1. GitHub 저장소에서 **Code > Download ZIP** 클릭
2. 다운로드한 파일을 `C:\Safety_Prediction\` 폴더에 압축 해제
3. 또는 Git을 사용하는 경우:

```cmd
cd C:\
git clone <GitHub_저장소_URL> Safety_Prediction
cd Safety_Prediction
```

### 폴더 구조 확인
```
C:\Safety_Prediction\
├── main.py                    # 메인 프로그램
├── build_exe.py              # 빌드 스크립트  
├── requirements.txt          # 패키지 목록
├── models\                   # 모델 폴더
│   ├── dummy_model.py
│   └── *.pkl (자동 생성)
└── README_PROTOTYPE.md       # 상세 문서
```

---

## 📦 3단계: 패키지 설치

### 가상환경 생성 (권장)
```cmd
cd C:\Safety_Prediction
python -m venv safety_env
safety_env\Scripts\activate
```

### 필수 패키지 설치
```cmd
pip install -r requirements.txt
```

**설치되는 주요 패키지**:
- `pandas`, `numpy` - 데이터 처리
- `openpyxl` - 엑셀 파일 생성
- `tkinter` - GUI (Python 기본 포함)
- `scikit-learn` - 머신러닝 (실제 모델용)
- `pyinstaller` - .exe 생성용

---

## 🎮 4단계: 프로그램 실행

### Python으로 직접 실행
```cmd
cd C:\Safety_Prediction
python main.py
```

### 실행 성공 확인
프로그램이 정상 실행되면 다음과 같은 GUI 창이 나타납니다:

```
┌─────────────────────────────────────────────────────────┐
│ 🛡️ 육군 종합정비창 안전 예측 시스템 v1.0                │
├─────────────────┬─────────────────────────────────────┤
│ 📝 사용자 정보   │ 📊 예측 결과                        │
│ ┌─────────────┐ │                                     │
│ │이름: 정수호  │ │ (예측 실행 후 결과 표시)             │
│ │성별: 남성   │ │                                     │  
│ │나이: 30     │ │                                     │
│ └─────────────┘ │                                     │
└─────────────────┴─────────────────────────────────────┘
│ 🔮 안전 예측 실행 | 💾 엑셀로 저장 | ⚙️ 설정 | ❓ 도움말 │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 5단계: .exe 파일 생성 (선택사항)

### 자동 빌드 스크립트 사용
```cmd
cd C:\Safety_Prediction
python build_exe.py
```

### 배치 파일 사용
```cmd
build.bat
```

### 빌드 완료 후
- 실행 파일: `dist\SafetyPredictionSystem.exe`
- 크기: 약 50-100MB
- **Python 설치 없이도 실행 가능!**

---

## 🧪 6단계: 프로그램 테스트

### 기본 테스트 시나리오

1. **사용자 정보 입력**
   - 이름: `정수호`
   - 성별: `남성` 
   - 나이: `30`
   - 근속연수: `5`
   - 임무: `복합적층장갑`

2. **예측 실행**
   - `🔮 안전 예측 실행` 버튼 클릭
   - 2-3초 후 결과 표시 확인

3. **결과 확인**
   - 위험지수: 6.0~8.0 범위의 값
   - 위험 키워드: 10개 목록
   - 안전대책: 맞춤형 추천사항

4. **엑셀 저장 테스트**
   - `💾 엑셀로 저장` 버튼 클릭
   - 4개 시트로 구성된 엑셀 파일 생성 확인

---

## ❗ 문제 해결

### 자주 발생하는 오류

#### 1. "ModuleNotFoundError: No module named 'pandas'"
```cmd
# 해결책: 패키지 재설치
pip install pandas numpy openpyxl
```

#### 2. "tkinter 오류" (GUI 실행 실패)
```cmd
# 해결책: Python 재설치 시 tcl/tk 옵션 포함
# 또는 Python 공식 배포판 사용
```

#### 3. ".exe 생성 실패"
```cmd
# 해결책: PyInstaller 재설치
pip uninstall pyinstaller
pip install pyinstaller

# 수동 빌드 시도
pyinstaller --onefile --windowed main.py
```

#### 4. "Permission denied" (권한 오류)
```cmd
# 해결책: 관리자 권한으로 명령 프롬프트 실행
# 우클릭 > "관리자 권한으로 실행"
```

### 성능 최적화

#### GPU 가속 설정
```cmd
# CUDA 설치 후 PyTorch GPU 버전
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 메모리 사용량 줄이기
```cmd
# 불필요한 패키지 제외하고 빌드
pyinstaller --exclude-module matplotlib --exclude-module scipy main.py
```

---

## 🔄 실제 모델 통합 준비

### 현재 프로토타입에서 실제 모델로 업그레이드하려면:

1. **models/ 폴더에 실제 파일 배치**
   ```
   models/
   ├── enhanced_safety_model.pkl      # ML 모델
   ├── enhanced_encoders.pkl          # 인코더
   ├── enhanced_scaler.pkl           # 스케일러
   ├── neural_safety_model.pth       # DL 모델
   └── neural_vocab.pkl              # 어휘 사전
   ```

2. **main.py의 더미 구현 부분을 실제 코드로 교체**
   - `load_models()` 함수
   - `perform_prediction()` 함수

3. **의존성 패키지 추가 설치**
   ```cmd
   pip install torch scikit-learn joblib
   ```

---

## 📞 지원 및 문의

### 개발 관련 문의
- **GitHub Issues**: 버그 리포트 및 기능 요청
- **Pull Requests**: 코드 개선사항 제안

### 프로토타입 피드백
다음 사항들에 대한 피드백을 환영합니다:

1. **사용성**: GUI 인터페이스의 편의성
2. **성능**: 프로그램 실행 속도 및 안정성  
3. **기능**: 필요한 추가 기능이나 개선사항
4. **배포**: .exe 생성 및 배포 관련 이슈

---

## 📅 업데이트 로드맵

### 다음 버전 (v1.1) 예정 기능
- ✅ 실제 ML/DL 모델 통합
- ✅ GPU 가속 완전 지원  
- ✅ 성능 최적화
- ✅ UI/UX 개선

### 장기 계획 (v2.0)
- 🌐 웹 버전 개발
- 📱 모바일 앱 지원
- ☁️ 클라우드 배포
- 📊 대시보드 시스템

---

**문서 작성**: 2025-10-07  
**프로토타입 버전**: v1.0  
**테스트 환경**: Windows 10/11, Python 3.8+
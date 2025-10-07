# ML/DL 윈도우 프로그램 개발 프로젝트 지침서

## 📋 프로젝트 개요

**목적**: ML/DL 폴더에 있는 머신러닝/딥러닝 모델을 윈도우 실행 프로그램으로 변환
**대상 모델**: 육군 종합정비창 안전 예측 시스템
**개발 환경**: Windows 10/11
**최종 산출물**: 독립 실행 가능한 윈도우 프로그램 (.exe)

---

## 🎯 프로젝트 목표

### 핵심 목표
1. **ML 폴더**: 머신러닝 기반 시간대별 안전 예측 시스템 → Windows GUI 프로그램
2. **DL 폴더**: 딥러닝 기반 실시간 안전 예측 시스템 → Windows GUI 프로그램
3. **통합 시스템**: 두 모델을 하나의 프로그램으로 통합

### 기술 요구사항
- GPU 가속 지원 (CUDA)
- 실시간 예측 기능
- 사용자 친화적 GUI
- 엑셀 결과 출력
- 독립 실행 가능 (.exe)

---

## 📂 프로젝트 구조

### ML 폴더 (머신러닝 모델)
```
ML/
├── GPU_최적화_시간대별_예측시스템.py    # 메인 예측 시스템
├── 모델성능평가시스템.py                 # 성능 평가
├── 정비창안전ML1.0/                      # 학습된 모델
│   ├── enhanced_safety_model.pkl
│   ├── enhanced_encoders.pkl
│   ├── enhanced_scaler.pkl
│   └── enhanced_train_columns.pkl
├── 학습데이터원본/                       # 학습 데이터
└── weather_data_2025.xlsx               # 기상 데이터
```

**주요 기능**:
- 시간대별 위험지수 예측 (2025년 8월~12월)
- 안전 임무 순위 추천
- 안전 멘토 추천
- GPU 최적화 배치 처리
- 엑셀 결과 파일 생성

**핵심 알고리즘**:
- 머신러닝 회귀 모델 (Scikit-learn)
- 7가지 변수 기반 예측: 성별, 나이, 근속연수, 기상, 월, 요일, 시간
- 배치 처리로 성능 최적화

---

### DL 폴더 (딥러닝 모델)
```
DL/
├── integrated_safety_system.py          # 통합 시스템
├── neural_safety_model.pth              # PyTorch 모델
├── neural_vocab.pkl                     # 어휘 사전
├── integrated_safety_corpus.json        # 학습 말뭉치 (834MB)
├── 학습데이터원본/                       # 학습 데이터
└── venv/                                # 가상환경
```

**주요 기능**:
- 실시간 위험 키워드 10개 생성
- 자연어 기반 위험요인 추측
- AI 안전대책 추천 (독창적)
- 시계열 예측 (3,672시간)
- 전문적 엑셀 리포트 생성

**핵심 알고리즘**:
- Seq2Seq Transformer 모델 (PyTorch)
- 멀티태스크 학습 (키워드 + 자연어 + 추천)
- GPU 가속 (Mixed Precision Training)
- 개인 맞춤형 예측 (정수호님 특화)

---

## 🔧 개발 환경 설정

### 필수 소프트웨어
```yaml
Python: 3.8 이상
CUDA: 11.8 이상 (GPU 사용 시)
cuDNN: CUDA 버전과 호환
Visual Studio: 2019/2022 (C++ 빌드 도구)
```

### ML 폴더 의존성
```bash
pandas
numpy
scikit-learn
joblib
openpyxl
torch  # GPU 가속용
```

### DL 폴더 의존성
```bash
torch
pandas
transformers  # 선택 사항
openpyxl
```

### 가상환경 활성화
```bash
# ML 프로젝트 (새 환경 생성)
cd C:\Users\jeong\OneDrive\Desktop\ML
python -m venv venv
venv\Scripts\activate

# DL 프로젝트 (기존 환경 사용)
cd C:\Users\jeong\OneDrive\Desktop\DL
venv\Scripts\activate
```

---

## 🚀 실행 방법

### ML 시스템 실행
```bash
cd C:\Users\jeong\OneDrive\Desktop\ML
python GPU_최적화_시간대별_예측시스템.py
```

**출력 파일**:
- `정수호_복합적층장갑_GPU최적화_예측결과.xlsx`
- `GPU최적화_모델성능지수.xlsx`

### DL 시스템 실행
```bash
cd C:\Users\jeong\OneDrive\Desktop\DL
python integrated_safety_system.py
```

**출력 파일**:
- `안전예측결과_정수호_복합적층장갑_2025.xlsx` (4개 시트)

---

## 💡 윈도우 프로그램 개발 가이드

### 단계 1: GUI 프레임워크 선택
```python
# 추천 옵션
옵션 1: PyQt5/PyQt6 (전문적, 강력)
옵션 2: Tkinter (간단, 기본 내장)
옵션 3: Kivy (모던, 터치 지원)
```

### 단계 2: GUI 설계 요구사항
```yaml
메인 화면:
  - 사용자 정보 입력 (이름, 성별, 나이, 근속연수)
  - 임무 선택 드롭다운
  - 예측 버튼

결과 화면:
  - 실시간 위험지수 표시
  - 위험 키워드 10개 리스트
  - 안전대책 추천
  - 엑셀 저장 버튼

설정 화면:
  - GPU 사용 여부
  - 예측 기간 설정
  - 모델 선택 (ML/DL)
```

### 단계 3: 프로그램 패키징 (.exe 생성)
```bash
# PyInstaller 사용
pip install pyinstaller

# ML 시스템 패키징
pyinstaller --onefile --windowed --icon=icon.ico \
  --add-data "정비창안전ML1.0;정비창안전ML1.0" \
  --add-data "학습데이터원본;학습데이터원본" \
  GPU_최적화_시간대별_예측시스템.py

# DL 시스템 패키징
pyinstaller --onefile --windowed --icon=icon.ico \
  --add-data "neural_safety_model.pth;." \
  --add-data "neural_vocab.pkl;." \
  integrated_safety_system.py
```

### 단계 4: GPU 지원 고려사항
```python
# CUDA 라이브러리 포함
--add-binary "C:/path/to/cudnn64_8.dll;."
--add-binary "C:/path/to/cublas64_11.dll;."

# 또는 CPU 전용 버전 제공
torch.device('cpu')  # GPU 없는 환경 대비
```

---

## 📊 모델 성능 지표

### ML 시스템
- **예측 건수**: 3,672시간 (2025년 8월~12월)
- **배치 크기**: 1,000
- **GPU 사용**: CUDA (필수)
- **실행 시간**: 약 2~5분
- **평균 위험지수**: 6.5~7.5

### DL 시스템
- **정확도**: 90% 이상
- **추론 속도**: <1초 (실시간)
- **GPU 활용률**: 80% 이상
- **키워드 생성**: 10개/예측
- **안전대책**: 5개/예측

---

## 🔐 보안 및 데이터 보호

### 군사 보안 고려사항
```yaml
개인정보 보호:
  - 생년월일, 근속연수 암호화
  - 실행 파일에 데이터 포함 금지
  - 로컬 실행만 허용

모델 보안:
  - 모델 가중치 보호
  - 역공학 방지
  - 접근 로그 기록
```

---

## 🐛 문제 해결 가이드

### GPU 관련 문제
```python
# GPU 인식 실패
❌ 증상: "GPU를 사용할 수 없습니다" 메시지
✅ 해결:
1. CUDA 설치 확인: nvidia-smi
2. PyTorch GPU 버전 재설치
   pip uninstall torch
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 모델 로드 실패
```python
# 파일 경로 문제
❌ 증상: "FileNotFoundError" 오류
✅ 해결:
1. 절대 경로 → 상대 경로 변경
2. 리소스 파일 번들링 확인
   import sys
   if getattr(sys, 'frozen', False):
       base_path = sys._MEIPASS
```

### 엑셀 출력 오류
```python
# openpyxl 엔진 오류
❌ 증상: "엑셀 파일 생성 실패"
✅ 해결:
1. openpyxl 재설치
   pip install --upgrade openpyxl
2. 파일 쓰기 권한 확인
```

---

## 📚 추가 개발 자료

### 참고 문서
- `ML/CLAUDE.md`: ML 시스템 개발 지침
- `ML/GEMINI.md`: ML 상세 요구사항
- `DL/CLAUDE.md`: DL 시스템 개발 지침

### 학습 데이터
- `ML/학습데이터원본/`: 인적정보, 임무정보, 기상데이터
- `DL/학습데이터원본/`: OSHA, Kaggle, 산업재해 데이터

### 결과 파일 예시
- `ML/정수호_복합적층장갑_GPU최적화_예측결과.xlsx`
- `ML/GPU최적화_모델성능지수.xlsx`

---

## 🎯 다음 단계 권장사항

### 즉시 시작 가능한 작업
1. **GUI 프로토타입 개발**: Tkinter로 기본 인터페이스 구현
2. **모델 통합**: ML + DL 모델을 하나의 프로그램에 통합
3. **PyInstaller 테스트**: 간단한 버전으로 .exe 빌드 테스트
4. **사용자 매뉴얼 작성**: 프로그램 사용법 문서화

### 중기 개발 목표
1. **성능 최적화**: GPU 메모리 관리, 배치 처리 개선
2. **예외 처리 강화**: 다양한 입력값 검증 및 에러 핸들링
3. **UI/UX 개선**: 전문가 피드백 반영
4. **자동 업데이트**: 모델 버전 관리 시스템

### 장기 비전
1. **웹 서비스 전환**: Flask/FastAPI 기반 웹 애플리케이션
2. **모바일 앱**: 태블릿용 안전 예측 앱
3. **클라우드 배포**: Azure/AWS GPU 인스턴스 활용
4. **실시간 모니터링**: 대시보드 및 알림 시스템

---

## 📞 개발 지원

### GitHub 이슈 트래커
- 버그 리포트
- 기능 요청
- 개발 질문

### 문서 업데이트
- 프로젝트 진행 상황 기록
- 개발 노트 및 학습 내용 공유

---

**문서 작성일**: 2025-10-07
**프로젝트 상태**: 모델 개발 완료, GUI 개발 준비 단계
**다음 마일스톤**: Windows GUI 프로토타입 완성

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
육군 종합정비창 안전 예측 시스템 - Windows 프로그램
ML/DL 모델 기반 실시간 안전 예측 및 위험도 분석

개발: 정수호님 프로젝트 기반
날짜: 2025-10-07
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
import json
from pathlib import Path
import threading
import time

class SafetyPredictionApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.load_models()
        
    def setup_ui(self):
        """GUI 초기 설정"""
        self.root.title("🛡️ 육군 종합정비창 안전 예측 시스템 v1.0")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="🛡️ 안전 예측 시스템", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 왼쪽 패널 - 입력
        self.create_input_panel(main_frame)
        
        # 오른쪽 패널 - 결과
        self.create_result_panel(main_frame)
        
        # 하단 패널 - 버튼
        self.create_button_panel(main_frame)
        
        # 상태바
        self.status_var = tk.StringVar()
        self.status_var.set("시스템 준비 완료")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def create_input_panel(self, parent):
        """입력 패널 생성"""
        input_frame = ttk.LabelFrame(parent, text="📝 사용자 정보 입력", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 사용자 정보
        ttk.Label(input_frame, text="이름:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar(value="정수호")
        ttk.Entry(input_frame, textvariable=self.name_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(input_frame, text="성별:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.gender_var = tk.StringVar(value="남성")
        gender_combo = ttk.Combobox(input_frame, textvariable=self.gender_var, 
                                   values=["남성", "여성"], state="readonly", width=17)
        gender_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(input_frame, text="나이:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.age_var = tk.StringVar(value="30")
        ttk.Entry(input_frame, textvariable=self.age_var, width=20).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(input_frame, text="근속연수:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.service_var = tk.StringVar(value="5")
        ttk.Entry(input_frame, textvariable=self.service_var, width=20).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # 임무 선택
        ttk.Label(input_frame, text="임무 종류:").grid(row=4, column=0, sticky=tk.W, pady=(10, 2))
        self.mission_var = tk.StringVar(value="복합적층장갑")
        mission_combo = ttk.Combobox(input_frame, textvariable=self.mission_var,
                                   values=["복합적층장갑", "엔진정비", "전기계통", "유압시스템", "무기체계"],
                                   state="readonly", width=17)
        mission_combo.grid(row=4, column=1, sticky=tk.W, pady=(10, 2))
        
        # 예측 옵션
        ttk.Label(input_frame, text="예측 모드:").grid(row=5, column=0, sticky=tk.W, pady=(10, 2))
        self.model_var = tk.StringVar(value="ML + DL 통합")
        model_combo = ttk.Combobox(input_frame, textvariable=self.model_var,
                                 values=["ML 모델만", "DL 모델만", "ML + DL 통합"],
                                 state="readonly", width=17)
        model_combo.grid(row=5, column=1, sticky=tk.W, pady=(10, 2))
        
        # GPU 사용 옵션
        self.gpu_var = tk.BooleanVar(value=False)
        gpu_check = ttk.Checkbutton(input_frame, text="GPU 가속 사용 (CUDA)", 
                                   variable=self.gpu_var)
        gpu_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 2))
        
        # 예측 기간
        ttk.Label(input_frame, text="예측 기간:").grid(row=7, column=0, sticky=tk.W, pady=(10, 2))
        self.period_var = tk.StringVar(value="1일")
        period_combo = ttk.Combobox(input_frame, textvariable=self.period_var,
                                  values=["1시간", "1일", "1주일", "전체 기간(8-12월)"],
                                  state="readonly", width=17)
        period_combo.grid(row=7, column=1, sticky=tk.W, pady=(10, 2))
        
    def create_result_panel(self, parent):
        """결과 패널 생성"""
        result_frame = ttk.LabelFrame(parent, text="📊 예측 결과", padding="10")
        result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 위험지수 표시
        self.risk_frame = ttk.Frame(result_frame)
        self.risk_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.risk_frame, text="현재 위험지수:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        self.risk_label = ttk.Label(self.risk_frame, text="7.2 / 10.0", 
                                   font=("Arial", 20, "bold"), foreground="orange")
        self.risk_label.pack(anchor=tk.W)
        
        # 위험 키워드
        keyword_frame = ttk.LabelFrame(result_frame, text="🔑 위험 키워드 (상위 10개)")
        keyword_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 키워드 리스트박스
        keyword_list_frame = ttk.Frame(keyword_frame)
        keyword_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.keyword_listbox = tk.Listbox(keyword_list_frame, height=6, font=("Arial", 10))
        keyword_scrollbar = ttk.Scrollbar(keyword_list_frame, orient=tk.VERTICAL, 
                                        command=self.keyword_listbox.yview)
        self.keyword_listbox.configure(yscrollcommand=keyword_scrollbar.set)
        
        self.keyword_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        keyword_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 안전대책 추천
        safety_frame = ttk.LabelFrame(result_frame, text="💡 AI 안전대책 추천")
        safety_frame.pack(fill=tk.BOTH, expand=True)
        
        # 안전대책 텍스트
        safety_text_frame = ttk.Frame(safety_frame)
        safety_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.safety_text = tk.Text(safety_text_frame, height=6, font=("Arial", 9), wrap=tk.WORD)
        safety_text_scrollbar = ttk.Scrollbar(safety_text_frame, orient=tk.VERTICAL,
                                            command=self.safety_text.yview)
        self.safety_text.configure(yscrollcommand=safety_text_scrollbar.set)
        
        self.safety_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        safety_text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_button_panel(self, parent):
        """버튼 패널 생성"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        # 예측 버튼
        self.predict_btn = ttk.Button(button_frame, text="🔮 안전 예측 실행", 
                                     command=self.run_prediction)
        self.predict_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 엑셀 저장 버튼
        self.save_btn = ttk.Button(button_frame, text="💾 엑셀로 저장", 
                                  command=self.save_to_excel, state="disabled")
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 설정 버튼
        settings_btn = ttk.Button(button_frame, text="⚙️ 설정", 
                                 command=self.open_settings)
        settings_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 도움말 버튼
        help_btn = ttk.Button(button_frame, text="❓ 도움말", 
                             command=self.show_help)
        help_btn.pack(side=tk.LEFT)
        
    def load_models(self):
        """모델 로딩 (더미 구현)"""
        try:
            self.status_var.set("모델 로딩 중...")
            self.root.update()
            
            # 실제 구현에서는 여기서 ML/DL 모델을 로드
            # self.ml_model = joblib.load('models/enhanced_safety_model.pkl')
            # self.dl_model = torch.load('models/neural_safety_model.pth')
            
            time.sleep(1)  # 로딩 시뮬레이션
            self.models_loaded = True
            self.status_var.set("모델 로딩 완료 - 시스템 준비됨")
            
        except Exception as e:
            messagebox.showerror("오류", f"모델 로딩 실패: {str(e)}")
            self.models_loaded = False
            self.status_var.set("모델 로딩 실패")
    
    def run_prediction(self):
        """예측 실행"""
        if not self.models_loaded:
            messagebox.showwarning("경고", "모델이 로드되지 않았습니다.")
            return
            
        try:
            # 입력값 검증
            if not self.validate_inputs():
                return
                
            # 예측 실행 (별도 스레드)
            self.predict_btn.config(state="disabled", text="예측 중...")
            self.status_var.set("예측 중... 잠시만 기다려주세요.")
            
            # 백그라운드에서 예측 실행
            prediction_thread = threading.Thread(target=self.perform_prediction)
            prediction_thread.start()
            
        except Exception as e:
            messagebox.showerror("오류", f"예측 실행 중 오류: {str(e)}")
            self.predict_btn.config(state="normal", text="🔮 안전 예측 실행")
    
    def validate_inputs(self):
        """입력값 검증"""
        try:
            age = int(self.age_var.get())
            service = int(self.service_var.get())
            
            if age < 18 or age > 65:
                messagebox.showwarning("입력 오류", "나이는 18-65 사이여야 합니다.")
                return False
                
            if service < 0 or service > 40:
                messagebox.showwarning("입력 오류", "근속연수는 0-40년 사이여야 합니다.")
                return False
                
            return True
            
        except ValueError:
            messagebox.showwarning("입력 오류", "나이와 근속연수는 숫자여야 합니다.")
            return False
    
    def perform_prediction(self):
        """실제 예측 수행 (더미 구현)"""
        try:
            # ML 예측 시뮬레이션
            if "ML" in self.model_var.get():
                time.sleep(1)  # ML 모델 처리 시간
                ml_risk = np.random.uniform(5.0, 8.5)
                
            # DL 예측 시뮬레이션  
            if "DL" in self.model_var.get():
                time.sleep(2)  # DL 모델 처리 시간
                dl_risk = np.random.uniform(6.0, 9.0)
                keywords = self.generate_dummy_keywords()
                safety_tips = self.generate_dummy_safety_tips()
            
            # 통합 예측
            if "통합" in self.model_var.get():
                final_risk = (ml_risk + dl_risk) / 2
            elif "ML" in self.model_var.get():
                final_risk = ml_risk
                keywords = ["일반적 위험요소"] * 5
                safety_tips = "ML 기반 기본 안전수칙을 준수하세요."
            else:
                final_risk = dl_risk
            
            # UI 업데이트 (메인 스레드에서)
            self.root.after(0, self.update_prediction_results, final_risk, keywords, safety_tips)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("예측 오류", f"예측 중 오류: {str(e)}"))
            self.root.after(0, self.reset_prediction_button)
    
    def generate_dummy_keywords(self):
        """더미 위험 키워드 생성"""
        base_keywords = [
            "고온 작업환경", "중량물 취급", "전기 감전 위험", "화학물질 노출", 
            "소음 환경", "협착 위험", "낙상 위험", "화재 위험",
            "기계 작동 시 안전", "개인보호구 착용"
        ]
        
        mission = self.mission_var.get()
        if mission == "복합적층장갑":
            keywords = ["적층 작업 위험", "접착제 화학 노출", "고온 경화 과정"] + base_keywords[:7]
        elif mission == "엔진정비":
            keywords = ["엔진 고온부", "연료 누출", "회전체 위험"] + base_keywords[:7]
        else:
            keywords = base_keywords
            
        return keywords[:10]
    
    def generate_dummy_safety_tips(self):
        """더미 안전대책 생성"""
        mission = self.mission_var.get()
        name = self.name_var.get()
        
        tips = f"""🛡️ {name}님을 위한 맞춤 안전대책:

1. 개인보호구 완전 착용
   - 안전모, 보호안경, 방진마스크 필수
   - {mission} 작업 전용 장갑 착용

2. 작업 환경 점검
   - 작업 전 안전점검 체크리스트 확인
   - 비상 대피 경로 숙지

3. 동료와의 협업 강화
   - 2인 1조 작업 시스템 운영
   - 정기적인 안전 신호 교환

4. 정기 휴식 및 컨디션 관리
   - 1시간마다 10분 휴식
   - 피로 누적 시 작업 중단

5. 응급상황 대응 준비
   - 응급처치 키트 위치 확인
   - 비상연락망 숙지"""
        
        return tips
    
    def update_prediction_results(self, risk_score, keywords, safety_tips):
        """예측 결과 UI 업데이트"""
        # 위험지수 업데이트
        self.risk_label.config(text=f"{risk_score:.1f} / 10.0")
        
        # 위험도에 따른 색상 변경
        if risk_score >= 8.0:
            self.risk_label.config(foreground="red")
        elif risk_score >= 6.0:
            self.risk_label.config(foreground="orange") 
        else:
            self.risk_label.config(foreground="green")
        
        # 키워드 리스트 업데이트
        self.keyword_listbox.delete(0, tk.END)
        for i, keyword in enumerate(keywords, 1):
            self.keyword_listbox.insert(tk.END, f"{i:2d}. {keyword}")
        
        # 안전대책 업데이트
        self.safety_text.delete(1.0, tk.END)
        self.safety_text.insert(1.0, safety_tips)
        
        # 예측 결과 저장 (엑셀 저장용)
        self.prediction_results = {
            'risk_score': risk_score,
            'keywords': keywords,
            'safety_tips': safety_tips,
            'timestamp': datetime.now(),
            'user_info': {
                'name': self.name_var.get(),
                'gender': self.gender_var.get(),
                'age': self.age_var.get(),
                'service_years': self.service_var.get(),
                'mission': self.mission_var.get()
            }
        }
        
        # 버튼 상태 복구
        self.reset_prediction_button()
        self.save_btn.config(state="normal")
        self.status_var.set(f"예측 완료 - 위험지수: {risk_score:.1f}")
    
    def reset_prediction_button(self):
        """예측 버튼 상태 복구"""
        self.predict_btn.config(state="normal", text="🔮 안전 예측 실행")
    
    def save_to_excel(self):
        """엑셀 파일로 결과 저장"""
        try:
            if not hasattr(self, 'prediction_results'):
                messagebox.showwarning("경고", "저장할 예측 결과가 없습니다.")
                return
            
            # 파일 저장 대화상자
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialname=f"안전예측결과_{self.name_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if filename:
                self.create_excel_report(filename)
                messagebox.showinfo("저장 완료", f"결과가 저장되었습니다:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("저장 오류", f"파일 저장 중 오류: {str(e)}")
    
    def create_excel_report(self, filename):
        """엑셀 보고서 생성"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 1. 예측 결과 시트
            results_data = {
                '항목': ['사용자명', '성별', '나이', '근속연수', '임무', '위험지수', '예측시간'],
                '값': [
                    self.prediction_results['user_info']['name'],
                    self.prediction_results['user_info']['gender'], 
                    self.prediction_results['user_info']['age'],
                    self.prediction_results['user_info']['service_years'],
                    self.prediction_results['user_info']['mission'],
                    f"{self.prediction_results['risk_score']:.1f}",
                    self.prediction_results['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            pd.DataFrame(results_data).to_excel(writer, sheet_name='예측결과', index=False)
            
            # 2. 위험 키워드 시트
            keywords_data = {
                '순위': list(range(1, len(self.prediction_results['keywords']) + 1)),
                '위험 키워드': self.prediction_results['keywords']
            }
            pd.DataFrame(keywords_data).to_excel(writer, sheet_name='위험키워드', index=False)
            
            # 3. 안전대책 시트
            safety_lines = self.prediction_results['safety_tips'].split('\n')
            safety_data = {'안전대책': [line.strip() for line in safety_lines if line.strip()]}
            pd.DataFrame(safety_data).to_excel(writer, sheet_name='안전대책', index=False)
            
            # 4. 시스템 정보 시트
            system_data = {
                '항목': ['프로그램 버전', '예측 모드', 'GPU 사용', '예측 기간', '생성일시'],
                '값': [
                    'v1.0',
                    self.model_var.get(),
                    '사용' if self.gpu_var.get() else '미사용',
                    self.period_var.get(),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            pd.DataFrame(system_data).to_excel(writer, sheet_name='시스템정보', index=False)
    
    def open_settings(self):
        """설정 창 열기"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ 시스템 설정")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # 설정 내용
        ttk.Label(settings_window, text="시스템 설정", font=("Arial", 14, "bold")).pack(pady=10)
        
        # 모델 경로 설정
        model_frame = ttk.LabelFrame(settings_window, text="모델 파일 경로", padding="10")
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(model_frame, text="ML 모델:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(model_frame, text="models/enhanced_safety_model.pkl", width=30).grid(row=0, column=1, padx=5)
        
        ttk.Label(model_frame, text="DL 모델:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(model_frame, text="models/neural_safety_model.pth", width=30).grid(row=1, column=1, padx=5)
        
        # GPU 설정
        gpu_frame = ttk.LabelFrame(settings_window, text="GPU 설정", padding="10")
        gpu_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(gpu_frame, text="CUDA 디바이스:").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(gpu_frame, values=["cuda:0", "cpu"], state="readonly", width=27).grid(row=0, column=1, padx=5)
        
        # 닫기 버튼
        ttk.Button(settings_window, text="확인", command=settings_window.destroy).pack(pady=20)
    
    def show_help(self):
        """도움말 표시"""
        help_text = """🛡️ 육군 종합정비창 안전 예측 시스템 사용법

📋 기본 사용법:
1. 왼쪽 패널에 사용자 정보를 입력하세요
2. 임무 종류와 예측 모드를 선택하세요
3. '안전 예측 실행' 버튼을 클릭하세요
4. 예측 결과를 확인하고 '엑셀로 저장'하세요

🔧 주요 기능:
• ML 모델: 시간대별 위험지수 예측
• DL 모델: 실시간 위험 키워드 및 안전대책 생성
• 통합 모드: ML + DL 모델 결합 예측
• GPU 가속: CUDA 지원 시 고속 처리

⚠️ 주의사항:
• 정확한 개인정보 입력 필수
• GPU 사용 시 CUDA 설치 필요
• 예측 결과는 참고용으로만 사용

📞 문의: 프로젝트 GitHub Issues
📅 버전: v1.0 (2025-10-07)"""
        
        messagebox.showinfo("도움말", help_text)

def main():
    """메인 함수"""
    try:
        root = tk.Tk()
        app = SafetyPredictionApp(root)
        root.mainloop()
    except Exception as e:
        print(f"프로그램 실행 오류: {e}")
        input("엔터키를 눌러 종료하세요...")

if __name__ == "__main__":
    main()
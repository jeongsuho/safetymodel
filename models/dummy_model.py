#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
더미 모델 구현 - 실제 ML/DL 모델 통합 전 테스트용

이 파일은 프로토타입에서 실제 모델처럼 동작하는 더미 모델을 제공합니다.
실제 프로젝트에서는 정수호님의 ML/DL 모델로 교체해야 합니다.
"""

import numpy as np
import pandas as pd
import json
import pickle
from datetime import datetime, timedelta
import random
from pathlib import Path

class DummyMLModel:
    """머신러닝 모델 더미 구현"""
    
    def __init__(self):
        self.model_loaded = False
        self.feature_names = [
            'gender_encoded', 'age', 'service_years', 
            'weather_temp', 'weather_humidity', 'weather_condition',
            'month', 'weekday', 'hour'
        ]
        self.load_model()
    
    def load_model(self):
        """모델 로딩 시뮬레이션"""
        try:
            # 실제 구현에서는 다음과 같이 로드:
            # self.model = joblib.load('enhanced_safety_model.pkl')
            # self.encoders = joblib.load('enhanced_encoders.pkl')
            # self.scaler = joblib.load('enhanced_scaler.pkl')
            
            print("✅ ML 모델 로딩 완료 (더미)")
            self.model_loaded = True
            
        except Exception as e:
            print(f"❌ ML 모델 로딩 실패: {e}")
            self.model_loaded = False
    
    def predict_risk_score(self, user_info, mission_type, prediction_hours=24):
        """위험지수 예측"""
        if not self.model_loaded:
            raise RuntimeError("모델이 로드되지 않았습니다")
        
        # 사용자 정보 기반 기본 위험도 계산
        base_risk = 5.0
        
        # 나이 요인 (30세 기준)
        age_factor = abs(int(user_info['age']) - 30) * 0.05
        base_risk += min(age_factor, 2.0)
        
        # 경험 요인 (경험이 많을수록 위험 감소)
        experience_factor = max(0, 3 - int(user_info['service_years'])) * 0.3
        base_risk += experience_factor
        
        # 임무 유형별 위험도
        mission_risks = {
            '복합적층장갑': 7.2,
            '엔진정비': 6.8,
            '전기계통': 7.5,
            '유압시스템': 8.1,
            '무기체계': 8.5
        }
        mission_risk = mission_risks.get(mission_type, 7.0)
        
        # 시간대별 예측 생성
        predictions = []
        current_time = datetime.now()
        
        for hour in range(prediction_hours):
            # 시간대별 변동 요인
            hour_of_day = (current_time.hour + hour) % 24
            
            # 야간/새벽 시간대 위험도 증가
            if 22 <= hour_of_day or hour_of_day <= 6:
                time_factor = 1.2
            elif 8 <= hour_of_day <= 17:  # 정규 근무시간
                time_factor = 0.9
            else:
                time_factor = 1.0
            
            # 최종 위험지수 계산
            final_risk = (base_risk + mission_risk) / 2 * time_factor
            
            # 랜덤 변동 추가 (±0.5)
            final_risk += np.random.uniform(-0.5, 0.5)
            
            # 범위 제한 (0~10)
            final_risk = np.clip(final_risk, 0.0, 10.0)
            
            predictions.append({
                'timestamp': current_time + timedelta(hours=hour),
                'risk_score': round(final_risk, 1),
                'hour_of_day': hour_of_day,
                'risk_level': self.get_risk_level(final_risk)
            })
        
        return predictions
    
    def get_risk_level(self, risk_score):
        """위험지수를 등급으로 변환"""
        if risk_score >= 8.0:
            return '높음'
        elif risk_score >= 6.0:
            return '보통'
        else:
            return '낮음'
    
    def recommend_safe_missions(self, user_info, available_missions=None):
        """안전한 임무 추천"""
        if available_missions is None:
            available_missions = ['복합적층장갑', '엔진정비', '전기계통', '유압시스템']
        
        mission_scores = {}
        for mission in available_missions:
            predictions = self.predict_risk_score(user_info, mission, 1)
            mission_scores[mission] = predictions[0]['risk_score']
        
        # 위험지수 낮은 순으로 정렬
        recommended = sorted(mission_scores.items(), key=lambda x: x[1])
        
        return [
            {
                'mission': mission,
                'risk_score': score,
                'recommendation': f'위험지수 {score} - {self.get_risk_level(score)}'
            }
            for mission, score in recommended
        ]

class DummyDLModel:
    """딥러닝 모델 더미 구현"""
    
    def __init__(self):
        self.model_loaded = False
        self.vocab_size = 5000
        self.load_model()
    
    def load_model(self):
        """모델 로딩 시뮬레이션"""
        try:
            # 실제 구현에서는 다음과 같이 로드:
            # import torch
            # self.model = torch.load('neural_safety_model.pth')
            # self.vocab = pickle.load(open('neural_vocab.pkl', 'rb'))
            
            print("✅ DL 모델 로딩 완료 (더미)")
            self.model_loaded = True
            
        except Exception as e:
            print(f"❌ DL 모델 로딩 실패: {e}")
            self.model_loaded = False
    
    def generate_risk_keywords(self, user_info, mission_type, num_keywords=10):
        """위험 키워드 생성"""
        if not self.model_loaded:
            raise RuntimeError("DL 모델이 로드되지 않았습니다")
        
        # 임무별 기본 키워드
        base_keywords = {
            '복합적층장갑': [
                '적층 작업 위험', '접착제 화학 노출', '고온 경화 과정',
                '압력기 사용 주의', '환기 불량', '화재 위험'
            ],
            '엔진정비': [
                '엔진 고온부 접촉', '연료 누출', '회전체 끼임',
                '오일 미끄러짐', '배기가스 흡입', '전기 쇼트'
            ],
            '전기계통': [
                '감전 위험', '누전 화재', '고압 전류',
                '절연 불량', '접지 미흡', '전선 손상'
            ],
            '유압시스템': [
                '고압 유체 분사', '유압 호스 파열', '오일 누출',
                '압력 용기 폭발', '미끄러짐 사고', '화상 위험'
            ],
            '무기체계': [
                '폭발물 취급', '화약 화재', '기계적 충격',
                '금속 파편', '소음 피해', '독성 가스'
            ]
        }
        
        # 공통 안전 키워드
        common_keywords = [
            '개인보호구 미착용', '작업 절차 미준수', '안전교육 부족',
            '피로 누적', '주의력 분산', '응급상황 대응',
            '동료와의 소통 부족', '장비 점검 미흡', '환경 요인'
        ]
        
        # 개인 특성 기반 키워드 추가
        personal_keywords = []
        age = int(user_info['age'])
        service_years = int(user_info['service_years'])
        
        if age >= 50:
            personal_keywords.extend(['신체 기능 저하', '반응속도 지연'])
        elif age <= 25:
            personal_keywords.extend(['경험 부족', '과신 위험'])
            
        if service_years <= 2:
            personal_keywords.extend(['숙련도 부족', '절차 미숙지'])
        elif service_years >= 15:
            personal_keywords.extend(['관습적 작업', '안전 불감증'])
        
        # 키워드 조합 및 순위 부여
        mission_keywords = base_keywords.get(mission_type, common_keywords[:6])
        all_keywords = mission_keywords + common_keywords + personal_keywords
        
        # 중복 제거 및 랜덤 셔플
        unique_keywords = list(set(all_keywords))
        random.shuffle(unique_keywords)
        
        return unique_keywords[:num_keywords]
    
    def generate_risk_analysis(self, user_info, mission_type, keywords):
        """위험요인 자연어 분석"""
        name = user_info['name']
        age = user_info['age']
        mission = mission_type
        
        analysis = f"""🔍 {name}님의 {mission} 임무 위험 분석:

현재 {age}세 {name}님이 {mission} 작업을 수행할 때 예상되는 주요 위험요인들을 AI가 분석한 결과입니다.

주요 위험 포인트:
• {keywords[0]}: 가장 높은 주의가 필요한 영역
• {keywords[1]}: 작업 중 지속적인 모니터링 필요  
• {keywords[2]}: 사전 준비 및 점검 강화 필요

개인 맞춤 주의사항:
작업 경험과 개인 특성을 고려할 때, 특히 안전 절차 준수와 개인보호구 착용이 중요합니다. 
동료와의 원활한 소통을 통해 위험 상황을 사전에 예방하시기 바랍니다."""

        return analysis
    
    def recommend_safety_measures(self, user_info, mission_type, keywords, num_measures=5):
        """AI 안전대책 추천"""
        name = user_info['name']
        mission = mission_type
        
        # 기본 안전대책 템플릿
        base_measures = [
            "개인보호구 완전 착용 (안전모, 보호안경, 작업복, 안전화)",
            "작업 전 안전점검 체크리스트 100% 준수",
            "2인 1조 작업 시스템으로 상호 안전 확인",
            "1시간마다 10분 휴식으로 피로도 관리",
            "응급상황 대응 절차 숙지 및 비상연락망 확인"
        ]
        
        # 임무별 특화 안전대책
        mission_measures = {
            '복합적층장갑': [
                "작업장 환기 시설 가동 및 공기 질 모니터링",
                "접착제 사용 시 방독마스크 착용 필수",
                "고온 장비 주변 화상 방지 조치"
            ],
            '엔진정비': [
                "연료 누출 감지 장비 점검 후 작업 시작",
                "회전 부품 작업 시 느슨한 의복 착용 금지", 
                "엔진 냉각 후 정비 작업 실시"
            ],
            '전기계통': [
                "전원 차단 후 검전기로 무전압 확인",
                "절연 장갑 및 절연 공구 사용",
                "습도가 높은 날 작업 시 특별 주의"
            ]
        }
        
        # 개인 맞춤 안전대책
        personal_measures = []
        age = int(user_info['age'])
        
        if age >= 45:
            personal_measures.append("작업 중 충분한 조명 확보로 시야 확보")
        if int(user_info['service_years']) <= 3:
            personal_measures.append("숙련자의 지도 하에 작업 수행")
        
        # 조합 및 선별
        all_measures = base_measures.copy()
        if mission in mission_measures:
            all_measures.extend(mission_measures[mission])
        all_measures.extend(personal_measures)
        
        # 상위 N개 선택
        selected_measures = all_measures[:num_measures]
        
        return {
            'measures': selected_measures,
            'summary': f"{name}님의 {mission} 작업을 위한 맞춤형 안전대책 {len(selected_measures)}가지",
            'priority_level': '높음' if any(keyword in ['폭발', '화재', '감전'] for keyword in keywords) else '보통'
        }

def create_dummy_model_files():
    """더미 모델 파일들 생성 (테스트용)"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # 더미 ML 모델 파일
    dummy_ml_model = {
        'type': 'RandomForestRegressor',
        'features': ['gender', 'age', 'service_years', 'weather', 'month', 'weekday', 'hour'],
        'trained_date': datetime.now().isoformat(),
        'version': '1.0'
    }
    
    with open(models_dir / 'enhanced_safety_model.pkl', 'wb') as f:
        pickle.dump(dummy_ml_model, f)
    
    # 더미 인코더
    dummy_encoders = {
        'gender_encoder': {'남성': 0, '여성': 1},
        'weather_encoder': {'맑음': 0, '흐림': 1, '비': 2, '눈': 3}
    }
    
    with open(models_dir / 'enhanced_encoders.pkl', 'wb') as f:
        pickle.dump(dummy_encoders, f)
    
    # 더미 스케일러
    dummy_scaler = {
        'mean': [0.5, 35.0, 8.5, 20.0, 6.5, 3.2, 12.0],
        'std': [0.5, 12.0, 5.2, 8.0, 3.5, 1.8, 6.5]
    }
    
    with open(models_dir / 'enhanced_scaler.pkl', 'wb') as f:
        pickle.dump(dummy_scaler, f)
    
    # 더미 어휘 사전
    dummy_vocab = {
        'word_to_idx': {f'word_{i}': i for i in range(1000)},
        'idx_to_word': {i: f'word_{i}' for i in range(1000)},
        'vocab_size': 1000
    }
    
    with open(models_dir / 'neural_vocab.pkl', 'wb') as f:
        pickle.dump(dummy_vocab, f)
    
    print("✅ 더미 모델 파일들이 models/ 폴더에 생성되었습니다.")
    print("📁 생성된 파일들:")
    for file_path in models_dir.glob("*.pkl"):
        print(f"   - {file_path}")

if __name__ == "__main__":
    # 테스트 실행
    print("🧪 더미 모델 테스트 시작")
    
    # 더미 파일 생성
    create_dummy_model_files()
    
    # 모델 테스트
    ml_model = DummyMLModel()
    dl_model = DummyDLModel()
    
    # 테스트 데이터
    test_user = {
        'name': '정수호',
        'gender': '남성', 
        'age': '30',
        'service_years': '5'
    }
    
    # ML 모델 테스트
    print("\n🔮 ML 모델 예측 테스트:")
    predictions = ml_model.predict_risk_score(test_user, '복합적층장갑', 24)
    print(f"   24시간 예측 완료: 평균 위험지수 {np.mean([p['risk_score'] for p in predictions]):.1f}")
    
    # DL 모델 테스트  
    print("\n🔮 DL 모델 예측 테스트:")
    keywords = dl_model.generate_risk_keywords(test_user, '복합적층장갑')
    print(f"   위험 키워드 {len(keywords)}개 생성: {keywords[:3]}...")
    
    analysis = dl_model.generate_risk_analysis(test_user, '복합적층장갑', keywords)
    print(f"   위험 분석 생성 완료 (길이: {len(analysis)}자)")
    
    measures = dl_model.recommend_safety_measures(test_user, '복합적층장갑', keywords)
    print(f"   안전대책 {len(measures['measures'])}개 추천 완료")
    
    print("\n✅ 더미 모델 테스트 완료!")
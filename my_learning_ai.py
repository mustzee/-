#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
나만의 학습하는 AI (Personal Learning AI)
100% 무료 · 완전 오프라인 · 당신의 데이터로 학습

사용 방법:
    python my_learning_ai.py

필요한 패키지: 없음! (순수 Python으로 구현)
선택 사항: numpy, scikit-learn (더 빠른 학습)
"""

import json
import os
import math
import random
from datetime import datetime
from typing import List, Dict, Tuple


class SimpleNeuralNetwork:
    """
    간단한 신경망 구현 (순수 Python)
    로지스틱 회귀를 위한 단층 퍼셉트론
    """

    def __init__(self, input_size: int):
        """
        신경망 초기화

        Args:
            input_size: 입력 특성의 개수
        """
        self.input_size = input_size
        # 가중치 랜덤 초기화 (-1 ~ 1)
        self.weights = [random.uniform(-1, 1) for _ in range(input_size)]
        self.bias = random.uniform(-1, 1)
        self.learning_rate = 0.1

    def sigmoid(self, x: float) -> float:
        """시그모이드 활성화 함수"""
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def predict(self, inputs: List[float]) -> float:
        """
        예측 수행 (순전파)

        Args:
            inputs: 입력 데이터

        Returns:
            0-1 사이의 확률값
        """
        # 가중합 계산
        weighted_sum = self.bias
        for i in range(len(inputs)):
            weighted_sum += inputs[i] * self.weights[i]

        # 활성화 함수 적용
        return self.sigmoid(weighted_sum)

    def train_single(self, inputs: List[float], target: float):
        """
        단일 데이터로 학습 (경사하강법)

        Args:
            inputs: 입력 데이터
            target: 정답 (0 또는 1)
        """
        # 순전파
        prediction = self.predict(inputs)

        # 오차 계산
        error = target - prediction

        # 역전파 (가중치 업데이트)
        gradient = prediction * (1 - prediction)  # 시그모이드 미분

        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate * error * inputs[i] * gradient

        self.bias += self.learning_rate * error * gradient

    def train_batch(self, dataset: List[Dict], epochs: int = 100):
        """
        배치 학습

        Args:
            dataset: 학습 데이터셋 [{'inputs': [...], 'target': ...}, ...]
            epochs: 학습 반복 횟수
        """
        for epoch in range(epochs):
            for data in dataset:
                self.train_single(data['inputs'], data['target'])

    def save(self, filename: str):
        """모델 저장"""
        model_data = {
            'weights': self.weights,
            'bias': self.bias,
            'input_size': self.input_size
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, indent=2)

    def load(self, filename: str):
        """모델 불러오기"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                model_data = json.load(f)
                self.weights = model_data['weights']
                self.bias = model_data['bias']
                self.input_size = model_data['input_size']
            return True
        return False


class PersonalAI:
    """개인 맞춤형 학습 AI"""

    def __init__(self):
        """초기화"""
        self.ai = SimpleNeuralNetwork(3)  # 3개 입력: 기분, 수면, 날씨
        self.training_data = []
        self.stats = {
            'data_count': 0,
            'prediction_count': 0,
            'correct_predictions': 0
        }

        self.data_file = 'my_ai_data.json'
        self.model_file = 'my_ai_model.json'

        self.load_data()

    def add_data(self, mood: float, sleep: float, weather: float, exercise: int):
        """
        데이터 추가 및 학습

        Args:
            mood: 기분 (1-10)
            sleep: 수면 시간 (시간)
            weather: 날씨 (1=맑음, 0.5=흐림, 0=비)
            exercise: 운동 여부 (1=예, 0=아니오)
        """
        # 데이터 정규화
        normalized_inputs = [
            mood / 10,      # 0-1 범위로
            sleep / 12,     # 0-1 범위로
            weather
        ]

        data = {
            'inputs': normalized_inputs,
            'target': exercise,
            'raw': {
                'mood': mood,
                'sleep': sleep,
                'weather': weather,
                'exercise': exercise
            },
            'date': datetime.now().isoformat()
        }

        self.training_data.append(data)
        self.stats['data_count'] += 1

        # 데이터가 3개 이상이면 학습
        if len(self.training_data) >= 3:
            print("\n🧠 AI 학습 중...", end=' ')
            self.ai.train_batch(self.training_data, epochs=50)
            print("완료!")

        self.save_data()

    def predict(self, mood: float, sleep: float, weather: float) -> Dict:
        """
        예측 수행

        Args:
            mood: 기분 (1-10)
            sleep: 수면 시간
            weather: 날씨

        Returns:
            예측 결과 딕셔너리
        """
        if len(self.training_data) < 3:
            return {
                'success': False,
                'message': '최소 3개의 데이터가 필요합니다!'
            }

        # 입력 정규화
        inputs = [
            mood / 10,
            sleep / 12,
            weather
        ]

        # 예측
        probability = self.ai.predict(inputs)
        prediction = 1 if probability > 0.5 else 0
        confidence = abs(probability - 0.5) * 200  # 0-100%

        self.stats['prediction_count'] += 1
        self.save_data()

        return {
            'success': True,
            'prediction': prediction,
            'probability': probability,
            'confidence': confidence,
            'message': '오늘 운동할 가능성이 높습니다! 🏃' if prediction == 1
                      else '오늘은 휴식이 필요할 것 같습니다 😴'
        }

    def show_stats(self):
        """통계 표시"""
        accuracy = 0
        if self.stats['prediction_count'] > 0:
            accuracy = (self.stats['correct_predictions'] / self.stats['prediction_count']) * 100

        print("\n" + "="*60)
        print("📊 AI 학습 통계")
        print("="*60)
        print(f"학습 데이터:   {self.stats['data_count']}개")
        print(f"예측 횟수:     {self.stats['prediction_count']}회")
        print(f"예측 정확도:   {accuracy:.1f}%")
        print("="*60)

        print(f"\n🧠 AI 모델 정보:")
        print(f"   알고리즘: 로지스틱 회귀 (신경망)")
        print(f"   가중치: {[f'{w:.3f}' for w in self.ai.weights]}")
        print(f"   편향: {self.ai.bias:.3f}")
        print(f"   학습률: {self.ai.learning_rate}")

    def show_data(self):
        """학습 데이터 표시"""
        if not self.training_data:
            print("\n아직 데이터가 없습니다.")
            return

        print("\n" + "="*60)
        print("📚 학습 데이터")
        print("="*60)

        for i, data in enumerate(reversed(self.training_data[-10:]), 1):
            raw = data['raw']
            weather_emoji = '☀️' if raw['weather'] == 1 else '⛅' if raw['weather'] == 0.5 else '🌧️'
            exercise_emoji = '✅' if raw['exercise'] == 1 else '❌'

            print(f"\n데이터 #{len(self.training_data) - i + 1}")
            print(f"  기분: {raw['mood']}/10 | 수면: {raw['sleep']}h | "
                  f"날씨: {weather_emoji} | 운동: {exercise_emoji}")
            print(f"  날짜: {data['date'][:10]}")

    def save_data(self):
        """데이터 및 모델 저장"""
        # 데이터 저장
        save_data = {
            'training_data': self.training_data,
            'stats': self.stats,
            'last_updated': datetime.now().isoformat()
        }

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        # 모델 저장
        self.ai.save(self.model_file)

    def load_data(self):
        """데이터 및 모델 불러오기"""
        # 데이터 불러오기
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                self.training_data = save_data.get('training_data', [])
                self.stats = save_data.get('stats', self.stats)

        # 모델 불러오기
        if os.path.exists(self.model_file):
            self.ai.load(self.model_file)
        elif len(self.training_data) >= 3:
            # 모델 파일이 없으면 재학습
            print("🧠 AI 재학습 중...", end=' ')
            self.ai.train_batch(self.training_data, epochs=100)
            print("완료!")

    def export_data(self):
        """데이터 내보내기"""
        filename = f"my_ai_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_data = {
            'training_data': self.training_data,
            'stats': self.stats,
            'model': {
                'weights': self.ai.weights,
                'bias': self.ai.bias
            },
            'export_date': datetime.now().isoformat()
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 데이터가 '{filename}'로 내보내졌습니다!")


def print_header():
    """헤더 출력"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          🧠 나만의 학습하는 AI (Personal Learning AI)        ║
║                                                               ║
║        100% 무료 · 완전 오프라인 · 당신의 데이터로 학습      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

💡 이 AI는 당신의 습관 패턴을 학습하여 개인 맞춤형 조언을 제공합니다.

명령어:
  1. 데이터 추가   - 새로운 데이터 입력 및 학습
  2. 예측하기      - AI가 예측 수행
  3. 통계 보기     - 학습 통계 확인
  4. 데이터 보기   - 학습 데이터 확인
  5. 내보내기      - 백업 파일 생성
  0. 종료

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """실수 입력 받기 (유효성 검사)"""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"❌ {min_val} 이상의 값을 입력하세요.")
                continue
            if max_val is not None and value > max_val:
                print(f"❌ {max_val} 이하의 값을 입력하세요.")
                continue
            return value
        except ValueError:
            print("❌ 숫자를 입력하세요.")


def get_choice_input(prompt: str, choices: List[str]) -> int:
    """선택지 입력 받기"""
    print(prompt)
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")

    while True:
        try:
            value = int(input("선택: "))
            if 1 <= value <= len(choices):
                return value - 1
            print(f"❌ 1-{len(choices)} 사이의 숫자를 입력하세요.")
        except ValueError:
            print("❌ 숫자를 입력하세요.")


def add_data_menu(ai: PersonalAI):
    """데이터 추가 메뉴"""
    print("\n" + "="*60)
    print("📝 새 데이터 입력")
    print("="*60)

    mood = get_float_input("😊 오늘 기분은? (1-10): ", 1, 10)
    sleep = get_float_input("😴 수면 시간은? (시간): ", 0, 24)

    weather_idx = get_choice_input("🌤️ 오늘 날씨는?", ["☀️ 맑음", "⛅ 흐림", "🌧️ 비/눈"])
    weather = [1, 0.5, 0][weather_idx]

    exercise_idx = get_choice_input("🏃 운동 했나요?", ["예", "아니오"])
    exercise = 1 - exercise_idx

    ai.add_data(mood, sleep, weather, exercise)
    print("\n✅ 데이터가 추가되고 AI가 학습했습니다!")


def predict_menu(ai: PersonalAI):
    """예측 메뉴"""
    print("\n" + "="*60)
    print("🔮 AI 예측")
    print("="*60)

    mood = get_float_input("😊 오늘 기분은? (1-10): ", 1, 10)
    sleep = get_float_input("😴 오늘 수면 시간은? (시간): ", 0, 24)

    weather_idx = get_choice_input("🌤️ 오늘 날씨는?", ["☀️ 맑음", "⛅ 흐림", "🌧️ 비/눈"])
    weather = [1, 0.5, 0][weather_idx]

    result = ai.predict(mood, sleep, weather)

    print("\n" + "="*60)
    if result['success']:
        print(f"🤖 AI 예측: {result['message']}")
        print(f"   확률: {result['probability']*100:.1f}%")
        print(f"   신뢰도: {result['confidence']:.1f}%")
    else:
        print(f"⚠️ {result['message']}")
    print("="*60)


def main():
    """메인 함수"""
    ai = PersonalAI()
    print_header()

    if ai.stats['data_count'] > 0:
        print(f"📚 기존 데이터 {ai.stats['data_count']}개를 불러왔습니다.\n")

    while True:
        try:
            print("\n명령어를 선택하세요:")
            choice = input(">>> ").strip()

            if choice == '1':
                add_data_menu(ai)

            elif choice == '2':
                predict_menu(ai)

            elif choice == '3':
                ai.show_stats()

            elif choice == '4':
                ai.show_data()

            elif choice == '5':
                ai.export_data()

            elif choice == '0':
                print("\n👋 AI가 저장되었습니다. 좋은 하루 되세요!\n")
                break

            elif choice == 'help' or choice == 'h':
                print_header()

            else:
                print("❌ 잘못된 명령어입니다. 0-5 사이의 숫자를 입력하세요.")

        except KeyboardInterrupt:
            print("\n\n👋 AI가 저장되었습니다. 좋은 하루 되세요!\n")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}\n")


if __name__ == "__main__":
    main()

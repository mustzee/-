#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
똑똑한 AI - 자연어 이해 + 재귀적 사고
100% 무료 · 완전 오프라인

사용 방법:
    python smart_ai.py

특징:
- 자연어 입력 이해 ("오늘 기분 안 좋고 잠 못 잤어")
- 재귀적 예측 (과거 데이터 기억)
- 자동 패턴 분석 및 인사이트 생성
- 의사결정 트리 + 신경망 조합
"""

import json
import os
import re
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class NaturalLanguageProcessor:
    """자연어 처리 엔진 (오프라인)"""

    def __init__(self):
        # 감정 사전
        self.sentiments = {
            'positive': ['좋아', '행복', '기쁘', '최고', '완벽', '잘', '만족', '편안', '좋은', '즐거'],
            'negative': ['안좋', '나빠', '힘들', '피곤', '스트레스', '우울', '슬프', '짜증', '별로', '못']
        }

        # 날씨 키워드
        self.weather_keywords = {
            1.0: ['맑', '화창', '쾌청', '날씨좋', '햇살', '맑음'],
            0.5: ['흐림', '구름', '흐리'],
            0.0: ['비', '눈', '장마', '우천', '비옴']
        }

    def parse(self, text: str) -> Dict:
        """
        자연어를 구조화된 데이터로 변환

        Args:
            text: 사용자 입력 텍스트

        Returns:
            파싱된 정보 딕셔너리
        """
        return {
            'mood': self.extract_mood(text),
            'sleep': self.extract_sleep(text),
            'weather': self.extract_weather(text),
            'exercise': self.extract_exercise(text),
            'intent': self.extract_intent(text),
            'sentiment': self.analyze_sentiment(text),
            'original': text
        }

    def extract_mood(self, text: str) -> Optional[int]:
        """기분 추출 (1-10)"""
        # "기분 7" or "7점" 패턴
        match = re.search(r'(\d+)점?|기분.*?(\d+)', text)
        if match:
            mood = int(match.group(1) or match.group(2))
            return max(1, min(10, mood))

        # 감정 단어로 추정
        if self._contains_any(text, self.sentiments['positive']):
            return 8
        if self._contains_any(text, self.sentiments['negative']):
            return 4

        return None

    def extract_sleep(self, text: str) -> Optional[float]:
        """수면 시간 추출"""
        # "7시간" or "7시간 잤어"
        match = re.search(r'(\d+(?:\.\d+)?)\s*시간', text)
        if match:
            return float(match.group(1))

        # "못 잤어", "잠 못 잤어"
        if '못 잤' in text or '못자' in text or '안 잤' in text:
            return 4.0

        # "잘 잤어", "푹 잤어"
        if '잘 잤' in text or '푹 잤' in text:
            return 8.0

        return None

    def extract_weather(self, text: str) -> Optional[float]:
        """날씨 추출 (1=맑음, 0.5=흐림, 0=비)"""
        for value, keywords in self.weather_keywords.items():
            if self._contains_any(text, keywords):
                return value
        return None

    def extract_exercise(self, text: str) -> Optional[int]:
        """운동 여부 추출"""
        if '운동했' in text or '운동 했' in text:
            return 1
        if '안 했' in text or '못 했' in text or '안했' in text:
            return 0
        return None

    def extract_intent(self, text: str) -> str:
        """사용자 의도 추출"""
        if '왜' in text or '이유' in text:
            return 'explain'
        if '비교' in text or '차이' in text:
            return 'compare'
        if '예측' in text or '내일' in text or '다음' in text or '어떨' in text:
            return 'predict'
        if '조언' in text or '추천' in text or '해줘' in text:
            return 'advise'
        return 'inform'

    def analyze_sentiment(self, text: str) -> str:
        """감정 분석"""
        pos_count = sum(1 for word in self.sentiments['positive'] if word in text)
        neg_count = sum(1 for word in self.sentiments['negative'] if word in text)

        if pos_count > neg_count:
            return 'positive'
        if neg_count > pos_count:
            return 'negative'
        return 'neutral'

    def _contains_any(self, text: str, keywords: List[str]) -> bool:
        """텍스트에 키워드가 포함되어 있는지 확인"""
        return any(keyword in text for keyword in keywords)


class RecursiveAI:
    """재귀적 신경망 (LSTM 스타일)"""

    def __init__(self):
        self.memory = []  # 과거 상태 기억
        self.max_memory = 7  # 지난 7일
        self.weights = {
            'current': [0.5, 0.5, 0.5],  # 현재 입력 가중치
            'memory': [0.3, 0.3, 0.3],    # 과거 기억 가중치
            'bias': 0.0
        }
        self.learning_rate = 0.1

    def predict_with_context(self, current_inputs: List[float]) -> float:
        """
        재귀적 예측 (과거 데이터 고려)

        Args:
            current_inputs: 현재 입력 데이터

        Returns:
            예측 확률 (0-1)
        """
        prediction = self.weights['bias']

        # 현재 입력
        for i, inp in enumerate(current_inputs):
            prediction += inp * self.weights['current'][i]

        # 과거 기억 (최근 데이터일수록 가중치 높음)
        recent_memory = self.memory[-self.max_memory:]

        for t, mem_data in enumerate(recent_memory):
            time_weight = (t + 1) / len(recent_memory)  # 최근일수록 높음
            mem_inputs = mem_data['inputs']

            for i, inp in enumerate(mem_inputs):
                prediction += inp * self.weights['memory'][i] * time_weight

        return self.sigmoid(prediction)

    def learn(self, inputs: List[float], target: float):
        """
        학습 (과거 데이터 포함)

        Args:
            inputs: 입력 데이터
            target: 정답 (0 또는 1)
        """
        prediction = self.predict_with_context(inputs)
        error = target - prediction
        gradient = prediction * (1 - prediction)

        # 가중치 업데이트
        for i in range(len(self.weights['current'])):
            self.weights['current'][i] += self.learning_rate * error * inputs[i] * gradient

        self.weights['bias'] += self.learning_rate * error * gradient

        # 메모리에 저장
        self.memory.append({
            'inputs': inputs,
            'target': target,
            'prediction': prediction,
            'timestamp': datetime.now().isoformat()
        })

        # 메모리 크기 제한
        if len(self.memory) > 50:
            self.memory.pop(0)

    def sigmoid(self, x: float) -> float:
        """시그모이드 활성화 함수"""
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def analyze_trend(self) -> Optional[Dict]:
        """트렌드 분석"""
        if len(self.memory) < 3:
            return None

        recent = self.memory[-7:]
        values = [m['target'] for m in recent]

        # 평균
        avg = sum(values) / len(values)

        # 추세 (상승/하락)
        mid = len(values) // 2
        first_half = values[:mid]
        second_half = values[mid:]

        first_avg = sum(first_half) / len(first_half) if first_half else 0
        second_avg = sum(second_half) / len(second_half) if second_half else 0

        # 일관성 (분산 기반)
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        consistency = 1 - min(variance, 1)

        return {
            'average': avg,
            'trend': 'increasing' if second_avg > first_avg else 'decreasing',
            'consistency': consistency
        }


class SmartAI:
    """똑똑한 AI 에이전트"""

    def __init__(self):
        self.nlp = NaturalLanguageProcessor()
        self.recursive_ai = RecursiveAI()
        self.context = []
        self.insights = []

        self.data_file = 'smart_ai_data.json'
        self.load_data()

    def process_natural_language(self, text: str) -> Dict:
        """
        자연어 입력 처리

        Args:
            text: 사용자 입력

        Returns:
            처리 결과
        """
        parsed = self.nlp.parse(text)

        # 의도에 따라 다른 처리
        handlers = {
            'explain': self.explain_patterns,
            'compare': self.compare_periods,
            'predict': lambda: self.predict_future(parsed),
            'advise': self.give_advice,
            'inform': lambda: self.handle_inform(parsed)
        }

        handler = handlers.get(parsed['intent'], lambda: self.handle_inform(parsed))
        return handler()

    def handle_inform(self, parsed: Dict) -> Dict:
        """데이터 입력 처리"""
        thinking = self.generate_thinking(parsed)
        response = self.generate_response(parsed)

        # 데이터가 충분히 파싱되었으면 학습
        if parsed['mood'] and parsed['sleep'] and parsed['exercise'] is not None:
            inputs = [
                parsed['mood'] / 10,
                parsed['sleep'] / 12,
                parsed['weather'] if parsed['weather'] is not None else 0.5
            ]

            self.recursive_ai.learn(inputs, parsed['exercise'])

            # 컨텍스트에 저장
            self.context.append({
                'date': datetime.now().isoformat(),
                'parsed': parsed,
                'inputs': inputs
            })

            # 인사이트 생성
            self.generate_insights()
            self.save_data()

        return {
            'thinking': thinking,
            'response': response,
            'parsed': parsed
        }

    def generate_thinking(self, parsed: Dict) -> str:
        """AI의 사고 과정 생성"""
        parts = []

        if parsed['mood']:
            parts.append(f"기분: {parsed['mood']}/10 인식")
        if parsed['sleep']:
            parts.append(f"수면: {parsed['sleep']}시간 파악")
        if parsed['weather'] is not None:
            weather_str = {1: '맑음', 0.5: '흐림', 0: '비/눈'}.get(parsed['weather'], '?')
            parts.append(f"날씨: {weather_str} 감지")
        if parsed['sentiment'] != 'neutral':
            sentiment_str = '긍정적' if parsed['sentiment'] == 'positive' else '부정적'
            parts.append(f"감정: {sentiment_str}")

        return ' | '.join(parts) if parts else '입력 분석 중...'

    def generate_response(self, parsed: Dict) -> str:
        """응답 생성"""
        response = []

        # 감정 공감
        if parsed['sentiment'] == 'negative':
            response.append('힘드셨겠어요.')
        elif parsed['sentiment'] == 'positive':
            response.append('좋은 하루를 보내셨네요!')

        # 데이터 확인
        confirmed = []
        if parsed['mood']:
            confirmed.append(f"기분 {parsed['mood']}점")
        if parsed['sleep']:
            confirmed.append(f"수면 {parsed['sleep']}시간")
        if parsed['weather'] is not None:
            weather_map = {1: '맑은 날씨', 0.5: '흐린 날씨', 0: '비/눈'}
            confirmed.append(weather_map[parsed['weather']])

        if confirmed:
            response.append(f"{', '.join(confirmed)}로 기록했습니다.")

        # 예측 (데이터가 있으면)
        if len(self.recursive_ai.memory) >= 3 and parsed['mood'] and parsed['sleep']:
            inputs = [
                parsed['mood'] / 10,
                parsed['sleep'] / 12,
                parsed['weather'] if parsed['weather'] is not None else 0.5
            ]
            prob = self.recursive_ai.predict_with_context(inputs)
            will_exercise = prob > 0.5

            response.append(
                f"\n{'오늘 운동하실 것 같네요!' if will_exercise else '오늘은 휴식이 필요해 보여요.'} "
                f"(확률: {prob * 100:.0f}%)"
            )

        return '\n'.join(response)

    def explain_patterns(self) -> Dict:
        """패턴 설명"""
        if not self.insights:
            return {
                'thinking': '패턴 분석 중...',
                'response': '아직 데이터가 부족해요. 최소 5개 이상의 데이터를 입력해주세요!',
                'parsed': {'intent': 'explain'}
            }

        trend = self.recursive_ai.analyze_trend()
        response = ['제가 발견한 패턴을 설명드릴게요:\n']

        for i, insight in enumerate(self.insights, 1):
            response.append(f"{i}. {insight}")

        if trend:
            response.append(f"\n최근 추세: {('상승 중 📈' if trend['trend'] == 'increasing' else '하락 중 📉')}")
            response.append(f"일관성: {trend['consistency'] * 100:.0f}%")

        return {
            'thinking': '과거 데이터 분석 → 패턴 추출 → 설명 생성',
            'response': '\n'.join(response),
            'parsed': {'intent': 'explain'}
        }

    def compare_periods(self) -> Dict:
        """기간 비교"""
        if len(self.context) < 5:
            return {
                'thinking': '비교 분석 시도...',
                'response': '비교하려면 최소 5일치 데이터가 필요해요!',
                'parsed': {'intent': 'compare'}
            }

        mid = len(self.context) // 2
        first_half = self.context[:mid]
        second_half = self.context[mid:]

        def calc_avg(data_list):
            moods = [d['parsed']['mood'] for d in data_list if d['parsed']['mood']]
            sleeps = [d['parsed']['sleep'] for d in data_list if d['parsed']['sleep']]
            return {
                'mood': sum(moods) / len(moods) if moods else 0,
                'sleep': sum(sleeps) / len(sleeps) if sleeps else 0
            }

        avg1 = calc_avg(first_half)
        avg2 = calc_avg(second_half)

        response = [
            '기간별 비교 결과:\n',
            '전반부 평균:',
            f"  기분: {avg1['mood']:.1f}점",
            f"  수면: {avg1['sleep']:.1f}시간\n",
            '후반부 평균:',
            f"  기분: {avg2['mood']:.1f}점 ({'↑' if avg2['mood'] > avg1['mood'] else '↓'})",
            f"  수면: {avg2['sleep']:.1f}시간 ({'↑' if avg2['sleep'] > avg1['sleep'] else '↓'})"
        ]

        return {
            'thinking': '데이터 분할 → 평균 계산 → 차이 분석',
            'response': '\n'.join(response),
            'parsed': {'intent': 'compare'}
        }

    def predict_future(self, parsed: Dict) -> Dict:
        """미래 예측"""
        if len(self.recursive_ai.memory) < 3:
            return {
                'thinking': '예측 시도...',
                'response': '예측하려면 최소 3일치 데이터가 필요해요!',
                'parsed': parsed
            }

        # 최근 평균으로 예측
        recent = self.recursive_ai.memory[-3:]
        avg_inputs = [0.0, 0.0, 0.0]

        for data in recent:
            for i in range(3):
                avg_inputs[i] += data['inputs'][i]

        avg_inputs = [x / len(recent) for x in avg_inputs]

        prob = self.recursive_ai.predict_with_context(avg_inputs)
        trend = self.recursive_ai.analyze_trend()

        response = [
            '내일 예측:\n',
            f"운동 확률: {prob * 100:.0f}%",
            f"추세: {('개선 중' if trend['trend'] == 'increasing' else '주의 필요')}\n"
        ]

        if prob > 0.6:
            response.append('💪 좋은 컨디션이 예상되네요!')
        elif prob > 0.4:
            response.append('🤔 보통 정도의 컨디션이 예상됩니다.')
        else:
            response.append('😴 충분한 휴식이 필요해 보여요.')

        return {
            'thinking': '최근 패턴 분석 → 재귀적 예측 → 결과 생성',
            'response': '\n'.join(response),
            'parsed': parsed
        }

    def give_advice(self) -> Dict:
        """조언 생성"""
        if len(self.context) < 3:
            return {
                'thinking': '조언 생성 중...',
                'response': '조언을 드리려면 좀 더 많은 데이터가 필요해요!',
                'parsed': {'intent': 'advise'}
            }

        recent = self.context[-7:]

        moods = [c['parsed']['mood'] for c in recent if c['parsed']['mood']]
        sleeps = [c['parsed']['sleep'] for c in recent if c['parsed']['sleep']]

        avg_mood = sum(moods) / len(moods) if moods else 7
        avg_sleep = sum(sleeps) / len(sleeps) if sleeps else 7

        response = ['당신을 위한 조언:\n']

        if avg_sleep < 6:
            response.append('💤 수면 시간이 부족해요. 최소 7시간 수면을 목표로 해보세요.')

        if avg_mood < 6:
            response.append('😊 기분이 좋지 않은 날이 많네요. 좋아하는 활동을 더 자주 해보세요.')

        if avg_sleep >= 7 and avg_mood >= 7:
            response.append('✨ 좋은 상태를 유지하고 계시네요! 계속 이 패턴을 유지하세요.')

        return {
            'thinking': '데이터 집계 → 패턴 분석 → 맞춤 조언 생성',
            'response': '\n'.join(response),
            'parsed': {'intent': 'advise'}
        }

    def generate_insights(self):
        """인사이트 생성"""
        self.insights = []

        if len(self.context) < 5:
            return

        # 상관관계 분석
        correlations = self.calculate_correlations()

        if correlations['mood'] > 0.5:
            self.insights.append('기분이 좋을 때 운동을 더 자주 하시네요')

        if correlations['sleep'] > 0.5:
            self.insights.append('충분히 주무시면 운동을 잘 하시는 편이에요')

        if correlations['weather'] > 0.3:
            self.insights.append('날씨가 좋을 때 활동적이시네요')

        # 일관성
        trend = self.recursive_ai.analyze_trend()
        if trend and trend['consistency'] > 0.7:
            self.insights.append('매우 규칙적인 생활 패턴을 보이고 계세요')

    def calculate_correlations(self) -> Dict[str, float]:
        """상관관계 계산"""
        data = [
            c for c in self.context
            if c['parsed']['mood'] and c['parsed']['sleep'] and c['parsed']['exercise'] is not None
        ]

        if len(data) < 3:
            return {'mood': 0, 'sleep': 0, 'weather': 0}

        exercise_avg = sum(d['parsed']['exercise'] for d in data) / len(data)

        correlations = {}
        features = ['mood', 'sleep', 'weather']

        for idx, feature in enumerate(features):
            correlation_sum = 0

            for d in data:
                if idx == 0:
                    feature_val = d['parsed']['mood'] / 10
                elif idx == 1:
                    feature_val = d['parsed']['sleep'] / 12
                else:
                    feature_val = d['parsed']['weather'] if d['parsed']['weather'] is not None else 0.5

                correlation_sum += (feature_val - 0.5) * (d['parsed']['exercise'] - exercise_avg)

            correlations[feature] = abs(correlation_sum / len(data))

        return correlations

    def save_data(self):
        """데이터 저장"""
        data = {
            'context': self.context,
            'memory': self.recursive_ai.memory,
            'weights': self.recursive_ai.weights,
            'insights': self.insights,
            'last_updated': datetime.now().isoformat()
        }

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        """데이터 불러오기"""
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.context = data.get('context', [])
            self.recursive_ai.memory = data.get('memory', [])
            self.recursive_ai.weights = data.get('weights', self.recursive_ai.weights)
            self.insights = data.get('insights', [])

            print(f"✅ 기존 데이터 {len(self.context)}개를 불러왔습니다.")
        except Exception as e:
            print(f"⚠️ 데이터 불러오기 실패: {e}")

    def show_insights(self):
        """인사이트 표시"""
        print("\n" + "=" * 60)
        print("🔍 AI가 발견한 패턴")
        print("=" * 60)

        if not self.insights:
            print("아직 충분한 데이터가 없습니다.")
            return

        for i, insight in enumerate(self.insights, 1):
            print(f"{i}. {insight}")

        # 상관관계
        correlations = self.calculate_correlations()
        print(f"\n📊 상관관계 분석:")
        print(f"  기분: {correlations['mood'] * 100:.0f}%")
        print(f"  수면: {correlations['sleep'] * 100:.0f}%")
        print(f"  날씨: {correlations['weather'] * 100:.0f}%")

        print("=" * 60)


def print_header():
    """헤더 출력"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          🧠 똑똑한 AI - 자연어 이해 + 재귀적 사고            ║
║                                                               ║
║        100% 무료 · 완전 오프라인 · 자동 해석                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

💡 자연어로 말하세요:
  • "오늘 기분 안 좋고 잠 못 잤어"
  • "요즘 계속 피곤한데 왜 그럴까?"
  • "지난주랑 이번주 비교해줘"
  • "내일은 어떨 것 같아?"

명령어:
  /insights  - AI가 발견한 패턴 보기
  /help      - 도움말
  /quit      - 종료

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def main():
    """메인 함수"""
    ai = SmartAI()
    print_header()

    while True:
        try:
            user_input = input("\n당신: ").strip()

            if not user_input:
                continue

            # 명령어 처리
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("\n👋 데이터가 저장되었습니다. 좋은 하루 되세요!\n")
                break

            elif user_input.lower() in ['/insights', '/i']:
                ai.show_insights()

            elif user_input.lower() in ['/help', '/h']:
                print_header()

            else:
                # AI 처리
                result = ai.process_natural_language(user_input)

                print(f"\n🧠 AI 사고: {result['thinking']}")
                print(f"\nAI: {result['response']}")

                # 인사이트 표시 (랜덤)
                if ai.insights and result['parsed']['intent'] == 'inform':
                    import random
                    print(f"\n💡 인사이트: {random.choice(ai.insights)}")

        except KeyboardInterrupt:
            print("\n\n👋 데이터가 저장되었습니다. 좋은 하루 되세요!\n")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}\n")


if __name__ == "__main__":
    main()

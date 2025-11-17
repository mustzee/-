#!/usr/bin/env python3
"""
CPU 정보 확인 프로그램
내 컴퓨터의 CPU와 메모리 상태를 실시간으로 확인합니다.
"""

import os
import time
import psutil


def display_cpu_info():
    """CPU 정보를 보기 좋게 출력합니다"""

    print("="*60)
    print("💻 CPU 정보")
    print("="*60)

    # 기본 정보
    cpu_count_logical = os.cpu_count()
    cpu_count_physical = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()

    print(f"\n📊 CPU 코어:")
    print(f"   - 물리적 코어: {cpu_count_physical}")
    print(f"   - 논리적 코어: {cpu_count_logical}")

    if cpu_freq:
        print(f"\n⚡ CPU 속도:")
        print(f"   - 현재: {cpu_freq.current:.0f} MHz")
        print(f"   - 최대: {cpu_freq.max:.0f} MHz")

    # CPU 사용률
    print(f"\n📈 CPU 사용률 (5초간 측정):")
    for i in range(5):
        cpu_percent = psutil.cpu_percent(interval=1)
        bar_length = int(cpu_percent / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"   [{bar}] {cpu_percent:5.1f}%", end='\r')
        time.sleep(0.1)

    print()  # 줄바꿈

    # 코어별 사용률
    print(f"\n📊 코어별 사용률:")
    per_cpu = psutil.cpu_percent(interval=1, percpu=True)
    for i, percent in enumerate(per_cpu):
        bar_length = int(percent / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"   코어 {i:2d}: [{bar}] {percent:5.1f}%")


def display_memory_info():
    """메모리 정보를 보기 좋게 출력합니다"""

    print("\n" + "="*60)
    print("💾 메모리 정보")
    print("="*60)

    memory = psutil.virtual_memory()

    total_gb = memory.total / (1024**3)
    used_gb = memory.used / (1024**3)
    available_gb = memory.available / (1024**3)

    print(f"\n📊 메모리 상태:")
    print(f"   - 전체: {total_gb:.1f} GB")
    print(f"   - 사용 중: {used_gb:.1f} GB")
    print(f"   - 사용 가능: {available_gb:.1f} GB")
    print(f"   - 사용률: {memory.percent}%")

    # 시각적 표시
    bar_length = int(memory.percent / 5)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    print(f"\n   [{bar}] {memory.percent:.1f}%")


def main():
    print("\n" + "🔍 컴퓨터 성능 분석 중..." + "\n")

    display_cpu_info()
    display_memory_info()

    print("\n" + "="*60)
    print("💡 팁:")
    print("="*60)
    print("""
1. CPU 코어가 많을수록 병렬처리가 효과적입니다
2. 논리적 코어 = 물리적 코어 × 2 (하이퍼스레딩)
3. 메모리 사용률이 80% 이상이면 분산처리를 고려하세요
4. 병렬처리 최대 속도 ≈ 물리적 코어 수
""")

    print("="*60)
    print("✅ CPU 정보 확인 완료!")
    print("👉 이제 Step 1에서 병렬처리의 위력을 체험해봅시다!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

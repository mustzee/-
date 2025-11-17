#!/usr/bin/env python3
"""
빠른 프로그램: 병렬 처리
여러 작업을 동시에 처리합니다!
"""

import time
from concurrent.futures import ProcessPoolExecutor
import os


def process_number(n):
    """
    숫자를 처리하는 함수
    slow_program.py와 동일한 작업
    """
    time.sleep(1)  # 1초 대기
    return n * n


def main():
    print("="*50)
    print("병렬 처리 (동시에 여러 개)")
    print("="*50)

    numbers = list(range(1, 11))  # 1부터 10까지
    print(f"처리할 숫자: {numbers}")

    # 사용할 CPU 코어 수
    cpu_cores = min(os.cpu_count(), len(numbers))
    print(f"사용할 CPU 코어: {cpu_cores}개\n")

    print("모든 작업 동시 시작!")
    start_time = time.time()

    # 병렬로 처리
    with ProcessPoolExecutor(max_workers=cpu_cores) as executor:
        results = list(executor.map(process_number, numbers))

    end_time = time.time()
    duration = end_time - start_time

    print("\n모든 작업 완료!")
    print(f"결과: {results}")
    print(f"총 시간: {duration:.2f}초")
    print("="*50)

    # 순차 처리 시간 계산
    sequential_time = len(numbers)
    speedup = sequential_time / duration

    print(f"\n📊 성능 비교:")
    print(f"   순차 처리 (예상): {sequential_time}초")
    print(f"   병렬 처리 (실제): {duration:.2f}초")
    print(f"   속도 향상: {speedup:.1f}배! 🚀")
    print(f"   절약된 시간: {sequential_time - duration:.2f}초")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
느린 프로그램: 순차 처리
하나씩 차례대로 처리합니다.
"""

import time


def process_number(n):
    """
    숫자를 처리하는 함수
    실제로는 복잡한 계산이나 I/O 작업을 시뮬레이션
    """
    print(f"처리 중: {n}...")
    time.sleep(1)  # 1초 대기 (무거운 작업 시뮬레이션)
    return n * n


def main():
    print("="*50)
    print("순차 처리 (하나씩 차례대로)")
    print("="*50)

    numbers = range(1, 11)  # 1부터 10까지
    print(f"처리할 숫자: {list(numbers)}\n")

    start_time = time.time()

    # 하나씩 순차적으로 처리
    results = []
    for n in numbers:
        result = process_number(n)
        results.append(result)

    end_time = time.time()
    duration = end_time - start_time

    print(f"\n결과: {results}")
    print(f"총 시간: {duration:.2f}초")
    print("="*50)
    print(f"\n💡 {len(numbers)}개 작업 × 1초 = 약 {len(numbers)}초 소요")
    print("   순차 처리는 시간이 많이 걸립니다!")


if __name__ == "__main__":
    main()

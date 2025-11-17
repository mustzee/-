#!/usr/bin/env python3
"""
NumPy 벡터화: 가장 간단하고 빠른 병렬처리
"""

import numpy as np
import time


def slow_way(data):
    """일반 Python 루프 (느림)"""
    result = []
    for x in data:
        result.append(x ** 2 + 2 * x + 1)
    return result


def fast_way(data):
    """NumPy 벡터화 (빠름)"""
    return data ** 2 + 2 * data + 1


def main():
    print("="*60)
    print("NumPy 벡터화의 힘")
    print("="*60)

    # 테스트 크기
    sizes = [10_000, 100_000, 1_000_000]

    for size in sizes:
        print(f"\n📊 배열 크기: {size:,} 원소")
        print("-" * 60)

        # 데이터 생성
        data_list = list(range(size))
        data_numpy = np.arange(size)

        # 일반 Python
        start = time.time()
        result_slow = slow_way(data_list)
        slow_time = time.time() - start

        # NumPy
        start = time.time()
        result_fast = fast_way(data_numpy)
        fast_time = time.time() - start

        # 결과
        speedup = slow_time / fast_time
        print(f"일반 Python: {slow_time:.3f}초")
        print(f"NumPy:       {fast_time:.3f}초")
        print(f"속도 향상:   {speedup:.1f}배! 🚀")

    print("\n" + "="*60)
    print("💡 NumPy는 C로 작성되어 매우 빠릅니다!")
    print("   숫자 계산은 항상 NumPy를 사용하세요!")
    print("="*60)


if __name__ == "__main__":
    main()

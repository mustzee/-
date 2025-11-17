#!/usr/bin/env python3
"""
Python 버전: 성능 비교용
"""

import time
import numpy as np


def main():
    print("="*60)
    print("Python 버전")
    print("="*60)

    size = 10_000_000
    data = np.arange(size, dtype=np.int32)

    print(f"\n데이터 크기: {size:,} 원소\n")

    # 1. 배열 계산
    print("1️⃣ 배열 계산 (제곱 + 2배 + 1)")
    start = time.time()
    result = data ** 2 + 2 * data + 1
    t1 = time.time() - start
    print(f"   시간: {t1:.3f}초\n")

    # 2. 필터링
    print("2️⃣ 필터링 (짝수만)")
    start = time.time()
    filtered = data[data % 2 == 0]
    t2 = time.time() - start
    print(f"   결과: {len(filtered):,} 원소")
    print(f"   시간: {t2:.3f}초\n")

    # 3. 합계
    print("3️⃣ 합계")
    start = time.time()
    total = np.sum(data)
    t3 = time.time() - start
    print(f"   합계: {total:,}")
    print(f"   시간: {t3:.3f}초\n")

    total_time = t1 + t2 + t3

    print("="*60)
    print(f"총 시간: {total_time:.3f}초")
    print("="*60)
    print("\n💡 이제 Rust 버전과 비교해보세요!")
    print("   cd compare_rust && cargo run --release")


if __name__ == "__main__":
    main()

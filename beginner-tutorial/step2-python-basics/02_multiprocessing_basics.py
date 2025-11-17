#!/usr/bin/env python3
"""
Multiprocessing 기초: CPU 집약적 작업의 병렬 처리
"""

import time
from multiprocessing import Pool, cpu_count
import os


def heavy_computation(n):
    """무거운 계산 (예: 이미지 처리, 데이터 분석)"""
    result = 0
    for i in range(n):
        result += i ** 2
    return result


def main():
    print("="*60)
    print("Multiprocessing Pool 사용법")
    print("="*60)
    print(f"CPU 코어: {cpu_count()}개\n")

    # 작업 리스트
    tasks = [1_000_000] * 8

    # 1. 순차 처리
    print("1️⃣ 순차 처리")
    start = time.time()
    results_seq = [heavy_computation(n) for n in tasks]
    seq_time = time.time() - start
    print(f"   시간: {seq_time:.2f}초\n")

    # 2. 병렬 처리 (Pool)
    print("2️⃣ 병렬 처리 (Pool)")
    start = time.time()
    with Pool(processes=cpu_count()) as pool:
        results_par = pool.map(heavy_computation, tasks)
    par_time = time.time() - start
    print(f"   시간: {par_time:.2f}초\n")

    # 결과
    print("="*60)
    print("📊 결과")
    print("="*60)
    print(f"속도 향상: {seq_time/par_time:.1f}배")
    print(f"절약 시간: {seq_time - par_time:.2f}초")
    print("\n💡 Pool은 자동으로 작업을 분산합니다!")


if __name__ == "__main__":
    main()

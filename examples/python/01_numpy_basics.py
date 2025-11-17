#!/usr/bin/env python3
"""
NumPy 기초 - 벡터화 연산의 힘
배열 연산을 통한 성능 향상 데모
"""

import numpy as np
import time
from typing import Tuple


def pure_python_computation(size: int) -> Tuple[float, float]:
    """순수 Python으로 배열 연산 (느림)"""
    data = list(range(size))

    start = time.perf_counter()
    result = []
    for x in data:
        result.append(x ** 2 + 2 * x + 1)
    duration = time.perf_counter() - start

    return duration, sum(result)


def numpy_computation(size: int) -> Tuple[float, float]:
    """NumPy 벡터화 연산 (빠름)"""
    data = np.arange(size)

    start = time.perf_counter()
    result = data ** 2 + 2 * data + 1
    duration = time.perf_counter() - start

    return duration, np.sum(result)


def demonstrate_broadcasting():
    """NumPy 브로드캐스팅 데모"""
    print("\n" + "="*60)
    print("NumPy 브로드캐스팅 예제")
    print("="*60)

    # 2D 행렬
    matrix = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])

    # 1D 배열
    row_vector = np.array([10, 20, 30])

    print("\n원본 행렬:")
    print(matrix)
    print("\n행 벡터:")
    print(row_vector)

    # 브로드캐스팅: 각 행에 벡터 더하기
    result = matrix + row_vector
    print("\n행렬 + 벡터 (브로드캐스팅):")
    print(result)


def advanced_operations():
    """고급 NumPy 연산"""
    print("\n" + "="*60)
    print("고급 NumPy 연산")
    print("="*60)

    # 대규모 데이터 생성
    size = 1_000_000
    data = np.random.randn(size)

    start = time.perf_counter()

    # 복잡한 연산 체인
    result = np.sqrt(np.abs(np.sin(data) * np.cos(data))) + np.exp(-data**2 / 2)

    # 통계 연산
    mean = np.mean(result)
    std = np.std(result)
    percentiles = np.percentile(result, [25, 50, 75])

    duration = time.perf_counter() - start

    print(f"\n배열 크기: {size:,} 원소")
    print(f"처리 시간: {duration*1000:.2f} ms")
    print(f"평균: {mean:.4f}")
    print(f"표준편차: {std:.4f}")
    print(f"사분위수: {percentiles}")


def matrix_operations():
    """행렬 연산 데모"""
    print("\n" + "="*60)
    print("행렬 연산")
    print("="*60)

    size = 1000
    A = np.random.randn(size, size)
    B = np.random.randn(size, size)

    # 행렬 곱셈
    start = time.perf_counter()
    C = np.dot(A, B)
    duration = time.perf_counter() - start

    print(f"\n{size}x{size} 행렬 곱셈")
    print(f"처리 시간: {duration*1000:.2f} ms")
    print(f"결과 행렬 크기: {C.shape}")

    # 전치와 대각합
    start = time.perf_counter()
    trace = np.trace(C)
    det = np.linalg.det(C[:100, :100])  # 작은 부분행렬의 행렬식
    duration = time.perf_counter() - start

    print(f"\n추가 연산 시간: {duration*1000:.2f} ms")
    print(f"대각합: {trace:.2e}")
    print(f"부분행렬 행렬식: {det:.2e}")


def memory_efficient_operations():
    """메모리 효율적인 연산"""
    print("\n" + "="*60)
    print("메모리 효율적인 연산")
    print("="*60)

    size = 10_000_000

    # In-place 연산으로 메모리 절약
    data = np.arange(size, dtype=np.float64)
    initial_memory = data.nbytes / (1024**2)  # MB

    print(f"\n초기 메모리 사용: {initial_memory:.2f} MB")

    start = time.perf_counter()

    # In-place 연산 (메모리 추가 할당 없음)
    data *= 2
    data += 1
    np.sqrt(data, out=data)

    duration = time.perf_counter() - start

    print(f"처리 시간: {duration*1000:.2f} ms")
    print(f"최종 메모리 사용: {data.nbytes / (1024**2):.2f} MB (변화 없음)")
    print(f"처리된 원소: {size:,}")


def main():
    print("="*60)
    print("NumPy 병렬 처리 기초")
    print("="*60)

    # 1. 성능 비교
    sizes = [10_000, 100_000, 1_000_000]

    print("\n순수 Python vs NumPy 성능 비교:")
    print("-" * 60)

    for size in sizes:
        py_time, py_result = pure_python_computation(size)
        np_time, np_result = numpy_computation(size)

        speedup = py_time / np_time

        print(f"\n크기: {size:,} 원소")
        print(f"  순수 Python: {py_time*1000:>8.2f} ms")
        print(f"  NumPy:        {np_time*1000:>8.2f} ms")
        print(f"  속도 향상:    {speedup:>8.2f}x")

        # 결과 검증
        assert abs(py_result - np_result) < 1e-6, "결과 불일치!"

    # 2. 브로드캐스팅
    demonstrate_broadcasting()

    # 3. 고급 연산
    advanced_operations()

    # 4. 행렬 연산
    matrix_operations()

    # 5. 메모리 효율성
    memory_efficient_operations()

    print("\n" + "="*60)
    print("요약")
    print("="*60)
    print("""
NumPy의 주요 장점:
1. 벡터화 연산: 10-100배 속도 향상
2. 브로드캐스팅: 간결하고 효율적인 코드
3. 메모리 효율: In-place 연산 지원
4. C/Fortran 기반: 네이티브 코드 성능
5. 광범위한 수학 함수 라이브러리

다음 단계: 02_parallel_concepts.py
""")


if __name__ == "__main__":
    main()

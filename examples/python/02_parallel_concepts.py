#!/usr/bin/env python3
"""
병렬 처리 기본 개념
프로세스, 스레드, 동시성의 차이점 이해
"""

import time
import threading
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
from typing import List


def cpu_bound_task(n: int) -> float:
    """CPU 집약적 작업 - 계산이 많음"""
    result = 0.0
    for i in range(n):
        result += np.sin(i) * np.cos(i)
    return result


def io_bound_task(duration: float) -> str:
    """I/O 집약적 작업 - 대기가 많음"""
    time.sleep(duration)
    return f"완료 (대기: {duration}초)"


def sequential_processing():
    """순차 처리"""
    print("\n" + "="*60)
    print("1. 순차 처리 (Single Thread)")
    print("="*60)

    tasks = [1_000_000] * 4

    start = time.perf_counter()
    results = [cpu_bound_task(n) for n in tasks]
    duration = time.perf_counter() - start

    print(f"작업 수: {len(tasks)}")
    print(f"총 시간: {duration:.2f}초")
    print(f"평균 작업 시간: {duration/len(tasks):.2f}초")

    return duration


def thread_based_processing():
    """스레드 기반 처리 (GIL 때문에 CPU 작업에는 비효율적)"""
    print("\n" + "="*60)
    print("2. 멀티스레드 처리 (Threading)")
    print("="*60)

    tasks = [1_000_000] * 4

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, tasks))
    duration = time.perf_counter() - start

    print(f"작업 수: {len(tasks)}")
    print(f"총 시간: {duration:.2f}초")
    print(f"스레드 수: 4")
    print("⚠️  GIL로 인해 CPU 작업에서는 속도 향상이 없거나 미미함")

    return duration


def process_based_processing():
    """프로세스 기반 처리 (진정한 병렬 처리)"""
    print("\n" + "="*60)
    print("3. 멀티프로세스 처리 (Multiprocessing)")
    print("="*60)

    tasks = [1_000_000] * 4

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, tasks))
    duration = time.perf_counter() - start

    print(f"작업 수: {len(tasks)}")
    print(f"총 시간: {duration:.2f}초")
    print(f"프로세스 수: 4")
    print("✓ 진정한 병렬 처리로 속도 향상")

    return duration


def io_bound_comparison():
    """I/O 작업에서는 스레드가 효율적"""
    print("\n" + "="*60)
    print("4. I/O 작업 비교")
    print("="*60)

    tasks = [0.5] * 8

    # 순차 처리
    start = time.perf_counter()
    results = [io_bound_task(d) for d in tasks]
    seq_duration = time.perf_counter() - start

    # 멀티스레드
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(io_bound_task, tasks))
    thread_duration = time.perf_counter() - start

    print(f"\n순차 처리: {seq_duration:.2f}초")
    print(f"멀티스레드: {thread_duration:.2f}초")
    print(f"속도 향상: {seq_duration/thread_duration:.2f}x")
    print("\n💡 I/O 작업에는 스레드가 적합 (GIL 영향 없음)")


def demonstrate_scaling():
    """코어 수에 따른 확장성 테스트"""
    print("\n" + "="*60)
    print("5. 확장성 테스트")
    print("="*60)

    task_size = 500_000
    num_tasks = 8
    tasks = [task_size] * num_tasks

    cpu_count = mp.cpu_count()
    print(f"\n사용 가능한 CPU 코어: {cpu_count}")
    print("-" * 60)

    # 순차 처리 시간
    start = time.perf_counter()
    results = [cpu_bound_task(n) for n in tasks[:1]]
    single_time = time.perf_counter() - start

    print(f"\n단일 작업 시간: {single_time:.2f}초")
    print(f"이론적 순차 시간: {single_time * num_tasks:.2f}초")
    print("\n워커 수별 성능:")

    for workers in [1, 2, 4, 8]:
        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(cpu_bound_task, tasks))
        duration = time.perf_counter() - start

        speedup = (single_time * num_tasks) / duration
        efficiency = speedup / workers * 100

        print(f"  {workers}개 워커: {duration:.2f}초 "
              f"| 속도향상: {speedup:.2f}x "
              f"| 효율: {efficiency:.1f}%")


def array_processing_comparison():
    """대규모 배열 처리 비교"""
    print("\n" + "="*60)
    print("6. 대규모 배열 처리")
    print("="*60)

    # 큰 배열을 여러 청크로 나누어 처리
    array_size = 10_000_000
    num_chunks = 4

    data = np.arange(array_size)

    def process_chunk(chunk):
        """배열 청크 처리"""
        return np.sum(np.sqrt(np.abs(np.sin(chunk) * np.cos(chunk))))

    # NumPy 벡터화 (단일 스레드)
    start = time.perf_counter()
    result_numpy = np.sum(np.sqrt(np.abs(np.sin(data) * np.cos(data))))
    numpy_duration = time.perf_counter() - start

    # 멀티프로세싱
    chunks = np.array_split(data, num_chunks)
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=num_chunks) as executor:
        results = list(executor.map(process_chunk, chunks))
    result_parallel = sum(results)
    parallel_duration = time.perf_counter() - start

    print(f"\n배열 크기: {array_size:,} 원소")
    print(f"청크 수: {num_chunks}")
    print(f"\nNumPy (단일 스레드): {numpy_duration:.3f}초")
    print(f"멀티프로세싱: {parallel_duration:.3f}초")

    if parallel_duration < numpy_duration:
        print(f"속도 향상: {numpy_duration/parallel_duration:.2f}x")
    else:
        print(f"⚠️  이 경우 오버헤드로 인해 느림 (비율: {parallel_duration/numpy_duration:.2f}x)")

    print(f"\n결과 검증: {abs(result_numpy - result_parallel) < 1e-6}")
    print("\n💡 작은 작업에는 멀티프로세싱 오버헤드가 이득을 상쇄할 수 있음")


def demonstrate_shared_memory():
    """공유 메모리 사용 예제"""
    print("\n" + "="*60)
    print("7. 공유 메모리 (Python 3.8+)")
    print("="*60)

    try:
        from multiprocessing import shared_memory

        # 공유 메모리 생성
        size = 1_000_000
        shm = shared_memory.SharedMemory(create=True, size=size * 8)  # 8 bytes per float64

        # NumPy 배열로 공유 메모리 사용
        shared_array = np.ndarray((size,), dtype=np.float64, buffer=shm.buf)
        shared_array[:] = np.arange(size)

        print(f"✓ 공유 메모리 생성: {size:,} 원소")
        print(f"  메모리 크기: {size * 8 / (1024**2):.2f} MB")
        print(f"  메모리 이름: {shm.name}")

        # 정리
        shm.close()
        shm.unlink()

        print("\n💡 공유 메모리를 사용하면 프로세스 간 데이터 복사 오버헤드 제거")

    except ImportError:
        print("⚠️  Python 3.8+ 필요 (shared_memory)")


def main():
    print("="*60)
    print("병렬 처리 기본 개념")
    print("="*60)

    # CPU 작업 비교
    seq_time = sequential_processing()
    thread_time = thread_based_processing()
    process_time = process_based_processing()

    print("\n" + "="*60)
    print("CPU 작업 성능 요약")
    print("="*60)
    print(f"순차 처리:        {seq_time:.2f}초 (1.00x)")
    print(f"멀티스레드:       {thread_time:.2f}초 ({seq_time/thread_time:.2f}x)")
    print(f"멀티프로세스:     {process_time:.2f}초 ({seq_time/process_time:.2f}x)")

    # I/O 작업
    io_bound_comparison()

    # 확장성
    demonstrate_scaling()

    # 배열 처리
    array_processing_comparison()

    # 공유 메모리
    demonstrate_shared_memory()

    print("\n" + "="*60)
    print("핵심 개념 정리")
    print("="*60)
    print("""
1. GIL (Global Interpreter Lock)
   - Python의 스레드는 GIL로 인해 CPU 작업에서 병렬 실행 안됨
   - I/O 작업에서는 GIL이 해제되어 스레드가 효과적

2. 멀티프로세싱
   - 각 프로세스는 독립적인 Python 인터프리터
   - CPU 작업에서 진정한 병렬 처리 가능
   - 메모리 오버헤드와 프로세스 간 통신 비용 있음

3. 적절한 선택
   - CPU 집약적: multiprocessing 또는 ProcessPoolExecutor
   - I/O 집약적: threading 또는 ThreadPoolExecutor
   - 간단한 병렬화: concurrent.futures 사용
   - 복잡한 제어: multiprocessing 사용

4. 성능 고려사항
   - 작업 크기: 너무 작으면 오버헤드가 이득을 상쇄
   - 워커 수: CPU 코어 수와 작업 특성 고려
   - 메모리: 프로세스는 메모리 복사, 공유 메모리로 최적화 가능

다음 단계: 03_multiprocessing_advanced.py
""")


if __name__ == "__main__":
    main()

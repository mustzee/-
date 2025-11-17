#!/usr/bin/env python3
"""
고급 멀티프로세싱 기법
Pool, Queue, 공유 메모리, 그리고 실전 예제
"""

import time
import multiprocessing as mp
from multiprocessing import Pool, Queue, Process, Manager, shared_memory
import numpy as np
from typing import List, Tuple
import os


def monte_carlo_pi(num_samples: int) -> Tuple[int, int]:
    """몬테카를로 방법으로 π 추정 (워커 함수)"""
    np.random.seed()  # 각 프로세스마다 다른 시드
    x = np.random.random(num_samples)
    y = np.random.random(num_samples)
    inside_circle = np.sum(x**2 + y**2 <= 1.0)
    return inside_circle, num_samples


def parallel_monte_carlo():
    """병렬 몬테카를로 시뮬레이션"""
    print("\n" + "="*60)
    print("1. 몬테카를로 시뮬레이션 (π 추정)")
    print("="*60)

    total_samples = 100_000_000
    num_workers = mp.cpu_count()
    samples_per_worker = total_samples // num_workers

    print(f"\n총 샘플: {total_samples:,}")
    print(f"워커 수: {num_workers}")
    print(f"워커당 샘플: {samples_per_worker:,}")

    # 병렬 실행
    start = time.perf_counter()
    with Pool(processes=num_workers) as pool:
        results = pool.map(monte_carlo_pi, [samples_per_worker] * num_workers)

    total_inside = sum(r[0] for r in results)
    total_samples_actual = sum(r[1] for r in results)
    pi_estimate = 4 * total_inside / total_samples_actual

    duration = time.perf_counter() - start

    print(f"\n처리 시간: {duration:.2f}초")
    print(f"π 추정값: {pi_estimate:.6f}")
    print(f"실제 π: {np.pi:.6f}")
    print(f"오차: {abs(pi_estimate - np.pi):.6f}")
    print(f"처리 속도: {total_samples / duration / 1e6:.2f}M 샘플/초")


def image_filter_worker(args: Tuple[np.ndarray, int, int]) -> Tuple[int, np.ndarray]:
    """이미지 필터 적용 워커"""
    image, blur_size, worker_id = args

    # 간단한 박스 블러 필터
    height, width = image.shape
    result = np.zeros_like(image)

    half_size = blur_size // 2

    for i in range(height):
        for j in range(width):
            i_min = max(0, i - half_size)
            i_max = min(height, i + half_size + 1)
            j_min = max(0, j - half_size)
            j_max = min(width, j + half_size + 1)

            result[i, j] = np.mean(image[i_min:i_max, j_min:j_max])

    return worker_id, result


def parallel_image_processing():
    """병렬 이미지 처리"""
    print("\n" + "="*60)
    print("2. 병렬 이미지 처리")
    print("="*60)

    # 가상 이미지 생성
    num_images = 8
    img_size = (200, 200)
    images = [np.random.rand(*img_size) for _ in range(num_images)]

    blur_size = 5
    num_workers = min(mp.cpu_count(), num_images)

    print(f"\n이미지 수: {num_images}")
    print(f"이미지 크기: {img_size}")
    print(f"블러 크기: {blur_size}x{blur_size}")
    print(f"워커 수: {num_workers}")

    # 순차 처리
    start = time.perf_counter()
    seq_results = []
    for i, img in enumerate(images):
        _, result = image_filter_worker((img, blur_size, i))
        seq_results.append(result)
    seq_duration = time.perf_counter() - start

    # 병렬 처리
    start = time.perf_counter()
    with Pool(processes=num_workers) as pool:
        results = pool.map(image_filter_worker,
                          [(img, blur_size, i) for i, img in enumerate(images)])

    # 결과 정렬
    par_results = [r[1] for r in sorted(results, key=lambda x: x[0])]
    par_duration = time.perf_counter() - start

    print(f"\n순차 처리: {seq_duration:.2f}초")
    print(f"병렬 처리: {par_duration:.2f}초")
    print(f"속도 향상: {seq_duration/par_duration:.2f}x")

    # 결과 검증
    for seq, par in zip(seq_results, par_results):
        assert np.allclose(seq, par), "결과 불일치!"
    print("✓ 결과 검증 완료")


def producer_consumer_demo():
    """Producer-Consumer 패턴"""
    print("\n" + "="*60)
    print("3. Producer-Consumer 패턴")
    print("="*60)

    def producer(queue: Queue, num_items: int):
        """데이터 생성자"""
        for i in range(num_items):
            # 복잡한 계산 시뮬레이션
            data = np.random.randn(1000, 1000)
            result = np.linalg.svd(data, compute_uv=False)
            queue.put((i, result))
            if (i + 1) % 5 == 0:
                print(f"  Producer: {i+1} 항목 생성")

        # 종료 신호
        queue.put(None)

    def consumer(queue: Queue, consumer_id: int):
        """데이터 소비자"""
        count = 0
        while True:
            item = queue.get()
            if item is None:
                # 다른 소비자를 위해 종료 신호 다시 넣기
                queue.put(None)
                break

            idx, data = item
            # 데이터 처리
            result = np.mean(data)
            count += 1

        print(f"  Consumer {consumer_id}: {count} 항목 처리 완료")

    # 큐 생성
    queue = Queue(maxsize=5)  # 버퍼 크기 제한

    num_items = 20
    num_consumers = 3

    print(f"\n생성 항목: {num_items}")
    print(f"소비자 수: {num_consumers}")
    print(f"큐 크기: 5\n")

    start = time.perf_counter()

    # 프로세스 시작
    prod = Process(target=producer, args=(queue, num_items))
    consumers = [Process(target=consumer, args=(queue, i))
                 for i in range(num_consumers)]

    prod.start()
    for c in consumers:
        c.start()

    # 종료 대기
    prod.join()
    for c in consumers:
        c.join()

    duration = time.perf_counter() - start

    print(f"\n총 처리 시간: {duration:.2f}초")
    print("✓ 모든 프로세스 완료")


def shared_memory_processing():
    """공유 메모리를 사용한 대규모 배열 처리"""
    print("\n" + "="*60)
    print("4. 공유 메모리 고급 사용")
    print("="*60)

    try:
        # 큰 배열 생성
        size = 10_000_000
        data = np.arange(size, dtype=np.float64)

        # 공유 메모리에 배열 저장
        shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
        shared_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
        shared_array[:] = data[:]

        def process_shared_chunk(args):
            """공유 메모리의 청크 처리"""
            shm_name, shape, dtype, start_idx, end_idx = args

            # 기존 공유 메모리 연결
            shm = shared_memory.SharedMemory(name=shm_name)
            array = np.ndarray(shape, dtype=dtype, buffer=shm.buf)

            # 청크 처리
            chunk = array[start_idx:end_idx]
            result = np.sum(np.sqrt(np.abs(np.sin(chunk) * np.cos(chunk))))

            shm.close()
            return result

        # 청크 분할
        num_workers = mp.cpu_count()
        chunk_size = size // num_workers
        chunks = [
            (shm.name, data.shape, data.dtype, i * chunk_size,
             (i + 1) * chunk_size if i < num_workers - 1 else size)
            for i in range(num_workers)
        ]

        print(f"\n배열 크기: {size:,} 원소")
        print(f"메모리 사용: {data.nbytes / (1024**2):.2f} MB")
        print(f"워커 수: {num_workers}")
        print(f"청크 크기: ~{chunk_size:,} 원소")

        # 병렬 처리
        start = time.perf_counter()
        with Pool(processes=num_workers) as pool:
            results = pool.map(process_shared_chunk, chunks)

        total_result = sum(results)
        duration = time.perf_counter() - start

        print(f"\n처리 시간: {duration:.3f}초")
        print(f"결과: {total_result:.2f}")
        print("✓ 공유 메모리로 데이터 복사 오버헤드 제거")

        # 정리
        shm.close()
        shm.unlink()

    except Exception as e:
        print(f"⚠️  공유 메모리 오류: {e}")


def matrix_multiplication_parallel():
    """병렬 행렬 곱셈"""
    print("\n" + "="*60)
    print("5. 병렬 행렬 곱셈")
    print("="*60)

    def multiply_row_block(args):
        """행 블록 곱셈"""
        A_block, B, start_row = args
        return start_row, np.dot(A_block, B)

    size = 2000
    A = np.random.randn(size, size)
    B = np.random.randn(size, size)

    print(f"\n행렬 크기: {size}x{size}")

    # NumPy (단일 스레드, 하지만 BLAS 사용)
    start = time.perf_counter()
    C_numpy = np.dot(A, B)
    numpy_duration = time.perf_counter() - start

    # 수동 병렬화 (행 블록 분할)
    num_workers = mp.cpu_count()
    rows_per_worker = size // num_workers

    blocks = [
        (A[i*rows_per_worker:(i+1)*rows_per_worker if i < num_workers-1 else size],
         B, i*rows_per_worker)
        for i in range(num_workers)
    ]

    start = time.perf_counter()
    with Pool(processes=num_workers) as pool:
        results = pool.map(multiply_row_block, blocks)

    # 결과 조합
    C_parallel = np.vstack([r[1] for r in sorted(results, key=lambda x: x[0])])
    parallel_duration = time.perf_counter() - start

    print(f"\nNumPy (BLAS): {numpy_duration:.3f}초")
    print(f"병렬화: {parallel_duration:.3f}초")

    # NumPy는 최적화된 BLAS를 사용하므로 보통 더 빠름
    print("\n💡 NumPy는 최적화된 BLAS를 사용하므로 보통 수동 병렬화보다 빠릅니다")
    print("   하지만 이 예제는 병렬화 기법을 보여줍니다")

    # 결과 검증
    assert np.allclose(C_numpy, C_parallel), "결과 불일치!"
    print("✓ 결과 검증 완료")


def demonstrate_pool_methods():
    """Pool의 다양한 메서드"""
    print("\n" + "="*60)
    print("6. Pool 메서드 비교")
    print("="*60)

    def square(x):
        return x * x

    data = list(range(20))

    print("\n1) map() - 순서 보장")
    with Pool(processes=4) as pool:
        results = pool.map(square, data)
    print(f"   결과: {results[:10]}...")

    print("\n2) imap() - 이터레이터 반환 (메모리 효율적)")
    with Pool(processes=4) as pool:
        results = list(pool.imap(square, data))
    print(f"   결과: {results[:10]}...")

    print("\n3) imap_unordered() - 순서 무관, 더 빠름")
    with Pool(processes=4) as pool:
        results = list(pool.imap_unordered(square, data))
    print(f"   결과: {results[:10]}...")

    print("\n4) starmap() - 여러 인자 전달")
    def power(base, exp):
        return base ** exp

    args = [(2, 3), (3, 2), (4, 2), (5, 2)]
    with Pool(processes=4) as pool:
        results = pool.starmap(power, args)
    print(f"   결과: {results}")

    print("\n5) apply_async() - 비동기 실행")
    with Pool(processes=4) as pool:
        async_results = [pool.apply_async(square, (i,)) for i in range(10)]
        results = [r.get() for r in async_results]
    print(f"   결과: {results}")


def error_handling_demo():
    """에러 처리"""
    print("\n" + "="*60)
    print("7. 에러 처리")
    print("="*60)

    def risky_function(x):
        if x == 5:
            raise ValueError(f"5는 처리할 수 없습니다!")
        return x * 2

    data = list(range(10))

    print("\n에러 발생 시나리오:")
    try:
        with Pool(processes=4) as pool:
            results = pool.map(risky_function, data)
    except ValueError as e:
        print(f"  ✗ 에러 발생: {e}")

    print("\n에러 무시하고 계속:")
    def safe_function(x):
        try:
            return risky_function(x)
        except ValueError:
            return None

    with Pool(processes=4) as pool:
        results = pool.map(safe_function, data)
    print(f"  결과: {results}")
    print(f"  성공: {sum(1 for r in results if r is not None)}/{len(results)}")


def main():
    print("="*60)
    print("고급 멀티프로세싱 기법")
    print("="*60)
    print(f"\nCPU 코어: {mp.cpu_count()}")

    # 1. 몬테카를로
    parallel_monte_carlo()

    # 2. 이미지 처리
    parallel_image_processing()

    # 3. Producer-Consumer
    producer_consumer_demo()

    # 4. 공유 메모리
    shared_memory_processing()

    # 5. 행렬 곱셈
    matrix_multiplication_parallel()

    # 6. Pool 메서드
    demonstrate_pool_methods()

    # 7. 에러 처리
    error_handling_demo()

    print("\n" + "="*60)
    print("핵심 포인트")
    print("="*60)
    print("""
1. Pool 사용
   - map(): 간단하고 순서 보장
   - imap(): 메모리 효율적
   - imap_unordered(): 최대 성능
   - starmap(): 여러 인자 전달

2. 통신 패턴
   - Queue: Producer-Consumer
   - Pipe: 양방향 통신
   - Manager: 공유 객체

3. 공유 메모리
   - 대규모 데이터 복사 오버헤드 제거
   - Python 3.8+ 필수
   - 수동 동기화 필요

4. 최적화 팁
   - 작업 크기 조정 (너무 작으면 오버헤드)
   - 적절한 워커 수 (보통 CPU 코어 수)
   - 데이터 직렬화 비용 고려

5. 주의사항
   - 프로세스 생성 비용
   - 데이터 직렬화 (pickle) 오버헤드
   - 메모리 사용량 증가

다음 단계: Julia, Rust, C++ 예제 살펴보기
""")


if __name__ == "__main__":
    main()

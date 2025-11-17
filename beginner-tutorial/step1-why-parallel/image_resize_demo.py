#!/usr/bin/env python3
"""
실전 예제: 이미지 크기 변경 시뮬레이션
실제 이미지 대신 계산으로 시뮬레이션합니다.
"""

import time
import random
from concurrent.futures import ProcessPoolExecutor
import os


def resize_image(image_id):
    """
    이미지 크기를 변경하는 함수 (시뮬레이션)
    실제로는 복잡한 이미지 처리를 수행
    """
    # 이미지 처리 시뮬레이션 (50~100ms)
    processing_time = random.uniform(0.05, 0.1)
    time.sleep(processing_time)
    return f"image_{image_id}_resized.jpg"


def print_progress(current, total, start_time):
    """진행률 표시"""
    progress = current / total
    bar_length = 20
    filled = int(bar_length * progress)
    bar = "█" * filled + "░" * (bar_length - filled)
    elapsed = time.time() - start_time

    print(f"\r진행: [{bar}] {current}/{total} ({progress*100:.0f}%) - {elapsed:.1f}초",
          end='', flush=True)


def sequential_processing(num_images):
    """순차 처리"""
    print("\n[순차 처리]")
    start_time = time.time()

    results = []
    for i in range(num_images):
        result = resize_image(i)
        results.append(result)
        if (i + 1) % 50 == 0 or i == num_images - 1:
            print_progress(i + 1, num_images, start_time)

    duration = time.time() - start_time
    print(f"\n시간: {duration:.1f}초")
    return duration, results


def parallel_processing(num_images, num_workers):
    """병렬 처리"""
    print(f"\n[병렬 처리 - {num_workers}코어]")
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = []
        for i, result in enumerate(executor.map(resize_image, range(num_images))):
            results.append(result)
            if (i + 1) % 50 == 0 or i == num_images - 1:
                print_progress(i + 1, num_images, start_time)

    duration = time.time() - start_time
    print(f"\n시간: {duration:.1f}초")
    return duration, results


def main():
    print("="*60)
    print("이미지 크기 변경 시뮬레이션")
    print("="*60)

    # 설정
    num_images = 1000
    num_workers = min(os.cpu_count(), 8)

    print(f"처리할 이미지: {num_images}장")
    print(f"사용 가능한 CPU 코어: {os.cpu_count()}개")
    print(f"사용할 워커: {num_workers}개")

    # 순차 처리
    seq_duration, seq_results = sequential_processing(num_images)

    # 병렬 처리
    par_duration, par_results = parallel_processing(num_images, num_workers)

    # 결과 비교
    print("\n" + "="*60)
    print("📊 결과 비교")
    print("="*60)

    speedup = seq_duration / par_duration
    time_saved = seq_duration - par_duration

    print(f"\n순차 처리: {seq_duration:.1f}초")
    print(f"병렬 처리: {par_duration:.1f}초")
    print(f"\n속도 향상: {speedup:.1f}배! 🚀")
    print(f"절약된 시간: {time_saved:.1f}초")

    # 실제 상황 비유
    print("\n💡 실생활로 비유하면:")
    if seq_duration < 60:
        seq_str = f"{seq_duration:.0f}초"
    else:
        seq_str = f"{seq_duration/60:.1f}분"

    if par_duration < 60:
        par_str = f"{par_duration:.0f}초"
    else:
        par_str = f"{par_duration/60:.1f}분"

    print(f"   순차 처리: 커피 마시고 올 시간 ({seq_str})")
    print(f"   병렬 처리: 바로 완료! ({par_str})")

    # 효율성
    efficiency = (speedup / num_workers) * 100
    print(f"\n⚙️  병렬화 효율: {efficiency:.1f}%")
    if efficiency > 80:
        print("   → 매우 효율적!")
    elif efficiency > 60:
        print("   → 양호")
    else:
        print("   → 개선 여지 있음")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()

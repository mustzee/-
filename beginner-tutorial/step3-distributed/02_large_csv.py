#!/usr/bin/env python3
"""
대용량 CSV 처리: 메모리보다 큰 데이터 다루기
"""

import dask.dataframe as dd
import pandas as pd
import numpy as np
import os
import time


def generate_large_csv(num_files=10, rows_per_file=100_000):
    """대용량 CSV 파일 생성 (시뮬레이션)"""
    print(f"📝 샘플 CSV 파일 생성 중...")
    print(f"   파일 수: {num_files}")
    print(f"   파일당 rows: {rows_per_file:,}")

    total_rows = num_files * rows_per_file
    total_size_mb = (total_rows * 50) / (1024 * 1024)  # 대략적인 크기

    print(f"   총 rows: {total_rows:,}")
    print(f"   예상 크기: ~{total_size_mb:.0f} MB\n")

    os.makedirs('data', exist_ok=True)

    for i in range(num_files):
        filename = f'data/data_{i:03d}.csv'
        data = {
            'id': range(i * rows_per_file, (i + 1) * rows_per_file),
            'value1': np.random.randn(rows_per_file),
            'value2': np.random.randn(rows_per_file),
            'category': np.random.choice(['A', 'B', 'C', 'D'], rows_per_file),
            'timestamp': pd.date_range('2024-01-01', periods=rows_per_file, freq='1min')
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

        if (i + 1) % 3 == 0:
            print(f"   진행: {i+1}/{num_files} 파일 생성...")

    print(f"✅ 파일 생성 완료!\n")
    return num_files


def process_with_pandas():
    """Pandas로 처리 (메모리 제한 있음)"""
    print("="*60)
    print("1️⃣ Pandas로 처리 (모든 파일 합치기)")
    print("="*60)

    try:
        start = time.time()

        # 모든 CSV 읽기
        files = [f'data/data_{i:03d}.csv' for i in range(10)]
        df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

        # 처리
        result = df.groupby('category').agg({
            'value1': 'mean',
            'value2': 'sum',
            'id': 'count'
        })

        duration = time.time() - start

        print(f"\n✅ 완료!")
        print(f"   시간: {duration:.2f}초")
        print(f"   메모리: 모든 데이터 로드 (높음)")
        print(f"\n결과:\n{result}\n")

        return duration

    except MemoryError:
        print("❌ 메모리 부족! Pandas로는 처리 불가")
        return None


def process_with_dask():
    """Dask로 처리 (메모리 효율적)"""
    print("="*60)
    print("2️⃣ Dask로 처리 (청크 단위)")
    print("="*60)

    start = time.time()

    # 모든 CSV 읽기 (와일드카드 사용)
    df = dd.read_csv('data/data_*.csv')

    print(f"   파일 발견: {df.npartitions}개 파티션")
    print(f"   메모리: 필요한 부분만 로드 (낮음)")

    # 처리 (Lazy)
    result_lazy = df.groupby('category').agg({
        'value1': 'mean',
        'value2': 'sum',
        'id': 'count'
    })

    # 실제 계산
    result = result_lazy.compute()

    duration = time.time() - start

    print(f"\n✅ 완료!")
    print(f"   시간: {duration:.2f}초")
    print(f"\n결과:\n{result}\n")

    return duration


def cleanup():
    """임시 파일 정리"""
    import shutil
    if os.path.exists('data'):
        shutil.rmtree('data')
        print("🗑️  임시 파일 정리 완료")


def main():
    print("="*60)
    print("대용량 CSV 파일 처리")
    print("="*60)
    print()

    # 1. 파일 생성
    num_files = generate_large_csv(num_files=10, rows_per_file=50_000)

    # 2. Pandas 처리
    pandas_time = process_with_pandas()

    # 3. Dask 처리
    dask_time = process_with_dask()

    # 4. 비교
    if pandas_time and dask_time:
        print("="*60)
        print("📊 성능 비교")
        print("="*60)
        print(f"Pandas: {pandas_time:.2f}초")
        print(f"Dask:   {dask_time:.2f}초")

        if dask_time < pandas_time:
            print(f"\n💡 Dask가 {pandas_time/dask_time:.1f}배 효율적!")
        else:
            print(f"\n💡 작은 데이터에서는 Pandas가 더 빠를 수 있음")

    print("\n" + "="*60)
    print("핵심 포인트")
    print("="*60)
    print("""
1. Pandas: 모든 데이터를 메모리에
   → 작은 데이터에 적합

2. Dask: 필요한 부분만 메모리에
   → 대용량 데이터에 적합

3. 와일드카드 사용: 'data_*.csv'
   → 여러 파일을 한 번에!

4. 메모리가 부족하면 Dask 사용!
""")

    # 정리
    cleanup()


if __name__ == "__main__":
    main()

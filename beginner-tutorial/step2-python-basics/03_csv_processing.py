#!/usr/bin/env python3
"""
실전: CSV 파일 병렬 처리
"""

import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
import time
import os


def generate_sample_csv(filename, num_rows=100_000):
    """샘플 CSV 파일 생성"""
    print(f"📝 샘플 데이터 생성 중... ({num_rows:,} rows)")

    data = {
        'id': range(num_rows),
        'value1': np.random.randn(num_rows),
        'value2': np.random.randn(num_rows),
        'category': np.random.choice(['A', 'B', 'C'], num_rows)
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ 파일 생성: {filename}\n")
    return filename


def process_chunk(chunk_data):
    """데이터 청크 처리"""
    # 예: 복잡한 계산 수행
    chunk = chunk_data
    chunk['result'] = np.sqrt(chunk['value1']**2 + chunk['value2']**2)
    chunk['score'] = chunk['result'] * 100
    return chunk


def main():
    print("="*60)
    print("CSV 파일 병렬 처리")
    print("="*60)

    # 샘플 파일 생성
    filename = 'sample_data.csv'
    if not os.path.exists(filename):
        generate_sample_csv(filename, 100_000)

    # 파일 읽기
    print("📖 파일 읽기...")
    df = pd.read_csv(filename)
    print(f"   데이터: {len(df):,} rows × {len(df.columns)} columns\n")

    # 1. 순차 처리
    print("1️⃣ 순차 처리")
    start = time.time()
    result_seq = process_chunk(df.copy())
    seq_time = time.time() - start
    print(f"   시간: {seq_time:.2f}초\n")

    # 2. 병렬 처리
    print("2️⃣ 병렬 처리")
    num_workers = cpu_count()
    chunks = np.array_split(df, num_workers)

    start = time.time()
    with Pool(processes=num_workers) as pool:
        results = pool.map(process_chunk, chunks)
    result_par = pd.concat(results, ignore_index=True)
    par_time = time.time() - start
    print(f"   시간: {par_time:.2f}초\n")

    # 결과
    print("="*60)
    print("📊 결과")
    print("="*60)
    print(f"속도 향상: {seq_time/par_time:.1f}배")
    print(f"처리된 rows: {len(result_par):,}")
    print(f"\n💡 대용량 데이터는 청크로 나눠 병렬 처리!")

    # 정리
    if os.path.exists(filename):
        os.remove(filename)
        print(f"\n🗑️  임시 파일 삭제: {filename}")


if __name__ == "__main__":
    main()

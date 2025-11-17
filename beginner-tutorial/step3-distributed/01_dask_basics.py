#!/usr/bin/env python3
"""
Dask 기초: Lazy Evaluation의 힘
"""

import dask.dataframe as dd
import pandas as pd
import numpy as np
import time


def main():
    print("="*60)
    print("Dask 기초: Lazy Evaluation")
    print("="*60)

    # 1. 샘플 데이터 생성
    print("\n📝 샘플 데이터 생성 (100,000 rows)")
    data = {
        'x': np.random.rand(100_000),
        'y': np.random.rand(100_000),
        'category': np.random.choice(['A', 'B', 'C'], 100_000)
    }

    # Pandas DataFrame
    df_pandas = pd.DataFrame(data)

    # Dask DataFrame (from pandas)
    df_dask = dd.from_pandas(df_pandas, npartitions=4)

    print(f"✅ Pandas DataFrame: {len(df_pandas):,} rows")
    print(f"✅ Dask DataFrame: {df_dask.npartitions} partitions\n")

    # 2. Lazy Evaluation 체험
    print("="*60)
    print("🔍 Lazy Evaluation 체험")
    print("="*60)

    # Pandas: 즉시 실행
    print("\n1️⃣ Pandas (즉시 실행)")
    start = time.time()
    result_pandas = df_pandas[df_pandas['x'] > 0.5].groupby('category')['y'].mean()
    pandas_time = time.time() - start
    print(f"   결과: {dict(result_pandas)}")
    print(f"   시간: {pandas_time:.4f}초\n")

    # Dask: Lazy (정의만)
    print("2️⃣ Dask (Lazy - 아직 계산 안함)")
    start = time.time()
    result_dask_lazy = df_dask[df_dask['x'] > 0.5].groupby('category')['y'].mean()
    lazy_time = time.time() - start
    print(f"   타입: {type(result_dask_lazy)}")
    print(f"   시간: {lazy_time:.4f}초 (거의 0초!)")
    print("   💡 아직 계산을 하지 않았습니다!\n")

    # Dask: Compute (실제 실행)
    print("3️⃣ Dask (.compute() - 실제 계산)")
    start = time.time()
    result_dask = result_dask_lazy.compute()
    compute_time = time.time() - start
    print(f"   결과: {dict(result_dask)}")
    print(f"   시간: {compute_time:.4f}초\n")

    # 3. 장점: 최적화
    print("="*60)
    print("💡 Dask의 장점: 자동 최적화")
    print("="*60)
    print("""
Dask는 계산을 미루다가 .compute()할 때:
1. 작업 그래프 분석
2. 불필요한 계산 제거
3. 병렬로 실행
4. 메모리 효율적으로 처리

결과: 큰 데이터에서 훨씬 효율적!
""")

    # 4. Partitions (청크) 이해
    print("="*60)
    print("🧩 Partitions (청크)")
    print("="*60)
    print(f"\nDask DataFrame은 {df_dask.npartitions}개 조각으로 나뉨:")
    for i in range(df_dask.npartitions):
        partition = df_dask.get_partition(i).compute()
        print(f"   Partition {i}: {len(partition):,} rows")

    print("\n💡 각 조각은 병렬로 처리됩니다!")

    # 5. 메모리 효율성
    print("\n" + "="*60)
    print("💾 메모리 효율성")
    print("="*60)
    print("""
Pandas: 전체 데이터를 메모리에 로드
Dask: 필요한 조각만 로드

큰 데이터일수록 Dask가 유리!
""")

    print("="*60)
    print("✅ Dask 기초 완료!")
    print("="*60)


if __name__ == "__main__":
    main()

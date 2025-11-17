#!/usr/bin/env python3
"""
병렬 데이터 분석: 실전 시나리오
"""

import dask.dataframe as dd
import pandas as pd
import numpy as np
import time
from dask.diagnostics import ProgressBar


def generate_sales_data(num_rows=500_000):
    """판매 데이터 생성"""
    print("📝 판매 데이터 생성 중...")

    np.random.seed(42)

    data = {
        'date': pd.date_range('2023-01-01', periods=num_rows, freq='1min'),
        'product': np.random.choice(['A', 'B', 'C', 'D', 'E'], num_rows),
        'region': np.random.choice(['North', 'South', 'East', 'West'], num_rows),
        'quantity': np.random.randint(1, 100, num_rows),
        'price': np.random.uniform(10, 1000, num_rows)
    }

    df = pd.DataFrame(data)
    df['revenue'] = df['quantity'] * df['price']

    print(f"✅ 데이터 생성: {len(df):,} rows\n")
    return df


def analyze_with_dask(df):
    """Dask로 병렬 분석"""
    print("="*60)
    print("🔍 Dask 병렬 분석")
    print("="*60)

    # Pandas를 Dask로 변환
    ddf = dd.from_pandas(df, npartitions=8)

    print(f"파티션 수: {ddf.npartitions}\n")

    # ProgressBar 사용
    with ProgressBar():
        print("1️⃣ 제품별 총 매출")
        start = time.time()
        product_revenue = ddf.groupby('product')['revenue'].sum().compute()
        t1 = time.time() - start
        print(f"   완료! ({t1:.2f}초)")
        print(product_revenue.sort_values(ascending=False))

        print("\n2️⃣ 지역별 평균 거래액")
        start = time.time()
        region_avg = ddf.groupby('region')['revenue'].mean().compute()
        t2 = time.time() - start
        print(f"   완료! ({t2:.2f}초)")
        print(region_avg.sort_values(ascending=False))

        print("\n3️⃣ 일별 총 매출")
        start = time.time()
        ddf['date_only'] = ddf['date'].dt.date
        daily_revenue = ddf.groupby('date_only')['revenue'].sum().compute()
        t3 = time.time() - start
        print(f"   완료! ({t3:.2f}초)")
        print(f"   처음 5일:\n{daily_revenue.head()}")

        print("\n4️⃣ 복잡한 집계")
        start = time.time()
        complex_agg = ddf.groupby(['product', 'region']).agg({
            'quantity': ['sum', 'mean'],
            'revenue': ['sum', 'mean', 'max']
        }).compute()
        t4 = time.time() - start
        print(f"   완료! ({t4:.2f}초)")
        print(f"   결과 크기: {complex_agg.shape}")

    total_time = t1 + t2 + t3 + t4

    print(f"\n총 분석 시간: {total_time:.2f}초")

    return total_time


def main():
    print("="*60)
    print("실전 병렬 데이터 분석")
    print("="*60)
    print()

    # 데이터 생성
    df = generate_sales_data(num_rows=500_000)

    # Dask 분석
    dask_time = analyze_with_dask(df)

    # 결과
    print("\n" + "="*60)
    print("💡 핵심 포인트")
    print("="*60)
    print(f"""
1. ProgressBar로 진행 상황 확인
2. 여러 집계를 병렬로 처리
3. 복잡한 그룹화도 가능
4. 총 {dask_time:.2f}초에 500,000 rows 분석!

Dask는 다음과 같은 경우에 특히 유용합니다:
- 메모리보다 큰 데이터
- 여러 파일에 분산된 데이터
- 반복적인 대용량 분석
""")


if __name__ == "__main__":
    main()

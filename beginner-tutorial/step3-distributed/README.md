# Step 3: 대용량 분산처리 with Dask 🌐

**소요 시간**: 1시간 30분
**난이도**: ⭐⭐⭐ (중간)

## 🎯 이번 단계의 목표

- 메모리보다 큰 데이터 처리하기
- Dask로 분산 컴퓨팅 체험
- 실전 대용량 데이터 분석
- 클러스터 개념 이해 (선택)

---

## 🤔 왜 Dask가 필요할까?

### 문제 상황

```
내 컴퓨터 메모리: 16 GB
처리할 데이터: 50 GB ❌

일반 pandas: 메모리 부족 에러!
```

### Dask의 해결책

```
✅ 데이터를 작은 조각으로 나눔
✅ 필요한 부분만 메모리에 로드
✅ 여러 컴퓨터로 분산 가능!
```

---

## 📚 Dask란?

### Pandas의 슈퍼파워 버전!

```python
# Pandas (작은 데이터)
import pandas as pd
df = pd.read_csv('small_data.csv')  # 메모리에 전체 로드

# Dask (큰 데이터)
import dask.dataframe as dd
df = dd.read_csv('huge_data.csv')  # 필요할 때만 로드!
```

### 핵심 개념

1. **Lazy Evaluation**: 필요할 때만 계산
2. **Chunking**: 데이터를 작은 조각으로
3. **Distributed**: 여러 컴퓨터에서 실행 가능

---

## 🔬 실습 1: Dask 기초

```bash
python3 01_dask_basics.py
```

**배울 내용:**
- Dask DataFrame 생성
- Lazy evaluation 이해
- .compute() 실행

---

## 🔬 실습 2: 대용량 CSV 처리

```bash
python3 02_large_csv.py
```

**배울 내용:**
- 메모리보다 큰 파일 읽기
- 청크 단위 처리
- 결과 저장

**실행 결과 예시:**
```
생성할 데이터: 500 MB
메모리 사용: ~100 MB (청크 처리)
처리 시간: 15초
```

---

## 🔬 실습 3: 병렬 데이터 분석

```bash
python3 03_parallel_analytics.py
```

**배울 내용:**
- 그룹화 및 집계
- 병렬 통계 계산
- 시각화

---

## 🔬 실습 4: 분산 클러스터 (선택)

```bash
python3 04_distributed_cluster.py
```

**배울 내용:**
- 로컬 클러스터 설정
- 대시보드 사용
- 성능 모니터링

**대시보드:** http://localhost:8787

---

## 📊 성능 비교

| 방법 | 데이터 크기 | 메모리 사용 | 속도 |
|------|-----------|------------|------|
| Pandas | ~RAM | 100% | ⭐⭐⭐ |
| Dask (단일) | >> RAM | 20% | ⭐⭐⭐⭐ |
| Dask (클러스터) | >>> RAM | 분산 | ⭐⭐⭐⭐⭐ |

---

## 💡 Dask vs Pandas vs Multiprocessing

### Pandas
```python
# 🏠 작은 데이터 (< 메모리)
df = pd.read_csv('small.csv')
result = df.groupby('category').mean()
```

### Multiprocessing
```python
# ⚙️ CPU 집약적 작업
with Pool() as pool:
    results = pool.map(heavy_function, data)
```

### Dask
```python
# 🌐 대용량 데이터 (> 메모리)
df = dd.read_csv('huge.csv')
result = df.groupby('category').mean().compute()
```

---

## 🎯 실전 시나리오

### 시나리오 1: 로그 파일 분석 (10 GB)

```python
import dask.dataframe as dd

# 10GB 로그 파일 읽기
logs = dd.read_csv('server_logs_*.csv')

# 에러 필터링
errors = logs[logs['status'] == 'ERROR']

# 시간대별 집계
hourly = errors.groupby('hour').size().compute()

print(f"시간대별 에러: {hourly}")
```

### 시나리오 2: 센서 데이터 분석 (100 GB)

```python
# 100GB 센서 데이터
sensors = dd.read_parquet('sensors/*.parquet')

# 이상치 탐지
anomalies = sensors[sensors['value'] > threshold]

# 결과 저장
anomalies.to_csv('anomalies/*.csv')
```

---

## ⚠️ 주의사항

### Dask를 사용하지 마세요 (이럴 때)

1. **데이터가 작을 때** (< 1 GB)
   → Pandas가 더 빠름

2. **복잡한 조인이 많을 때**
   → 성능 저하 가능

3. **실시간 처리가 필요할 때**
   → Spark 고려

### Dask를 사용하세요 (이럴 때)

1. ✅ 메모리보다 큰 데이터
2. ✅ 병렬로 처리 가능한 작업
3. ✅ Pandas 코드를 조금만 수정

---

## ✅ 체크리스트

완료했다면 체크하세요:

- [ ] Dask DataFrame 기초 이해
- [ ] Lazy evaluation 개념 파악
- [ ] 대용량 CSV 처리 실습
- [ ] 병렬 분석 수행
- [ ] (선택) 분산 클러스터 체험
- [ ] Dask vs Pandas 차이 이해

---

## 🎓 배운 내용

- ✅ 메모리 제약 극복
- ✅ Dask DataFrame 사용법
- ✅ 청크 단위 처리
- ✅ 분산 컴퓨팅 개념
- ✅ 실전 데이터 분석

---

## 🚀 다음 단계

대용량 분산처리를 마스터했습니다!

👉 [Step 4: Rust 맛보기](../step4-rust-intro/README.md)에서 최고 성능을 경험해봅시다!

---

## 💡 더 알아보기

### Dask 에코시스템

- **Dask Array**: NumPy처럼 사용
- **Dask Bag**: 비정형 데이터
- **Dask ML**: 머신러닝
- **Dask Distributed**: 클러스터

### 실전 팁

1. **청크 크기 조정**
   ```python
   df = dd.read_csv('data.csv', blocksize='64MB')
   ```

2. **타입 명시로 속도 향상**
   ```python
   dtype = {'id': 'int64', 'value': 'float32'}
   df = dd.read_csv('data.csv', dtype=dtype)
   ```

3. **Parquet 사용**
   ```python
   # CSV보다 10배 빠름!
   df.to_parquet('data.parquet')
   ```

### 다른 도구들

- **Apache Spark**: 더 큰 규모
- **Ray**: 범용 분산 프레임워크
- **Vaex**: Out-of-core DataFrame

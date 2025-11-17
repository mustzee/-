# Step 2: Python 병렬처리 기초 🐍

**소요 시간**: 1시간
**난이도**: ⭐⭐ (쉬움)

## 🎯 이번 단계의 목표

- Python에서 병렬처리하는 3가지 방법 배우기
- 각 방법의 장단점 이해
- 실전 예제로 연습

---

## 📚 Python 병렬처리 3가지 방법

### 1. 🔢 NumPy (벡터화)
**언제?** 숫자 배열 계산
**속도:** ⭐⭐⭐⭐⭐
**난이도:** ⭐

### 2. 🧵 Threading (스레드)
**언제?** 파일 다운로드, 네트워크 요청
**속도:** ⭐⭐⭐
**난이도:** ⭐⭐

### 3. 🔄 Multiprocessing (프로세스)
**언제?** 무거운 계산 작업
**속도:** ⭐⭐⭐⭐⭐
**난이도:** ⭐⭐

---

## 실습 1: NumPy 벡터화

```bash
python3 01_numpy_vectorization.py
```

**배울 내용:**
- 일반 루프 vs NumPy
- 100배 빠른 계산
- 메모리 효율성

---

## 실습 2: Multiprocessing 기초

```bash
python3 02_multiprocessing_basics.py
```

**배울 내용:**
- Pool 사용법
- 데이터 분할 전략
- 결과 수집

---

## 실습 3: 실전 CSV 처리

```bash
python3 03_csv_processing.py
```

**배울 내용:**
- 대용량 CSV 읽기
- 병렬로 데이터 처리
- 결과 저장

---

## ✅ 체크리스트

- [ ] NumPy 벡터화 이해
- [ ] multiprocessing Pool 사용
- [ ] CSV 파일 병렬 처리
- [ ] 각 방법의 차이점 이해

---

## 🚀 다음 단계

Python 병렬처리의 기초를 마스터했습니다!

👉 [Step 3: 대용량 분산처리](../step3-distributed/README.md)에서 Dask를 배워봅시다!

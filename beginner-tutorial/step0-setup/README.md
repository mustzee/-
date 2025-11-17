# Step 0: 환경 설정 🔧

**소요 시간**: 15분
**난이도**: ⭐ (매우 쉬움)

## 🎯 이번 단계의 목표

- Python이 설치되어 있는지 확인
- 필요한 라이브러리 설치
- 첫 번째 프로그램 실행
- 내 컴퓨터의 CPU 정보 확인

---

## 1️⃣ Python 설치 확인

터미널(또는 명령 프롬프트)을 열고 다음 명령을 입력하세요:

```bash
python3 --version
```

또는

```bash
python --version
```

**기대 출력:**
```
Python 3.8.0 (또는 더 높은 버전)
```

### ❌ Python이 없다면?

**Mac/Linux:**
```bash
# Mac (Homebrew 사용)
brew install python3

# Ubuntu/Debian
sudo apt-get install python3 python3-pip
```

**Windows:**
1. [python.org](https://www.python.org/downloads/) 방문
2. "Download Python" 클릭
3. 설치 시 "Add Python to PATH" 체크!

---

## 2️⃣ 필요한 라이브러리 설치

이 튜토리얼에서 사용할 라이브러리들을 설치합니다:

```bash
pip install numpy pandas dask matplotlib psutil
```

**설치 확인:**
```bash
python3 check_installation.py
```

---

## 3️⃣ 첫 번째 프로그램 실행

`hello_parallel.py` 파일을 실행해봅시다:

```bash
python3 hello_parallel.py
```

**기대 출력:**
```
🎉 환영합니다! 병렬처리의 세계로!
💻 당신의 컴퓨터 정보:
   - CPU 코어 수: 8
   - 사용 가능한 메모리: 16.0 GB
   - 운영체제: Darwin (macOS)

✅ 모든 라이브러리가 정상적으로 설치되었습니다!
```

---

## 4️⃣ CPU 정보 확인하기

`cpu_info.py`를 실행하여 내 컴퓨터를 이해해봅시다:

```bash
python3 cpu_info.py
```

이 프로그램은 다음을 보여줍니다:
- CPU 코어 개수
- 각 코어의 사용률
- 메모리 정보

---

## 📝 실습: 코드 살펴보기

각 Python 파일을 텍스트 에디터로 열어서 코드를 읽어보세요.
지금은 다 이해하지 못해도 괜찮습니다!

**주의 깊게 볼 부분:**
- `import` 문: 어떤 라이브러리를 사용하는가?
- `print()` 문: 무엇을 출력하는가?
- 주석(`#`): 설명을 읽어보세요

---

## ✅ 체크리스트

완료했다면 체크하세요:

- [ ] Python 3.8 이상 설치 확인
- [ ] 필요한 라이브러리 설치 완료
- [ ] `hello_parallel.py` 정상 실행
- [ ] `cpu_info.py`로 CPU 정보 확인
- [ ] 내 컴퓨터의 CPU 코어 개수를 알게 됨

---

## 🐛 문제 해결

### "command not found" 에러
→ Python이 설치되지 않았거나 PATH에 없습니다. 위의 설치 가이드를 따라하세요.

### "No module named 'numpy'" 에러
→ 라이브러리 설치가 안 됐습니다. `pip install numpy` 실행

### 권한 에러 (Permission denied)
→ Mac/Linux: `sudo pip3 install ...` 시도
→ Windows: 관리자 권한으로 실행

---

## 🎓 배운 내용

- ✅ Python 환경 설정
- ✅ 라이브러리 설치 방법
- ✅ 내 컴퓨터의 CPU 정보
- ✅ 기본 Python 스크립트 실행

---

## 🚀 다음 단계

환경 설정이 끝났습니다!

👉 [Step 1: 왜 병렬처리가 필요할까?](../step1-why-parallel/README.md)로 이동하세요.

---

## 💡 추가 정보

### CPU 코어가 중요한 이유
- 코어 1개 = 작업자 1명
- 코어 8개 = 작업자 8명
- 병렬처리 = 여러 작업자가 동시에 일함
- 최대 속도 향상 ≈ 코어 개수

### 메모리가 중요한 이유
- 메모리 = 작업 공간
- 메모리보다 큰 데이터 = 디스크 사용 (느림)
- 분산처리 = 여러 컴퓨터의 메모리 합침

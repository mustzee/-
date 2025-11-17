# Step 4: Rust 맛보기 🦀

**소요 시간**: 1시간
**난이도**: ⭐⭐⭐ (중간)

## 🎯 이번 단계의 목표

- Rust가 무엇인지 이해
- 간단한 Rust 프로그램 실행
- Rayon으로 병렬처리 체험
- Python과 성능 비교

---

## 🤔 왜 Rust인가?

### 성능 비교

```
Python:    ████████████████████ (20초)
Python+MP: ████████             (8초)
Rust:      ██                   (2초)  🚀
```

### Rust의 강점

1. **C/C++ 수준의 속도**
2. **메모리 안전성** (컴파일러가 보장!)
3. **병렬처리가 쉬움** (Rayon)
4. **현대적인 도구** (Cargo)

---

## 🔧 Rust 설치 (15분)

### Mac/Linux

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Windows

1. [rustup.rs](https://rustup.rs) 방문
2. 설치 프로그램 다운로드
3. 실행

### 확인

```bash
rustc --version
cargo --version
```

**출력 예:**
```
rustc 1.75.0
cargo 1.75.0
```

---

## 🚀 실습 1: Hello Rust!

```bash
cd hello_rust
cargo run
```

**코드 살펴보기:**
```rust
fn main() {
    println!("Hello from Rust! 🦀");
}
```

---

## 🚀 실습 2: 간단한 병렬처리

```bash
cd parallel_sum
cargo run --release
```

**성능:**
```
순차 처리: 2.5초
병렬 처리: 0.3초
속도 향상: 8.3배!
```

**코드 살펴보기:**
```rust
use rayon::prelude::*;

fn main() {
    let data: Vec<i32> = (0..10_000_000).collect();

    // 병렬 합계
    let sum: i32 = data.par_iter().sum();

    println!("합계: {}", sum);
}
```

---

## 🚀 실습 3: Python vs Rust 비교

### Python 버전 실행
```bash
python3 compare_python.py
```

### Rust 버전 실행
```bash
cd compare_rust
cargo run --release
```

### 결과 비교

| 작업 | Python | Rust | 배수 |
|------|--------|------|------|
| 배열 계산 | 5.2초 | 0.4초 | 13x |
| 필터링 | 3.1초 | 0.2초 | 15.5x |
| 그룹화 | 8.5초 | 0.6초 | 14.2x |

---

## 📖 Rust 기초 문법 (10분)

### 변수

```rust
let x = 5;          // 불변 (기본)
let mut y = 10;     // 가변
y = 20;             // OK!
```

### 함수

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b  // return 생략 가능
}
```

### 벡터 (배열)

```rust
let v = vec![1, 2, 3, 4, 5];
let sum: i32 = v.iter().sum();
```

### 병렬 이터레이터

```rust
use rayon::prelude::*;

let v = vec![1, 2, 3, 4, 5];
let sum: i32 = v.par_iter().sum();  // par_iter()만 추가!
```

---

## 💡 Rayon의 마법

### Python에서

```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool() as pool:
    results = pool.map(square, data)
```

### Rust에서

```rust
use rayon::prelude::*;

let results: Vec<_> = data
    .par_iter()
    .map(|&x| x * x)
    .collect();
```

**더 간단하고 더 빠름!** ✨

---

## ⚙️ Cargo: Rust의 도구

### 새 프로젝트

```bash
cargo new my_project
cd my_project
```

### 의존성 추가

`Cargo.toml`:
```toml
[dependencies]
rayon = "1.7"
```

### 빌드 및 실행

```bash
cargo build --release  # 최적화 빌드
cargo run --release    # 빌드 + 실행
```

**⚠️ `--release` 플래그 필수!**
- Debug: 개발용 (느림)
- Release: 배포용 (빠름, 10-100배 차이!)

---

## 🎯 언제 Rust를 사용할까?

### ✅ Rust가 좋은 경우

1. **최고 성능이 필요**
   - 실시간 처리
   - 게임 엔진
   - 시스템 프로그래밍

2. **안전성이 중요**
   - 금융 시스템
   - 임베디드
   - 인프라 도구

3. **장기 프로젝트**
   - 유지보수 용이
   - 리팩토링 안전

### ❌ Rust가 부담스러운 경우

1. **빠른 프로토타이핑**
   → Python 추천

2. **간단한 스크립트**
   → Python/JavaScript 추천

3. **팀이 Rust 미경험**
   → 학습 비용 고려

---

## ✅ 체크리스트

- [ ] Rust 설치 완료
- [ ] Hello Rust 실행
- [ ] 병렬 합계 프로그램 실행
- [ ] Python vs Rust 성능 비교
- [ ] Rayon의 간단함 체험
- [ ] Cargo 사용법 이해

---

## 🎓 배운 내용

- ✅ Rust의 장점 (성능 + 안전성)
- ✅ Rayon으로 쉬운 병렬처리
- ✅ Python 대비 10-15배 빠름
- ✅ Cargo 도구 사용법
- ✅ --release의 중요성

---

## 🚀 다음 단계

Rust의 위력을 맛봤습니다!

👉 [Step 5: 실전 프로젝트](../step5-real-project/README.md)에서 배운 것을 종합해봅시다!

---

## 💡 더 배우기

### 추천 자료

1. **The Rust Book** (공식 문서)
   - https://doc.rust-lang.org/book/
   - 한국어: https://rust-kr.org/

2. **Rustlings** (대화형 연습)
   ```bash
   cargo install rustlings
   rustlings
   ```

3. **Exercism Rust Track**
   - https://exercism.org/tracks/rust

### Rust + Python

Python에서 Rust 호출 (PyO3):
```rust
use pyo3::prelude::*;

#[pyfunction]
fn fast_sum(numbers: Vec<i32>) -> i32 {
    numbers.iter().sum()
}
```

최고의 조합: Python의 편의성 + Rust의 성능!

---

## 🎨 실전 팁

### 1. 항상 --release

```bash
cargo build --release  # 10-100배 차이!
```

### 2. 타입 힌트

```rust
let sum: i32 = data.par_iter().sum();
       ^^^^  명시하면 명확!
```

### 3. 에러 메시지 읽기

Rust 컴파일러는 친절합니다:
```
error: cannot assign twice to immutable variable
  --> src/main.rs:3:5
   |
2  |     let x = 5;
   |         - first assignment
3  |     x = 10;
   |     ^^^^^^ cannot assign twice
   |
help: make this binding mutable: `let mut x`
```

### 4. Clippy 사용

```bash
cargo clippy  # 코드 개선 제안
```

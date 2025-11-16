# Go 언어 완벽 학습 가이드

Go(Golang)를 처음부터 체계적으로 배우기 위한 완벽한 학습 자료입니다.

## 📚 학습 로드맵

### [01. 기초 문법](./01-basics)
Go의 기본 문법과 핵심 개념을 배웁니다.
- Hello World & 환경 설정
- 변수와 상수
- 기본 데이터 타입
- 제어문 (if, for, switch)
- 함수
- 배열과 슬라이스
- 맵 (Map)
- 구조체 (Struct)
- 포인터

### [02. 중급 개념](./02-intermediate)
Go의 강력한 기능들을 학습합니다.
- 메서드
- 인터페이스 (Interface)
- 에러 처리
- Goroutine (동시성)
- Channel
- 패키지 관리
- 모듈 시스템
- 파일 입출력

### [03. 고급 주제](./03-advanced)
실무에 필요한 고급 개념을 다룹니다.
- Context
- Select 문
- Mutex와 동기화
- 리플렉션 (Reflection)
- 테스팅
- 벤치마크
- 프로파일링
- 디자인 패턴

### [04. 실전 프로젝트](./04-projects)
실제 프로젝트를 통해 배운 내용을 활용합니다.
- REST API 서버
- CLI 도구
- 웹 스크래퍼
- 동시성 패턴 활용

## 🚀 빠른 시작

### Go 설치

**macOS:**
```bash
brew install go
```

**Linux:**
```bash
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

**Windows:**
https://go.dev/dl/ 에서 설치 파일 다운로드

### 설치 확인
```bash
go version
```

### 첫 프로그램 실행
```bash
cd 01-basics
go run 01-hello-world.go
```

## 💡 학습 방법

1. **순서대로 학습**: 01-basics부터 시작하여 순서대로 진행하세요
2. **코드 실행**: 모든 예제 코드를 직접 실행해보세요
3. **수정해보기**: 코드를 수정하고 결과를 확인하세요
4. **연습 문제**: 각 섹션의 연습 문제를 풀어보세요
5. **프로젝트**: 실전 프로젝트로 배운 내용을 종합하세요

## 🎯 Go의 특징

- **간결함**: 최소한의 문법으로 명확한 코드 작성
- **빠른 컴파일**: C/C++처럼 빠른 컴파일 속도
- **동시성**: Goroutine과 Channel로 쉬운 동시성 프로그래밍
- **가비지 컬렉션**: 자동 메모리 관리
- **정적 타입**: 컴파일 타임 타입 체크
- **크로스 플랫폼**: 다양한 OS에서 실행 가능

## 📖 추가 자료

- [공식 문서](https://go.dev/doc/)
- [Go by Example](https://gobyexample.com/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Tour](https://go.dev/tour/)

## 🤝 기여

이 학습 자료에 대한 피드백이나 개선 사항이 있다면 언제든지 제안해주세요!

## 📝 라이선스

MIT License

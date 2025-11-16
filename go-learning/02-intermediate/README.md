# 02. Go 중급 개념

Go의 핵심 기능과 실무에 필요한 중급 개념을 학습합니다.

## 📋 목차

1. [메서드](01-methods.go)
2. [인터페이스](02-interfaces.go)
3. [에러 처리](03-errors.go)
4. [Goroutine](04-goroutines.go)
5. [Channel](05-channels.go)
6. [패키지와 모듈](06-packages/)
7. [파일 입출력](07-file-io.go)
8. [JSON 처리](08-json.go)

## 🎯 학습 목표

이 섹션을 마치면 다음을 할 수 있습니다:
- 메서드를 정의하고 값/포인터 리시버의 차이 이해
- 인터페이스로 다형성 구현
- 효과적인 에러 처리
- Goroutine으로 동시성 프로그래밍
- Channel로 안전한 데이터 통신
- 패키지 구조화 및 모듈 관리
- 파일과 JSON 데이터 처리

## 💻 실행 방법

각 예제를 실행하려면:
```bash
go run 01-methods.go
go run 02-interfaces.go
# ... 등등
```

## 🚀 Go의 동시성

Go의 가장 강력한 기능 중 하나는 동시성입니다:
- **Goroutine**: 경량 스레드
- **Channel**: 안전한 통신 메커니즘
- **Select**: 여러 채널 작업 관리

"Do not communicate by sharing memory; instead, share memory by communicating."

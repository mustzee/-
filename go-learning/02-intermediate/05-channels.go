package main

import (
	"fmt"
	"time"
)

// === 기본 Channel ===

func basicChannel() {
	ch := make(chan int)

	// 송신 goroutine
	go func() {
		ch <- 42 // 채널에 값 보내기
	}()

	// 수신
	value := <-ch // 채널에서 값 받기
	fmt.Println("받은 값:", value)
}

// === 버퍼링된 Channel ===

func bufferedChannel() {
	ch := make(chan int, 3) // 용량 3인 버퍼링된 채널

	// 버퍼가 차기 전까지 블로킹 없음
	ch <- 1
	ch <- 2
	ch <- 3

	fmt.Println(<-ch)
	fmt.Println(<-ch)
	fmt.Println(<-ch)
}

// === 채널 닫기 ===

func channelClose() {
	ch := make(chan int, 5)

	// 송신
	go func() {
		for i := 0; i < 5; i++ {
			ch <- i
		}
		close(ch) // 더 이상 보낼 데이터가 없음을 알림
	}()

	// 수신
	for {
		value, ok := <-ch
		if !ok {
			fmt.Println("채널이 닫혔습니다")
			break
		}
		fmt.Println("받은 값:", value)
	}
}

// === range로 채널 순회 ===

func channelRange() {
	ch := make(chan int, 5)

	go func() {
		for i := 0; i < 5; i++ {
			ch <- i * i
		}
		close(ch)
	}()

	// 채널이 닫힐 때까지 수신
	for value := range ch {
		fmt.Println("제곱:", value)
	}
}

// === select 문 ===

func selectExample() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		time.Sleep(1 * time.Second)
		ch1 <- "채널 1"
	}()

	go func() {
		time.Sleep(2 * time.Second)
		ch2 <- "채널 2"
	}()

	for i := 0; i < 2; i++ {
		select {
		case msg1 := <-ch1:
			fmt.Println("받음:", msg1)
		case msg2 := <-ch2:
			fmt.Println("받음:", msg2)
		}
	}
}

// === select with default ===

func selectDefault() {
	ch := make(chan int, 1)

	// 논블로킹 송신
	select {
	case ch <- 42:
		fmt.Println("송신 성공")
	default:
		fmt.Println("송신 실패: 버퍼 가득 참")
	}

	// 논블로킹 수신
	select {
	case value := <-ch:
		fmt.Println("수신:", value)
	default:
		fmt.Println("수신 실패: 데이터 없음")
	}
}

// === 타임아웃 패턴 ===

func timeoutPattern() {
	ch := make(chan string)

	go func() {
		time.Sleep(2 * time.Second)
		ch <- "결과"
	}()

	select {
	case result := <-ch:
		fmt.Println("받음:", result)
	case <-time.After(1 * time.Second):
		fmt.Println("타임아웃!")
	}
}

// === 파이프라인 패턴 ===

func generator(nums ...int) <-chan int {
	out := make(chan int)
	go func() {
		for _, n := range nums {
			out <- n
		}
		close(out)
	}()
	return out
}

func square(in <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for n := range in {
			out <- n * n
		}
		close(out)
	}()
	return out
}

func print(in <-chan int) {
	for n := range in {
		fmt.Println(n)
	}
}

func pipelineExample() {
	// 파이프라인: generator -> square -> print
	nums := generator(1, 2, 3, 4, 5)
	squared := square(nums)
	print(squared)
}

// === 방향성 채널 ===

func send(ch chan<- int) { // 송신 전용
	ch <- 42
}

func receive(ch <-chan int) { // 수신 전용
	value := <-ch
	fmt.Println("수신:", value)
}

func directedChannels() {
	ch := make(chan int)
	go send(ch)
	receive(ch)
}

// === 실용 예제: Worker Pool ===

type Job struct {
	ID     int
	Data   string
	Result chan string
}

func worker(id int, jobs <-chan Job) {
	for job := range jobs {
		fmt.Printf("Worker %d가 작업 %d 처리 중\n", id, job.ID)
		time.Sleep(100 * time.Millisecond)
		job.Result <- fmt.Sprintf("Worker %d: %s 완료", id, job.Data)
	}
}

func workerPoolPattern() {
	numWorkers := 3
	jobs := make(chan Job, 10)

	// Worker 시작
	for w := 1; w <= numWorkers; w++ {
		go worker(w, jobs)
	}

	// 작업 생성
	results := make([]chan string, 5)
	for i := 0; i < 5; i++ {
		results[i] = make(chan string)
		jobs <- Job{
			ID:     i + 1,
			Data:   fmt.Sprintf("작업-%d", i+1),
			Result: results[i],
		}
	}

	// 결과 수집
	for i := 0; i < 5; i++ {
		fmt.Println(<-results[i])
	}

	close(jobs)
}

// === 실용 예제: 팬아웃/팬인 ===

func producer(ch chan<- int, n int) {
	for i := 1; i <= n; i++ {
		ch <- i
	}
	close(ch)
}

func multiplier(in <-chan int, out chan<- int, factor int) {
	for num := range in {
		out <- num * factor
	}
}

func fanInPattern() {
	input := make(chan int)
	output := make(chan int)

	// Producer
	go producer(input, 10)

	// Fan-out: 3개의 multiplier
	numWorkers := 3
	for i := 0; i < numWorkers; i++ {
		go multiplier(input, output, 2)
	}

	// Fan-in을 위한 카운터
	go func() {
		// 입력 채널이 닫히면 출력 채널도 닫기
		// (실제로는 sync.WaitGroup 사용 권장)
		time.Sleep(200 * time.Millisecond)
		close(output)
	}()

	// 결과 수집
	for result := range output {
		fmt.Println("결과:", result)
	}
}

// === 실용 예제: 세마포어 ===

func semaphore() {
	// 동시에 3개까지만 실행
	sem := make(chan struct{}, 3)

	for i := 1; i <= 10; i++ {
		sem <- struct{}{} // 세마포어 획득
		go func(id int) {
			defer func() { <-sem }() // 세마포어 해제

			fmt.Printf("작업 %d 시작\n", id)
			time.Sleep(500 * time.Millisecond)
			fmt.Printf("작업 %d 완료\n", id)
		}(i)
	}

	// 모든 작업 완료 대기
	for i := 0; i < cap(sem); i++ {
		sem <- struct{}{}
	}
}

// === Done 채널 패턴 ===

func donePattern() {
	done := make(chan struct{})

	go func() {
		for {
			select {
			case <-done:
				fmt.Println("Goroutine 종료")
				return
			default:
				fmt.Println("작업 중...")
				time.Sleep(200 * time.Millisecond)
			}
		}
	}()

	time.Sleep(1 * time.Second)
	close(done) // goroutine에 종료 신호 보내기
	time.Sleep(100 * time.Millisecond)
}

// === nil 채널 ===

func nilChannel() {
	var ch chan int // nil 채널

	select {
	case <-ch:
		// nil 채널은 영원히 블로킹
		fmt.Println("이 줄은 실행되지 않음")
	case <-time.After(100 * time.Millisecond):
		fmt.Println("nil 채널은 블로킹됨")
	}
}

func main() {
	// === 기본 Channel ===
	fmt.Println("=== 기본 Channel ===")
	basicChannel()

	// === 버퍼링된 Channel ===
	fmt.Println("\n=== 버퍼링된 Channel ===")
	bufferedChannel()

	// === 채널 닫기 ===
	fmt.Println("\n=== 채널 닫기 ===")
	channelClose()

	// === range로 순회 ===
	fmt.Println("\n=== range로 채널 순회 ===")
	channelRange()

	// === select ===
	fmt.Println("\n=== select ===")
	selectExample()

	// === select with default ===
	fmt.Println("\n=== select with default ===")
	selectDefault()

	// === 타임아웃 ===
	fmt.Println("\n=== 타임아웃 패턴 ===")
	timeoutPattern()

	// === 파이프라인 ===
	fmt.Println("\n=== 파이프라인 ===")
	pipelineExample()

	// === 방향성 채널 ===
	fmt.Println("\n=== 방향성 채널 ===")
	directedChannels()

	// === Worker Pool ===
	fmt.Println("\n=== Worker Pool ===")
	workerPoolPattern()

	// === Fan-In ===
	fmt.Println("\n=== Fan-In ===")
	fanInPattern()

	// === 세마포어 ===
	fmt.Println("\n=== 세마포어 ===")
	semaphore()

	// === Done 채널 ===
	fmt.Println("\n=== Done 채널 ===")
	donePattern()

	// === nil 채널 ===
	fmt.Println("\n=== nil 채널 ===")
	nilChannel()
}

/*
Channel 핵심 개념:

1. Channel 기초:
   - make(chan T): 버퍼 없는 채널
   - make(chan T, n): 버퍼 크기 n인 채널
   - ch <- value: 송신
   - value := <-ch: 수신
   - close(ch): 채널 닫기

2. 버퍼링:
   - 버퍼 없음: 동기 통신 (송신자와 수신자 모두 대기)
   - 버퍼 있음: 비동기 통신 (버퍼가 찰 때까지 블로킹 없음)

3. select:
   - 여러 채널 작업 중 하나 실행
   - default: 논블로킹 동작
   - time.After(): 타임아웃 구현

4. 채널 방향:
   - chan T: 양방향
   - chan<- T: 송신 전용
   - <-chan T: 수신 전용

5. 패턴:
   - Pipeline: 단계별 처리
   - Fan-Out/Fan-In: 작업 분산 및 수집
   - Worker Pool: 작업자 풀
   - Done Channel: 종료 신호

6. 주의사항:
   - 닫힌 채널에 송신: panic
   - nil 채널: 영원히 블로킹
   - 채널 누수 방지
   - 송신자가 채널을 닫아야 함

Go의 철학:
"Do not communicate by sharing memory;
 instead, share memory by communicating."

연습 문제:
1. 피보나치 수열을 생성하는 채널 기반 제너레이터를 만드세요
2. 여러 소스의 데이터를 하나의 채널로 병합하세요
3. 채널로 구현한 큐(Queue)를 만드세요
4. 속도 제한기(Rate Limiter)를 채널로 구현하세요
5. 여러 작업의 첫 번째 결과만 받는 패턴을 구현하세요

실행: go run 05-channels.go
*/

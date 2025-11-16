package main

import (
	"fmt"
	"sync"
	"time"
)

// === 기본 Goroutine ===

func sayHello() {
	for i := 0; i < 5; i++ {
		fmt.Println("Hello", i)
		time.Sleep(100 * time.Millisecond)
	}
}

func sayWorld() {
	for i := 0; i < 5; i++ {
		fmt.Println("World", i)
		time.Sleep(100 * time.Millisecond)
	}
}

// === 익명 함수와 Goroutine ===

func runAnonymous() {
	go func() {
		for i := 0; i < 3; i++ {
			fmt.Println("익명 함수", i)
			time.Sleep(100 * time.Millisecond)
		}
	}()
}

// === WaitGroup 사용 ===

func worker(id int, wg *sync.WaitGroup) {
	defer wg.Done() // 함수 종료 시 WaitGroup 카운터 감소

	fmt.Printf("Worker %d 시작\n", id)
	time.Sleep(time.Duration(id*100) * time.Millisecond)
	fmt.Printf("Worker %d 완료\n", id)
}

func useWaitGroup() {
	var wg sync.WaitGroup

	for i := 1; i <= 5; i++ {
		wg.Add(1) // WaitGroup 카운터 증가
		go worker(i, &wg)
	}

	wg.Wait() // 모든 goroutine이 완료될 때까지 대기
	fmt.Println("모든 worker 완료")
}

// === 동시성 문제: Race Condition ===

func unsafeCounter() {
	counter := 0
	var wg sync.WaitGroup

	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter++ // 동시 접근 문제!
		}()
	}

	wg.Wait()
	fmt.Println("Unsafe Counter:", counter) // 1000이 아닐 수 있음
}

// === Mutex로 안전하게 만들기 ===

func safeCounter() {
	counter := 0
	var mu sync.Mutex
	var wg sync.WaitGroup

	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			mu.Lock()
			counter++
			mu.Unlock()
		}()
	}

	wg.Wait()
	fmt.Println("Safe Counter:", counter) // 항상 1000
}

// === 구조체와 Mutex ===

type SafeCounter struct {
	mu    sync.Mutex
	value int
}

func (c *SafeCounter) Increment() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

func (c *SafeCounter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// === Goroutine 풀 패턴 ===

func workerPool() {
	numWorkers := 3
	jobs := make(chan int, 10)
	results := make(chan int, 10)

	var wg sync.WaitGroup

	// Worker 시작
	for w := 1; w <= numWorkers; w++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for job := range jobs {
				fmt.Printf("Worker %d가 작업 %d 처리 중\n", id, job)
				time.Sleep(100 * time.Millisecond)
				results <- job * 2
			}
		}(w)
	}

	// 작업 보내기
	for j := 1; j <= 9; j++ {
		jobs <- j
	}
	close(jobs)

	// 모든 worker 완료 대기
	wg.Wait()
	close(results)

	// 결과 수집
	fmt.Print("결과: ")
	for result := range results {
		fmt.Print(result, " ")
	}
	fmt.Println()
}

// === 실용 예제: 병렬 다운로드 시뮬레이션 ===

func downloadFile(url string, wg *sync.WaitGroup) {
	defer wg.Done()

	fmt.Printf("다운로드 시작: %s\n", url)
	time.Sleep(time.Duration(len(url)*10) * time.Millisecond)
	fmt.Printf("다운로드 완료: %s\n", url)
}

func parallelDownload() {
	urls := []string{
		"https://example.com/file1.zip",
		"https://example.com/file2.zip",
		"https://example.com/file3.zip",
		"https://example.com/file4.zip",
	}

	var wg sync.WaitGroup

	for _, url := range urls {
		wg.Add(1)
		go downloadFile(url, &wg)
	}

	wg.Wait()
	fmt.Println("모든 다운로드 완료")
}

// === 실용 예제: 팬아웃/팬인 패턴 ===

func producer(ch chan<- int) {
	for i := 1; i <= 10; i++ {
		ch <- i
	}
	close(ch)
}

func square(in <-chan int, out chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for num := range in {
		out <- num * num
	}
}

func fanOutFanIn() {
	numbers := make(chan int)
	results := make(chan int)

	// Producer
	go producer(numbers)

	// Fan-out: 여러 worker
	var wg sync.WaitGroup
	numWorkers := 3
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go square(numbers, results, &wg)
	}

	// Fan-in: 결과 수집
	go func() {
		wg.Wait()
		close(results)
	}()

	// 결과 출력
	fmt.Print("제곱 결과: ")
	for result := range results {
		fmt.Print(result, " ")
	}
	fmt.Println()
}

// === 타임아웃과 Goroutine ===

func longRunningTask(done chan bool) {
	fmt.Println("긴 작업 시작...")
	time.Sleep(3 * time.Second)
	fmt.Println("긴 작업 완료")
	done <- true
}

func withTimeout() {
	done := make(chan bool)

	go longRunningTask(done)

	select {
	case <-done:
		fmt.Println("작업이 완료되었습니다")
	case <-time.After(2 * time.Second):
		fmt.Println("타임아웃!")
	}
}

func main() {
	// === 기본 Goroutine ===
	fmt.Println("=== 기본 Goroutine ===")
	go sayHello()
	go sayWorld()
	time.Sleep(600 * time.Millisecond)

	fmt.Println("\n=== 익명 함수 ===")
	runAnonymous()
	time.Sleep(400 * time.Millisecond)

	// === WaitGroup ===
	fmt.Println("\n=== WaitGroup ===")
	useWaitGroup()

	// === Race Condition ===
	fmt.Println("\n=== Race Condition (안전하지 않음) ===")
	unsafeCounter() // 결과가 매번 다를 수 있음

	// === Mutex ===
	fmt.Println("\n=== Mutex (안전함) ===")
	safeCounter()

	// === SafeCounter ===
	fmt.Println("\n=== SafeCounter 구조체 ===")
	counter := &SafeCounter{}
	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}

	wg.Wait()
	fmt.Println("최종 카운터:", counter.Value())

	// === Worker Pool ===
	fmt.Println("\n=== Worker Pool ===")
	workerPool()

	// === 병렬 다운로드 ===
	fmt.Println("\n=== 병렬 다운로드 ===")
	parallelDownload()

	// === Fan-Out/Fan-In ===
	fmt.Println("\n=== Fan-Out/Fan-In ===")
	fanOutFanIn()

	// === 타임아웃 ===
	fmt.Println("\n=== 타임아웃 ===")
	withTimeout()

	// === 주의사항 ===
	fmt.Println("\n=== Goroutine 주의사항 ===")
	fmt.Println("1. main이 종료되면 모든 goroutine도 종료")
	fmt.Println("2. WaitGroup이나 Channel로 동기화 필요")
	fmt.Println("3. 공유 데이터는 Mutex나 Channel로 보호")
	fmt.Println("4. 너무 많은 goroutine 생성 주의 (메모리 소비)")
}

/*
Goroutine 핵심 개념:

1. Goroutine이란?
   - 경량 스레드
   - go 키워드로 실행
   - OS 스레드보다 훨씬 가벼움
   - Go 런타임이 관리

2. 동기화:
   - WaitGroup: 여러 goroutine 완료 대기
   - Channel: goroutine 간 통신 (다음 파일)
   - Mutex: 공유 데이터 보호

3. Race Condition:
   - 여러 goroutine이 동시에 데이터 접근
   - Mutex나 Channel로 해결
   - go run -race 로 검사 가능

4. 패턴:
   - Worker Pool: 고정된 수의 worker
   - Fan-Out/Fan-In: 작업 분산 후 수집
   - Pipeline: 단계별 처리

5. 주의사항:
   - Goroutine 누수 방지
   - 적절한 동기화
   - 공유 메모리 대신 채널 사용 권장

연습 문제:
1. 1부터 100까지 합을 10개의 goroutine으로 계산하세요
2. 파일 여러 개를 동시에 읽는 함수를 작성하세요
3. Rate limiter를 goroutine으로 구현하세요
4. 병렬 웹 크롤러를 만드세요
5. 프로듀서-컨슈머 패턴을 구현하세요

Race Detection:
  go run -race 04-goroutines.go

실행: go run 04-goroutines.go
*/

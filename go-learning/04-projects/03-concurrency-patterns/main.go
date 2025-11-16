package main

import (
	"fmt"
	"sync"
	"time"
)

// === 1. Worker Pool 패턴 ===

func workerPoolExample() {
	fmt.Println("=== Worker Pool ===")

	jobs := make(chan int, 10)
	results := make(chan int, 10)

	// 3개의 worker 시작
	var wg sync.WaitGroup
	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for job := range jobs {
				fmt.Printf("Worker %d가 작업 %d 처리\n", id, job)
				time.Sleep(100 * time.Millisecond)
				results <- job * 2
			}
		}(w)
	}

	// 10개의 작업 보내기
	for j := 1; j <= 10; j++ {
		jobs <- j
	}
	close(jobs)

	// 결과 수집
	go func() {
		wg.Wait()
		close(results)
	}()

	fmt.Print("결과: ")
	for r := range results {
		fmt.Print(r, " ")
	}
	fmt.Println()
}

// === 2. 파이프라인 패턴 ===

func pipelineExample() {
	fmt.Println("\n=== Pipeline ===")

	// Stage 1: 숫자 생성
	gen := func(nums ...int) <-chan int {
		out := make(chan int)
		go func() {
			for _, n := range nums {
				out <- n
			}
			close(out)
		}()
		return out
	}

	// Stage 2: 제곱
	square := func(in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			for n := range in {
				out <- n * n
			}
			close(out)
		}()
		return out
	}

	// Stage 3: 합계
	sum := func(in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			total := 0
			for n := range in {
				total += n
			}
			out <- total
			close(out)
		}()
		return out
	}

	// 파이프라인 실행
	nums := gen(1, 2, 3, 4, 5)
	squared := square(nums)
	result := sum(squared)

	fmt.Println("1² + 2² + 3² + 4² + 5² =", <-result)
}

// === 3. Fan-Out/Fan-In 패턴 ===

func fanOutFanInExample() {
	fmt.Println("\n=== Fan-Out/Fan-In ===")

	// Producer
	producer := func(n int) <-chan int {
		out := make(chan int)
		go func() {
			for i := 1; i <= n; i++ {
				out <- i
			}
			close(out)
		}()
		return out
	}

	// Worker
	worker := func(in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			for n := range in {
				time.Sleep(50 * time.Millisecond)
				out <- n * n
			}
			close(out)
		}()
		return out
	}

	// Fan-In
	fanIn := func(channels ...<-chan int) <-chan int {
		out := make(chan int)
		var wg sync.WaitGroup

		for _, ch := range channels {
			wg.Add(1)
			go func(c <-chan int) {
				defer wg.Done()
				for n := range c {
					out <- n
				}
			}(ch)
		}

		go func() {
			wg.Wait()
			close(out)
		}()

		return out
	}

	// 실행
	input := producer(10)

	// Fan-Out: 3개의 worker
	w1 := worker(input)
	w2 := worker(input)
	w3 := worker(input)

	// Fan-In: 결과 병합
	results := fanIn(w1, w2, w3)

	fmt.Print("제곱 결과: ")
	for r := range results {
		fmt.Print(r, " ")
	}
	fmt.Println()
}

// === 4. 세마포어 패턴 ===

func semaphoreExample() {
	fmt.Println("\n=== Semaphore (최대 3개 동시 실행) ===")

	sem := make(chan struct{}, 3) // 세마포어

	var wg sync.WaitGroup
	for i := 1; i <= 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			sem <- struct{}{} // 세마포어 획득
			fmt.Printf("작업 %d 시작\n", id)
			time.Sleep(200 * time.Millisecond)
			fmt.Printf("작업 %d 완료\n", id)
			<-sem // 세마포어 해제
		}(i)
	}

	wg.Wait()
	fmt.Println("모든 작업 완료")
}

// === 5. Context 패턴 (타임아웃) ===

func timeoutExample() {
	fmt.Println("\n=== Timeout ===")

	done := make(chan bool)

	go func() {
		fmt.Println("긴 작업 시작...")
		time.Sleep(2 * time.Second)
		done <- true
	}()

	select {
	case <-done:
		fmt.Println("작업 완료")
	case <-time.After(1 * time.Second):
		fmt.Println("타임아웃!")
	}
}

func main() {
	workerPoolExample()
	pipelineExample()
	fanOutFanInExample()
	semaphoreExample()
	timeoutExample()

	fmt.Println("\n모든 패턴 실행 완료!")
}

/*
동시성 패턴

패턴:
1. Worker Pool - 고정된 수의 작업자
2. Pipeline - 단계별 데이터 처리
3. Fan-Out/Fan-In - 병렬 처리 후 결과 수집
4. Semaphore - 동시 실행 수 제한
5. Timeout - 작업 시간 제한

실행:
  go run main.go
*/

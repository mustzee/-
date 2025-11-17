package main

import (
	"fmt"
	"math"
	"math/rand"
	"runtime"
	"sync"
	"sync/atomic"
	"time"
)

// 1. 기본 고루틴과 WaitGroup
func demonstrateBasicGoroutines() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("1. 기본 고루틴과 WaitGroup")
	fmt.Println(strings.Repeat("=", 60))

	size := 10_000_000
	numWorkers := runtime.NumCPU()
	chunkSize := size / numWorkers

	// 순차 처리
	start := time.Now()
	sumSeq := 0.0
	for i := 0; i < size; i++ {
		sumSeq += math.Sin(float64(i)) * math.Cos(float64(i))
	}
	seqDuration := time.Since(start)

	// 병렬 처리
	start = time.Now()
	var wg sync.WaitGroup
	results := make([]float64, numWorkers)

	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go func(worker int) {
			defer wg.Done()
			localSum := 0.0
			startIdx := worker * chunkSize
			endIdx := startIdx + chunkSize
			if worker == numWorkers-1 {
				endIdx = size
			}
			for i := startIdx; i < endIdx; i++ {
				localSum += math.Sin(float64(i)) * math.Cos(float64(i))
			}
			results[worker] = localSum
		}(w)
	}
	wg.Wait()

	sumPar := 0.0
	for _, r := range results {
		sumPar += r
	}
	parDuration := time.Since(start)

	fmt.Printf("\n크기: %d 원소\n", size)
	fmt.Printf("워커 수: %d\n", numWorkers)
	fmt.Printf("순차 처리: %.3f초\n", seqDuration.Seconds())
	fmt.Printf("병렬 처리: %.3f초 (%.2fx)\n",
		parDuration.Seconds(), seqDuration.Seconds()/parDuration.Seconds())
	fmt.Printf("차이: %.2e\n\n", math.Abs(sumSeq-sumPar))
}

// 2. 채널을 사용한 파이프라인
func demonstrateChannelPipeline() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("2. 채널 파이프라인")
	fmt.Println(strings.Repeat("=", 60))

	// 생성자: 숫자 생성
	generate := func(n int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for i := 0; i < n; i++ {
				out <- i
			}
		}()
		return out
	}

	// 처리자: 제곱
	square := func(in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for n := range in {
				out <- n * n
			}
		}()
		return out
	}

	// 필터: 짝수만
	filterEven := func(in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for n := range in {
				if n%2 == 0 {
					out <- n
				}
			}
		}()
		return out
	}

	n := 1_000_000
	start := time.Now()

	// 파이프라인 구성
	numbers := generate(n)
	squared := square(numbers)
	filtered := filterEven(squared)

	// 결과 수집
	sum := 0
	count := 0
	for n := range filtered {
		sum += n
		count++
	}

	duration := time.Since(start)

	fmt.Printf("\n원본 크기: %d\n", n)
	fmt.Printf("필터된 크기: %d\n", count)
	fmt.Printf("처리 시간: %.3f초\n", duration.Seconds())
	fmt.Printf("총합: %d\n\n", sum)
}

// 3. Worker Pool 패턴
func demonstrateWorkerPool() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("3. Worker Pool 패턴")
	fmt.Println(strings.Repeat("=", 60))

	numJobs := 100
	numWorkers := runtime.NumCPU()

	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)

	// Worker 생성
	start := time.Now()
	var wg sync.WaitGroup

	for w := 1; w <= numWorkers; w++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := range jobs {
				// 무거운 작업 시뮬레이션
				result := 0
				for i := 0; i < 1_000_000; i++ {
					result += int(math.Sin(float64(i)) * 1000)
				}
				results <- result + j
			}
		}(w)
	}

	// Job 전송
	go func() {
		for j := 1; j <= numJobs; j++ {
			jobs <- j
		}
		close(jobs)
	}()

	// 결과 수집
	go func() {
		wg.Wait()
		close(results)
	}()

	count := 0
	for range results {
		count++
	}

	duration := time.Since(start)

	fmt.Printf("\nJob 수: %d\n", numJobs)
	fmt.Printf("Worker 수: %d\n", numWorkers)
	fmt.Printf("처리 시간: %.3f초\n", duration.Seconds())
	fmt.Printf("처리된 Job: %d\n\n", count)
}

// 4. 몬테카를로 π 추정
func monteCarloWorker(samples int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	inside := 0
	rng := rand.New(rand.NewSource(time.Now().UnixNano()))

	for i := 0; i < samples; i++ {
		x := rng.Float64()
		y := rng.Float64()
		if x*x+y*y <= 1.0 {
			inside++
		}
	}
	results <- inside
}

func demonstrateMonteCarlo() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("4. 몬테카를로 π 추정")
	fmt.Println(strings.Repeat("=", 60))

	totalSamples := 100_000_000
	numWorkers := runtime.NumCPU()
	samplesPerWorker := totalSamples / numWorkers

	fmt.Printf("\n총 샘플: %d\n", totalSamples)
	fmt.Printf("워커 수: %d\n", numWorkers)

	start := time.Now()
	var wg sync.WaitGroup
	results := make(chan int, numWorkers)

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go monteCarloWorker(samplesPerWorker, results, &wg)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	totalInside := 0
	for r := range results {
		totalInside += r
	}

	piEstimate := 4.0 * float64(totalInside) / float64(totalSamples)
	duration := time.Since(start)

	fmt.Printf("\n처리 시간: %.3f초\n", duration.Seconds())
	fmt.Printf("π 추정값: %.6f\n", piEstimate)
	fmt.Printf("실제 π: %.6f\n", math.Pi)
	fmt.Printf("오차: %.6f\n", math.Abs(piEstimate-math.Pi))
	fmt.Printf("처리 속도: %.2fM 샘플/초\n\n",
		float64(totalSamples)/duration.Seconds()/1_000_000)
}

// 5. Atomic 연산
func demonstrateAtomic() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("5. Atomic 연산")
	fmt.Println(strings.Repeat("=", 60))

	numGoroutines := 100
	incrementsPerGoroutine := 10_000

	// Mutex 사용
	var counterMutex int64
	var mu sync.Mutex
	var wg sync.WaitGroup

	start := time.Now()
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < incrementsPerGoroutine; j++ {
				mu.Lock()
				counterMutex++
				mu.Unlock()
			}
		}()
	}
	wg.Wait()
	mutexDuration := time.Since(start)

	// Atomic 사용
	var counterAtomic int64

	start = time.Now()
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < incrementsPerGoroutine; j++ {
				atomic.AddInt64(&counterAtomic, 1)
			}
		}()
	}
	wg.Wait()
	atomicDuration := time.Since(start)

	expected := int64(numGoroutines * incrementsPerGoroutine)

	fmt.Printf("\n총 증가: %d\n", expected)
	fmt.Printf("Mutex: %.3f초, 결과: %d\n", mutexDuration.Seconds(), counterMutex)
	fmt.Printf("Atomic: %.3f초, 결과: %d (%.2fx 빠름)\n\n",
		atomicDuration.Seconds(), counterAtomic,
		mutexDuration.Seconds()/atomicDuration.Seconds())
}

// 6. 배열 병렬 처리
func demonstrateArrayProcessing() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("6. 배열 병렬 처리")
	fmt.Println(strings.Repeat("=", 60))

	size := 10_000_000
	data := make([]float64, size)
	for i := range data {
		data[i] = float64(i)
	}

	numWorkers := runtime.NumCPU()
	chunkSize := size / numWorkers

	// 순차 처리
	start := time.Now()
	resultSeq := make([]float64, size)
	for i, v := range data {
		resultSeq[i] = math.Sqrt(math.Abs(math.Sin(v) * math.Cos(v)))
	}
	seqDuration := time.Since(start)

	// 병렬 처리
	start = time.Now()
	resultPar := make([]float64, size)
	var wg sync.WaitGroup

	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go func(worker int) {
			defer wg.Done()
			startIdx := worker * chunkSize
			endIdx := startIdx + chunkSize
			if worker == numWorkers-1 {
				endIdx = size
			}
			for i := startIdx; i < endIdx; i++ {
				v := data[i]
				resultPar[i] = math.Sqrt(math.Abs(math.Sin(v) * math.Cos(v)))
			}
		}(w)
	}
	wg.Wait()
	parDuration := time.Since(start)

	// 검증
	diff := 0.0
	for i := range resultSeq {
		diff += math.Abs(resultSeq[i] - resultPar[i])
	}

	fmt.Printf("\n배열 크기: %d 원소\n", size)
	fmt.Printf("워커 수: %d\n", numWorkers)
	fmt.Printf("순차 처리: %.3f초\n", seqDuration.Seconds())
	fmt.Printf("병렬 처리: %.3f초 (%.2fx)\n",
		parDuration.Seconds(), seqDuration.Seconds()/parDuration.Seconds())
	fmt.Printf("결과 차이: %.2e\n\n", diff)
}

// 7. 이미지 블러 (간단한 버전)
func boxBlurParallel(image [][]uint8, blurSize int) [][]uint8 {
	height := len(image)
	width := len(image[0])
	result := make([][]uint8, height)
	for i := range result {
		result[i] = make([]uint8, width)
	}

	var wg sync.WaitGroup
	numWorkers := runtime.NumCPU()
	rowsPerWorker := height / numWorkers

	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go func(worker int) {
			defer wg.Done()
			startRow := worker * rowsPerWorker
			endRow := startRow + rowsPerWorker
			if worker == numWorkers-1 {
				endRow = height
			}

			half := blurSize / 2
			for i := startRow; i < endRow; i++ {
				for j := 0; j < width; j++ {
					iMin := max(0, i-half)
					iMax := min(height, i+half+1)
					jMin := max(0, j-half)
					jMax := min(width, j+half+1)

					sum := 0
					count := 0
					for ii := iMin; ii < iMax; ii++ {
						for jj := jMin; jj < jMax; jj++ {
							sum += int(image[ii][jj])
							count++
						}
					}
					result[i][j] = uint8(sum / count)
				}
			}
		}(w)
	}
	wg.Wait()

	return result
}

func demonstrateImageBlur() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("7. 이미지 블러")
	fmt.Println(strings.Repeat("=", 60))

	height, width := 1000, 1000
	blurSize := 5

	// 랜덤 이미지 생성
	image := make([][]uint8, height)
	for i := range image {
		image[i] = make([]uint8, width)
		for j := range image[i] {
			image[i][j] = uint8(rand.Intn(256))
		}
	}

	fmt.Printf("\n이미지 크기: %dx%d\n", height, width)
	fmt.Printf("블러 크기: %dx%d\n", blurSize, blurSize)

	start := time.Now()
	blurred := boxBlurParallel(image, blurSize)
	duration := time.Since(start)

	fmt.Printf("처리 시간: %.3f초\n", duration.Seconds())
	fmt.Printf("결과 크기: %dx%d\n\n", len(blurred), len(blurred[0]))
}

// 8. 스케일링 테스트
func demonstrateScaling() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("8. 스케일링 테스트")
	fmt.Println(strings.Repeat("=", 60))

	size := 50_000_000
	data := make([]float64, size)
	for i := range data {
		data[i] = float64(i)
	}

	maxWorkers := runtime.NumCPU()

	fmt.Printf("\n작업 크기: %d 원소\n", size)
	fmt.Printf("사용 가능 코어: %d\n", maxWorkers)
	fmt.Println("\n워커 수별 성능:")
	fmt.Println(strings.Repeat("-", 60))

	workerCounts := []int{1, 2, 4, 8}
	var baseTime float64

	for _, numWorkers := range workerCounts {
		if numWorkers > maxWorkers {
			break
		}

		chunkSize := size / numWorkers
		start := time.Now()

		var wg sync.WaitGroup
		results := make([]float64, numWorkers)

		for w := 0; w < numWorkers; w++ {
			wg.Add(1)
			go func(worker int) {
				defer wg.Done()
				localSum := 0.0
				startIdx := worker * chunkSize
				endIdx := startIdx + chunkSize
				if worker == numWorkers-1 {
					endIdx = size
				}
				for i := startIdx; i < endIdx; i++ {
					v := data[i]
					localSum += math.Sqrt(math.Abs(math.Sin(v) * math.Cos(v)))
				}
				results[worker] = localSum
			}(w)
		}
		wg.Wait()

		duration := time.Since(start).Seconds()

		if numWorkers == 1 {
			baseTime = duration
		}

		speedup := baseTime / duration
		efficiency := speedup / float64(numWorkers) * 100

		fmt.Printf("  %2d 워커: %.3f초 | 속도향상: %.2fx | 효율: %.1f%%\n",
			numWorkers, duration, speedup, efficiency)
	}
	fmt.Println()
}

// 유틸리티 함수
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// strings 패키지 대체
var strings = struct {
	Repeat func(string, int) string
}{
	Repeat: func(s string, count int) string {
		result := ""
		for i := 0; i < count; i++ {
			result += s
		}
		return result
	},
}

func main() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("Go 병렬 처리 데모")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Printf("CPU 코어: %d\n", runtime.NumCPU())
	fmt.Printf("최대 고루틴: %d\n\n", runtime.GOMAXPROCS(0))

	demonstrateBasicGoroutines()
	demonstrateChannelPipeline()
	demonstrateWorkerPool()
	demonstrateMonteCarlo()
	demonstrateAtomic()
	demonstrateArrayProcessing()
	demonstrateImageBlur()
	demonstrateScaling()

	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("Go 병렬 처리 핵심 정리")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println(`
1. 고루틴 (Goroutines)
   - 경량 스레드 (2KB 스택)
   - 수백만 개 생성 가능
   - go 키워드로 간단히 실행

2. 채널 (Channels)
   - 고루틴 간 통신
   - 동기화 메커니즘
   - "Don't communicate by sharing memory; share memory by communicating"

3. 동기화
   - sync.WaitGroup: 고루틴 완료 대기
   - sync.Mutex: 상호 배제
   - sync/atomic: 원자적 연산

4. 패턴
   - Worker Pool: 작업 분산
   - Pipeline: 데이터 스트림 처리
   - Fan-out/Fan-in: 병렬 처리 후 병합

5. 성능 특성
   - 중간 수준 (C보다 느리지만 Python보다 빠름)
   - 우수한 동시성
   - 가비지 컬렉션 오버헤드

6. 실행
   go run main.go

   GOMAXPROCS 설정:
   GOMAXPROCS=4 go run main.go

7. 다음 단계
   - Context 패키지 (취소, 타임아웃)
   - Select 문 (여러 채널)
   - 분산 시스템
`)
}

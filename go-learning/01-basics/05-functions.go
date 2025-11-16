package main

import "fmt"

// === 기본 함수 ===

// 파라미터와 반환값이 있는 함수
func add(a int, b int) int {
	return a + b
}

// 같은 타입의 파라미터는 타입을 한 번만 명시
func multiply(a, b int) int {
	return a * b
}

// === 여러 값 반환 ===
func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("0으로 나눌 수 없습니다")
	}
	return a / b, nil
}

// 여러 값 반환 (실용적 예제)
func minMax(numbers []int) (int, int) {
	if len(numbers) == 0 {
		return 0, 0
	}
	min, max := numbers[0], numbers[0]
	for _, num := range numbers {
		if num < min {
			min = num
		}
		if num > max {
			max = num
		}
	}
	return min, max
}

// === 이름 있는 반환값 ===
func rectangle(width, height float64) (area, perimeter float64) {
	area = width * height
	perimeter = 2 * (width + height)
	return // naked return
}

// === 가변 인자 함수 ===
func sum(numbers ...int) int {
	total := 0
	for _, num := range numbers {
		total += num
	}
	return total
}

// 가변 인자 + 일반 파라미터
func printInfo(prefix string, values ...interface{}) {
	fmt.Print(prefix, ": ")
	for _, v := range values {
		fmt.Print(v, " ")
	}
	fmt.Println()
}

// === 함수를 값으로 사용 ===
func applyOperation(a, b int, op func(int, int) int) int {
	return op(a, b)
}

// === 클로저 (익명 함수) ===
func makeCounter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

// === 재귀 함수 ===
func factorial(n int) int {
	if n <= 1 {
		return 1
	}
	return n * factorial(n-1)
}

func fibonacci(n int) int {
	if n <= 1 {
		return n
	}
	return fibonacci(n-1) + fibonacci(n-2)
}

// === defer ===
func demonstrateDefer() {
	fmt.Println("함수 시작")

	// defer는 함수가 종료될 때 실행됨 (LIFO 순서)
	defer fmt.Println("1번째 defer")
	defer fmt.Println("2번째 defer")
	defer fmt.Println("3번째 defer")

	fmt.Println("함수 중간")
	fmt.Println("함수 끝")
	// 출력 순서: 시작 -> 중간 -> 끝 -> 3번째 -> 2번째 -> 1번째
}

// defer의 실용적 사용 (파일 닫기 등)
func processFile(filename string) {
	fmt.Printf("파일 열기: %s\n", filename)
	defer fmt.Printf("파일 닫기: %s\n", filename)

	fmt.Println("파일 처리 중...")
	// 실제로는 여기서 파일 작업
}

// === 메서드와 비슷하지만 일반 함수 ===
type Calculator struct {
	result float64
}

func (c *Calculator) Add(value float64) {
	c.result += value
}

func (c *Calculator) Subtract(value float64) {
	c.result -= value
}

func (c Calculator) GetResult() float64 {
	return c.result
}

func main() {
	// 기본 함수 호출
	fmt.Println("=== 기본 함수 ===")
	fmt.Println("5 + 3 =", add(5, 3))
	fmt.Println("5 * 3 =", multiply(5, 3))

	// 여러 값 반환
	fmt.Println("\n=== 여러 값 반환 ===")
	result, err := divide(10, 2)
	if err != nil {
		fmt.Println("에러:", err)
	} else {
		fmt.Println("10 / 2 =", result)
	}

	_, err = divide(10, 0)
	if err != nil {
		fmt.Println("에러:", err)
	}

	numbers := []int{5, 2, 9, 1, 7, 3}
	min, max := minMax(numbers)
	fmt.Printf("최소: %d, 최대: %d\n", min, max)

	// 이름 있는 반환값
	fmt.Println("\n=== 이름 있는 반환값 ===")
	area, perimeter := rectangle(5, 3)
	fmt.Printf("넓이: %.1f, 둘레: %.1f\n", area, perimeter)

	// 가변 인자
	fmt.Println("\n=== 가변 인자 ===")
	fmt.Println("sum(1, 2, 3) =", sum(1, 2, 3))
	fmt.Println("sum(1, 2, 3, 4, 5) =", sum(1, 2, 3, 4, 5))

	// 슬라이스를 가변 인자로 전달
	nums := []int{10, 20, 30}
	fmt.Println("sum(nums...) =", sum(nums...))

	printInfo("숫자", 1, 2, 3)
	printInfo("혼합", "문자열", 42, true, 3.14)

	// 함수를 값으로 사용
	fmt.Println("\n=== 함수를 값으로 ===")
	result1 := applyOperation(10, 5, add)
	result2 := applyOperation(10, 5, multiply)
	fmt.Println("10 + 5 =", result1)
	fmt.Println("10 * 5 =", result2)

	// 익명 함수
	subtract := func(a, b int) int {
		return a - b
	}
	result3 := applyOperation(10, 5, subtract)
	fmt.Println("10 - 5 =", result3)

	// 클로저
	fmt.Println("\n=== 클로저 ===")
	counter := makeCounter()
	fmt.Println("카운터:", counter()) // 1
	fmt.Println("카운터:", counter()) // 2
	fmt.Println("카운터:", counter()) // 3

	counter2 := makeCounter() // 새로운 카운터
	fmt.Println("새 카운터:", counter2()) // 1

	// 재귀 함수
	fmt.Println("\n=== 재귀 함수 ===")
	fmt.Println("5! =", factorial(5))
	fmt.Print("피보나치 수열 (0-10): ")
	for i := 0; i <= 10; i++ {
		fmt.Print(fibonacci(i), " ")
	}
	fmt.Println()

	// defer
	fmt.Println("\n=== defer ===")
	demonstrateDefer()

	fmt.Println()
	processFile("data.txt")

	// Calculator 사용
	fmt.Println("\n=== Calculator ===")
	calc := Calculator{}
	calc.Add(10)
	calc.Add(5)
	calc.Subtract(3)
	fmt.Println("결과:", calc.GetResult())
}

/*
연습 문제:
1. 두 수의 최대공약수(GCD)를 구하는 함수를 작성하세요
2. 문자열을 뒤집는 함수를 작성하세요
3. 슬라이스에서 중복을 제거하는 함수를 작성하세요
4. 주어진 숫자까지의 소수를 모두 반환하는 함수를 작성하세요
5. 클로저를 사용해서 간단한 은행 계좌를 구현하세요 (입금, 출금, 잔액 조회)

실행: go run 05-functions.go
*/

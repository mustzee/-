package main

import "fmt"

func main() {
	// === 변수 선언 방법 ===

	// 1. var 키워드로 선언
	var age int
	age = 25
	fmt.Println("나이:", age)

	// 2. 선언과 동시에 초기화
	var name string = "홍길동"
	fmt.Println("이름:", name)

	// 3. 타입 추론
	var city = "서울" // string 타입으로 자동 추론
	fmt.Println("도시:", city)

	// 4. 짧은 선언 := (함수 내부에서만 사용 가능)
	height := 175.5 // float64로 자동 추론
	fmt.Printf("키: %.1fcm\n", height)

	// 5. 여러 변수 동시 선언
	var (
		firstName = "길동"
		lastName  = "홍"
		birthYear = 1990
	)
	fmt.Printf("%s%s, %d년생\n", lastName, firstName, birthYear)

	// 6. 한 줄에 여러 변수
	x, y, z := 1, 2, 3
	fmt.Printf("x=%d, y=%d, z=%d\n", x, y, z)

	// === 상수 ===
	const Pi = 3.14159
	const Greeting = "안녕하세요"
	fmt.Println("원주율:", Pi)
	fmt.Println(Greeting)

	// 상수는 변경 불가능 (아래 줄의 주석을 제거하면 에러)
	// Pi = 3.14

	// 여러 상수 선언
	const (
		Monday    = 1
		Tuesday   = 2
		Wednesday = 3
	)
	fmt.Println("수요일:", Wednesday)

	// iota를 사용한 자동 증가 상수
	const (
		Red = iota   // 0
		Orange       // 1
		Yellow       // 2
		Green        // 3
		Blue         // 4
	)
	fmt.Printf("Blue = %d\n", Blue)

	// === 변수 재할당 ===
	count := 10
	fmt.Println("초기 count:", count)
	count = 20 // 재할당 가능
	fmt.Println("변경된 count:", count)

	// === 제로 값 (Zero Value) ===
	// 초기화하지 않은 변수는 타입별 기본값을 가짐
	var defaultInt int       // 0
	var defaultFloat float64 // 0.0
	var defaultBool bool     // false
	var defaultString string // ""
	fmt.Printf("int 기본값: %d\n", defaultInt)
	fmt.Printf("float64 기본값: %f\n", defaultFloat)
	fmt.Printf("bool 기본값: %t\n", defaultBool)
	fmt.Printf("string 기본값: '%s'\n", defaultString)
}

/*
연습 문제:
1. 자신의 정보(이름, 나이, 키, 체중)를 변수로 선언하고 출력하세요
2. iota를 사용해서 월(January=1, February=2, ...)을 상수로 정의하세요
3. 두 변수의 값을 서로 바꿔보세요 (swap)
4. 변수 하나를 선언하고 여러 번 값을 변경해보세요

실행: go run 02-variables.go
*/

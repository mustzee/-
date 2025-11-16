package main

import "fmt"

func main() {
	// === if 문 ===
	age := 20

	if age >= 18 {
		fmt.Println("성인입니다")
	}

	// if-else
	if age >= 65 {
		fmt.Println("경로 우대")
	} else if age >= 18 {
		fmt.Println("일반 성인")
	} else {
		fmt.Println("미성년자")
	}

	// if 문에서 짧은 선언문 사용
	if score := 85; score >= 90 {
		fmt.Println("A 학점")
	} else if score >= 80 {
		fmt.Println("B 학점")
	} else {
		fmt.Println("C 학점 이하")
	}
	// score는 if 블록 밖에서 사용 불가

	// === for 문 ===

	// 1. 기본 for 문
	fmt.Println("\n=== 1부터 5까지 ===")
	for i := 1; i <= 5; i++ {
		fmt.Println(i)
	}

	// 2. while처럼 사용
	fmt.Println("\n=== while 스타일 ===")
	count := 0
	for count < 3 {
		fmt.Println("count:", count)
		count++
	}

	// 3. 무한 루프
	// for {
	//     fmt.Println("무한 반복")
	//     break // break로 탈출
	// }

	// 4. continue와 break
	fmt.Println("\n=== continue와 break ===")
	for i := 0; i < 10; i++ {
		if i%2 == 0 {
			continue // 짝수는 건너뛰기
		}
		if i > 7 {
			break // 7보다 크면 중단
		}
		fmt.Println(i)
	}

	// 5. range를 사용한 반복
	numbers := []int{10, 20, 30, 40, 50}
	fmt.Println("\n=== range로 슬라이스 순회 ===")
	for index, value := range numbers {
		fmt.Printf("numbers[%d] = %d\n", index, value)
	}

	// 인덱스만 필요한 경우
	fmt.Println("\n=== 인덱스만 ===")
	for index := range numbers {
		fmt.Printf("인덱스: %d\n", index)
	}

	// 값만 필요한 경우
	fmt.Println("\n=== 값만 ===")
	for _, value := range numbers {
		fmt.Printf("값: %d\n", value)
	}

	// 문자열 순회
	fmt.Println("\n=== 문자열 순회 ===")
	text := "Hello, 한글"
	for index, char := range text {
		fmt.Printf("%d: %c\n", index, char)
	}

	// === switch 문 ===

	// 1. 기본 switch
	day := "월요일"
	fmt.Printf("\n오늘은 %s입니다. ", day)
	switch day {
	case "월요일":
		fmt.Println("한 주의 시작!")
	case "금요일":
		fmt.Println("불금!")
	case "토요일", "일요일":
		fmt.Println("주말!")
	default:
		fmt.Println("평일입니다")
	}

	// 2. 조건 없는 switch (if-else 체인 대체)
	temperature := 25
	fmt.Printf("\n현재 온도: %d°C - ", temperature)
	switch {
	case temperature < 0:
		fmt.Println("영하")
	case temperature < 10:
		fmt.Println("춥다")
	case temperature < 20:
		fmt.Println("시원하다")
	case temperature < 30:
		fmt.Println("따뜻하다")
	default:
		fmt.Println("덥다")
	}

	// 3. 타입 switch (인터페이스에서 사용, 중급 섹션에서 자세히)
	var x interface{} = 42
	fmt.Print("\nx의 타입: ")
	switch v := x.(type) {
	case int:
		fmt.Printf("정수 %d\n", v)
	case string:
		fmt.Printf("문자열 %s\n", v)
	case bool:
		fmt.Printf("불리언 %t\n", v)
	default:
		fmt.Printf("알 수 없는 타입 %T\n", v)
	}

	// 4. fallthrough (다음 케이스도 실행)
	num := 1
	fmt.Printf("\nnum = %d: ", num)
	switch num {
	case 1:
		fmt.Print("하나 ")
		fallthrough
	case 2:
		fmt.Print("둘 이하 ")
		fallthrough
	case 3:
		fmt.Print("셋 이하")
	}
	fmt.Println()

	// === 레이블과 goto (권장하지 않음) ===
	// goto는 가능한 사용하지 않는 것이 좋습니다

	// === 중첩 루프와 레이블 ===
	fmt.Println("\n=== 구구단 (2단, 3단만) ===")
OuterLoop:
	for i := 2; i <= 9; i++ {
		for j := 1; j <= 9; j++ {
			if i > 3 {
				break OuterLoop // 외부 루프 탈출
			}
			fmt.Printf("%d x %d = %d\n", i, j, i*j)
		}
		fmt.Println()
	}
}

/*
연습 문제:
1. 1부터 100까지 합을 계산하세요
2. 1부터 50까지 중 3의 배수만 출력하세요
3. 구구단 전체를 출력하세요
4. 주어진 숫자가 소수(prime)인지 판별하세요
5. FizzBuzz: 1부터 30까지 숫자 중
   - 3의 배수면 "Fizz"
   - 5의 배수면 "Buzz"
   - 둘 다면 "FizzBuzz"
   - 아니면 숫자 출력

실행: go run 04-control-flow.go
*/

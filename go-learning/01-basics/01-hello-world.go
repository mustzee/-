package main

import "fmt"

// main 함수는 프로그램의 진입점입니다
func main() {
	// fmt.Println은 표준 출력에 텍스트를 출력합니다
	fmt.Println("Hello, World!")
	fmt.Println("안녕하세요, Go 세계!")

	// 여러 값을 한 번에 출력
	fmt.Println("Go는", "간결하고", "강력합니다")

	// Printf로 포맷팅된 출력
	name := "Gopher"
	fmt.Printf("안녕하세요, %s님!\n", name)

	// 여러 줄 문자열
	message := `
	Go 언어의 특징:
	- 간결한 문법
	- 빠른 컴파일
	- 동시성 지원
	`
	fmt.Println(message)
}

/*
연습 문제:
1. 자신의 이름을 출력하는 코드를 추가하세요
2. Printf를 사용해서 "나이: 25세" 형식으로 출력하세요
3. 백틱(`)을 사용해서 여러 줄 메시지를 출력하세요

실행: go run 01-hello-world.go
*/

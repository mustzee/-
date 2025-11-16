package main

import "fmt"

func main() {
	// === 숫자 타입 ===

	// 정수형
	var i8 int8 = 127                    // -128 ~ 127
	var i16 int16 = 32767                // -32768 ~ 32767
	var i32 int32 = 2147483647           // -2^31 ~ 2^31-1
	var i64 int64 = 9223372036854775807  // -2^63 ~ 2^63-1
	var i int = 42                       // 시스템에 따라 32bit 또는 64bit

	fmt.Printf("int8: %d\n", i8)
	fmt.Printf("int16: %d\n", i16)
	fmt.Printf("int32: %d\n", i32)
	fmt.Printf("int64: %d\n", i64)
	fmt.Printf("int: %d\n", i)

	// 부호 없는 정수형
	var u8 uint8 = 255      // 0 ~ 255
	var u32 uint32 = 4294967295
	var u uint = 100

	fmt.Printf("uint8: %d\n", u8)
	fmt.Printf("uint32: %d\n", u32)
	fmt.Printf("uint: %d\n", u)

	// byte는 uint8의 별칭
	var b byte = 'A' // ASCII 65
	fmt.Printf("byte: %d (%c)\n", b, b)

	// rune은 int32의 별칭 (유니코드 코드 포인트)
	var r rune = '한'
	fmt.Printf("rune: %d (%c)\n", r, r)

	// 실수형
	var f32 float32 = 3.14
	var f64 float64 = 3.141592653589793
	fmt.Printf("float32: %.2f\n", f32)
	fmt.Printf("float64: %.15f\n", f64)

	// 복소수
	var c64 complex64 = 1 + 2i
	var c128 complex128 = 2 + 3i
	fmt.Printf("complex64: %v\n", c64)
	fmt.Printf("complex128: %v\n", c128)

	// === 불리언 타입 ===
	var isTrue bool = true
	var isFalse bool = false
	fmt.Printf("참: %t, 거짓: %t\n", isTrue, isFalse)

	// === 문자열 타입 ===
	var str string = "Hello, Go!"
	fmt.Println("문자열:", str)
	fmt.Println("길이:", len(str))
	fmt.Println("첫 바이트:", str[0])

	// 문자열 연결
	greeting := "안녕하세요"
	name := "Gopher"
	message := greeting + ", " + name + "님!"
	fmt.Println(message)

	// 여러 줄 문자열 (백틱 사용)
	multiline := `첫 번째 줄
두 번째 줄
세 번째 줄`
	fmt.Println(multiline)

	// === 타입 변환 ===
	var intVal int = 42
	var floatVal float64 = float64(intVal) // 명시적 변환 필요
	fmt.Printf("int: %d -> float64: %.2f\n", intVal, floatVal)

	var pi float64 = 3.14
	var truncated int = int(pi) // 소수점 버림
	fmt.Printf("float64: %.2f -> int: %d\n", pi, truncated)

	// 문자열과 숫자 변환은 strconv 패키지 사용
	// (중급 섹션에서 다룸)

	// === 타입 확인 ===
	fmt.Printf("i의 타입: %T\n", i)
	fmt.Printf("f64의 타입: %T\n", f64)
	fmt.Printf("str의 타입: %T\n", str)
	fmt.Printf("isTrue의 타입: %T\n", isTrue)

	// === 연산자 ===
	a, b := 10, 3

	// 산술 연산자
	fmt.Printf("%d + %d = %d\n", a, b, a+b)
	fmt.Printf("%d - %d = %d\n", a, b, a-b)
	fmt.Printf("%d * %d = %d\n", a, b, a*b)
	fmt.Printf("%d / %d = %d\n", a, b, a/b)    // 정수 나눗셈
	fmt.Printf("%d %% %d = %d\n", a, b, a%b)   // 나머지

	// 비교 연산자
	fmt.Printf("%d == %d: %t\n", a, b, a == b)
	fmt.Printf("%d != %d: %t\n", a, b, a != b)
	fmt.Printf("%d > %d: %t\n", a, b, a > b)
	fmt.Printf("%d < %d: %t\n", a, b, a < b)
	fmt.Printf("%d >= %d: %t\n", a, b, a >= b)
	fmt.Printf("%d <= %d: %t\n", a, b, a <= b)

	// 논리 연산자
	t, f := true, false
	fmt.Printf("true && false: %t\n", t && f)
	fmt.Printf("true || false: %t\n", t || f)
	fmt.Printf("!true: %t\n", !t)

	// 비트 연산자
	x, y := 12, 10 // 1100, 1010 (2진수)
	fmt.Printf("%d & %d = %d\n", x, y, x&y)    // AND
	fmt.Printf("%d | %d = %d\n", x, y, x|y)    // OR
	fmt.Printf("%d ^ %d = %d\n", x, y, x^y)    // XOR
	fmt.Printf("%d << 1 = %d\n", x, x<<1)      // 왼쪽 시프트
	fmt.Printf("%d >> 1 = %d\n", x, x>>1)      // 오른쪽 시프트
}

/*
연습 문제:
1. 섭씨 온도를 화씨로 변환하는 코드를 작성하세요 (F = C * 9/5 + 32)
2. 원의 반지름을 입력받아 넓이와 둘레를 계산하세요
3. 두 정수를 나눈 결과를 실수로 출력하세요
4. 비트 연산을 사용해서 짝수/홀수를 판별하세요

실행: go run 03-types.go
*/

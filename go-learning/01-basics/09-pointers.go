package main

import "fmt"

func main() {
	// === 포인터 기초 ===

	// 1. 포인터 선언
	var p *int // int를 가리키는 포인터 (초기값은 nil)
	fmt.Println("nil 포인터:", p)

	// 2. 변수의 주소 얻기 (&)
	x := 42
	p = &x // x의 주소를 p에 할당
	fmt.Printf("x의 값: %d\n", x)
	fmt.Printf("x의 주소: %p\n", &x)
	fmt.Printf("p가 가리키는 주소: %p\n", p)

	// 3. 포인터 역참조 (*)
	fmt.Printf("p가 가리키는 값: %d\n", *p)

	// 4. 포인터를 통한 값 변경
	*p = 100
	fmt.Printf("*p = 100 후:\n")
	fmt.Printf("  x: %d\n", x)
	fmt.Printf("  *p: %d\n", *p)

	// 5. 포인터와 일반 변수의 차이
	fmt.Println("\n=== 값 vs 포인터 ===")
	a := 10
	b := a     // 값 복사
	c := &a    // 주소 복사

	a = 20
	fmt.Printf("a: %d, b: %d, *c: %d\n", a, b, *c)

	// 6. new 함수
	fmt.Println("\n=== new 함수 ===")
	ptr := new(int) // int 타입의 제로 값을 가진 포인터 반환
	fmt.Printf("new(int): %p, 값: %d\n", ptr, *ptr)

	*ptr = 42
	fmt.Printf("값 할당 후: %d\n", *ptr)

	// 7. 함수에 값 전달 (call by value)
	fmt.Println("\n=== 값 전달 ===")
	num := 10
	fmt.Println("함수 호출 전:", num)
	modifyValue(num)
	fmt.Println("함수 호출 후:", num) // 변경되지 않음

	// 8. 함수에 포인터 전달 (call by reference)
	fmt.Println("\n=== 포인터 전달 ===")
	num2 := 10
	fmt.Println("함수 호출 전:", num2)
	modifyPointer(&num2)
	fmt.Println("함수 호출 후:", num2) // 변경됨

	// 9. 구조체와 포인터
	fmt.Println("\n=== 구조체 포인터 ===")
	type Person struct {
		Name string
		Age  int
	}

	person1 := Person{Name: "홍길동", Age: 25}
	person2 := person1 // 구조체 복사
	person2.Age = 30

	fmt.Printf("person1: %+v\n", person1) // Age: 25
	fmt.Printf("person2: %+v\n", person2) // Age: 30

	// 포인터로 전달
	personPtr := &person1
	personPtr.Age = 26 // (*personPtr).Age와 동일 (자동 역참조)

	fmt.Printf("person1 (수정 후): %+v\n", person1) // Age: 26
	fmt.Printf("personPtr: %+v\n", personPtr)

	// 10. 구조체 포인터 생성
	fmt.Println("\n=== 구조체 포인터 생성 ===")
	p1 := &Person{Name: "김철수", Age: 30}
	p2 := new(Person)
	p2.Name = "이영희"
	p2.Age = 28

	fmt.Printf("p1: %+v\n", p1)
	fmt.Printf("p2: %+v\n", p2)

	// 11. 슬라이스와 포인터
	fmt.Println("\n=== 슬라이스와 포인터 ===")
	// 슬라이스는 이미 참조 타입이므로 포인터가 필요 없음
	slice := []int{1, 2, 3}
	modifySlice(slice)
	fmt.Println("슬라이스 (수정 후):", slice) // 변경됨

	// 12. 맵과 포인터
	fmt.Println("\n=== 맵과 포인터 ===")
	// 맵도 참조 타입
	m := make(map[string]int)
	m["a"] = 1
	modifyMap(m)
	fmt.Println("맵 (수정 후):", m) // 변경됨

	// 13. 포인터의 포인터
	fmt.Println("\n=== 포인터의 포인터 ===")
	value := 100
	ptr1 := &value
	ptr2 := &ptr1

	fmt.Printf("value: %d\n", value)
	fmt.Printf("*ptr1: %d\n", *ptr1)
	fmt.Printf("**ptr2: %d\n", **ptr2)

	**ptr2 = 200
	fmt.Printf("**ptr2 = 200 후:\n")
	fmt.Printf("  value: %d\n", value)

	// 14. nil 포인터 체크
	fmt.Println("\n=== nil 포인터 체크 ===")
	var nilPtr *int
	if nilPtr == nil {
		fmt.Println("nilPtr는 nil입니다")
	}

	// nil 포인터 역참조는 패닉 발생
	// fmt.Println(*nilPtr) // 런타임 에러!

	// 안전한 포인터 사용
	if nilPtr != nil {
		fmt.Println("값:", *nilPtr)
	} else {
		fmt.Println("포인터가 nil이므로 역참조하지 않음")
	}

	// 15. 함수에서 포인터 반환
	fmt.Println("\n=== 함수에서 포인터 반환 ===")
	personPtr2 := createPerson("박민수", 32)
	fmt.Printf("생성된 사람: %+v\n", personPtr2)

	// 16. 메서드 리시버: 값 vs 포인터
	fmt.Println("\n=== 메서드 리시버 ===")
	type Counter struct {
		count int
	}

	// 값 리시버 - 복사본을 받음
	func(c Counter) incrementValue() {
		c.count++
	}

	// 포인터 리시버 - 원본을 받음
	func(c *Counter) incrementPointer() {
		c.count++
	}

	counter := Counter{count: 0}
	fmt.Println("초기값:", counter.count)

	counter.incrementValue()
	fmt.Println("값 리시버 후:", counter.count) // 0 (변경 안됨)

	counter.incrementPointer()
	fmt.Println("포인터 리시버 후:", counter.count) // 1 (변경됨)

	// 17. 실용 예제: swap 함수
	fmt.Println("\n=== Swap 함수 ===")
	a1, b1 := 10, 20
	fmt.Printf("swap 전: a=%d, b=%d\n", a1, b1)
	swap(&a1, &b1)
	fmt.Printf("swap 후: a=%d, b=%d\n", a1, b1)

	// 18. 배열과 포인터
	fmt.Println("\n=== 배열과 포인터 ===")
	arr := [3]int{1, 2, 3}
	fmt.Println("원본 배열:", arr)
	modifyArray(&arr)
	fmt.Println("수정 후 배열:", arr)

	// 배열을 값으로 전달하면 복사됨
	arr2 := [3]int{10, 20, 30}
	modifyArrayValue(arr2)
	fmt.Println("값 전달 후:", arr2) // 변경 안됨

	// 19. 포인터를 사용해야 하는 경우
	fmt.Println("\n=== 포인터 사용 시기 ===")
	// 1) 큰 구조체를 복사하지 않으려면
	type LargeStruct struct {
		data [1000]int
	}
	large := LargeStruct{}
	processLarge(&large) // 포인터로 전달 (효율적)

	// 2) 함수에서 값을 수정해야 하면
	val := 42
	doubleValue(&val)
	fmt.Println("2배 후:", val)

	// 3) nil 가능성을 표현하려면
	var optionalValue *int
	if optionalValue == nil {
		fmt.Println("값이 없습니다")
	}

	// 20. 포인터 비교
	fmt.Println("\n=== 포인터 비교 ===")
	x1, x2 := 42, 42
	px1, px2 := &x1, &x2
	px3 := &x1

	fmt.Println("px1 == px2:", px1 == px2) // false (다른 주소)
	fmt.Println("px1 == px3:", px1 == px3) // true (같은 주소)
	fmt.Println("*px1 == *px2:", *px1 == *px2) // true (값은 같음)
}

// === 도우미 함수들 ===

func modifyValue(n int) {
	n = 100
	fmt.Println("  함수 내부:", n)
}

func modifyPointer(n *int) {
	*n = 100
	fmt.Println("  함수 내부:", *n)
}

func modifySlice(s []int) {
	if len(s) > 0 {
		s[0] = 999
	}
}

func modifyMap(m map[string]int) {
	m["b"] = 2
}

type Person struct {
	Name string
	Age  int
}

func createPerson(name string, age int) *Person {
	p := Person{Name: name, Age: age}
	return &p // 로컬 변수의 주소를 반환해도 안전 (Go가 힙에 할당)
}

func swap(a, b *int) {
	*a, *b = *b, *a
}

func modifyArray(arr *[3]int) {
	arr[0] = 999
}

func modifyArrayValue(arr [3]int) {
	arr[0] = 888
}

type LargeStruct struct {
	data [1000]int
}

func processLarge(ls *LargeStruct) {
	// 포인터로 받아서 복사 오버헤드 없음
}

func doubleValue(n *int) {
	*n = *n * 2
}

/*
연습 문제:
1. 두 정수를 교환하는 swap 함수를 작성하세요
2. 구조체를 포인터로 받아서 필드를 수정하는 함수를 작성하세요
3. 슬라이스의 모든 요소를 2배로 만드는 함수를 작성하세요 (포인터 필요 없음)
4. 포인터를 사용해서 트리 구조를 만드세요
5. nil 체크를 포함한 안전한 포인터 역참조 함수를 작성하세요
6. 값 리시버와 포인터 리시버를 모두 가진 구조체를 만들어 차이를 확인하세요

주요 포인트:
- & : 주소 연산자 (address-of)
- * : 역참조 연산자 (dereference)
- 슬라이스, 맵, 채널은 이미 참조 타입
- nil 포인터 역참조는 런타임 패닉 발생
- 포인터 리시버는 원본 수정 가능

실행: go run 09-pointers.go
*/

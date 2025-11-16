package main

import (
	"fmt"
	"math"
)

// === 메서드 기초 ===
// 메서드는 특정 타입에 연결된 함수입니다

type Rectangle struct {
	Width  float64
	Height float64
}

// 값 리시버 메서드
func (r Rectangle) Area() float64 {
	return r.Width * r.Height
}

func (r Rectangle) Perimeter() float64 {
	return 2 * (r.Width + r.Height)
}

// 포인터 리시버 메서드
func (r *Rectangle) Scale(factor float64) {
	r.Width *= factor
	r.Height *= factor
}

func (r *Rectangle) SetWidth(width float64) {
	r.Width = width
}

// === 다양한 타입에 메서드 정의 ===

// 기본 타입에는 직접 메서드를 정의할 수 없으므로, 새로운 타입 선언
type MyInt int

func (m MyInt) IsEven() bool {
	return m%2 == 0
}

func (m MyInt) Double() MyInt {
	return m * 2
}

// 문자열 타입
type MyString string

func (s MyString) Length() int {
	return len(s)
}

func (s MyString) Upper() string {
	// 간단한 예제 (실제로는 strings.ToUpper 사용)
	return string(s) + "!"
}

// === 슬라이스 타입 메서드 ===
type IntSlice []int

func (s IntSlice) Sum() int {
	total := 0
	for _, v := range s {
		total += v
	}
	return total
}

func (s IntSlice) Average() float64 {
	if len(s) == 0 {
		return 0
	}
	return float64(s.Sum()) / float64(len(s))
}

// === 복잡한 예제: 원 ===
type Circle struct {
	Radius float64
}

func (c Circle) Area() float64 {
	return math.Pi * c.Radius * c.Radius
}

func (c Circle) Circumference() float64 {
	return 2 * math.Pi * c.Radius
}

func (c *Circle) Grow(amount float64) {
	c.Radius += amount
}

func (c *Circle) Shrink(amount float64) {
	c.Radius -= amount
	if c.Radius < 0 {
		c.Radius = 0
	}
}

// === 체인 가능한 메서드 ===
type Counter struct {
	value int
}

func (c *Counter) Increment() *Counter {
	c.value++
	return c
}

func (c *Counter) Decrement() *Counter {
	c.value--
	return c
}

func (c *Counter) Add(n int) *Counter {
	c.value += n
	return c
}

func (c *Counter) Value() int {
	return c.value
}

// === 메서드와 인터페이스 ===
// 인터페이스는 다음 파일에서 자세히 다루지만, 기본 개념 소개

type Shape interface {
	Area() float64
	Perimeter() float64
}

// Rectangle과 Square는 Shape 인터페이스를 구현
type Square struct {
	Side float64
}

func (s Square) Area() float64 {
	return s.Side * s.Side
}

func (s Square) Perimeter() float64 {
	return 4 * s.Side
}

// === 메서드 값과 메서드 표현식 ===
type Person struct {
	Name string
	Age  int
}

func (p Person) Greet() string {
	return fmt.Sprintf("안녕하세요, 저는 %s입니다.", p.Name)
}

func (p *Person) HaveBirthday() {
	p.Age++
}

func main() {
	// === 기본 메서드 사용 ===
	fmt.Println("=== Rectangle ===")
	rect := Rectangle{Width: 10, Height: 5}
	fmt.Printf("직사각형: %.1f x %.1f\n", rect.Width, rect.Height)
	fmt.Printf("넓이: %.1f\n", rect.Area())
	fmt.Printf("둘레: %.1f\n", rect.Perimeter())

	// 포인터 리시버 메서드
	rect.Scale(2)
	fmt.Printf("2배 확대 후: %.1f x %.1f\n", rect.Width, rect.Height)
	fmt.Printf("새 넓이: %.1f\n", rect.Area())

	// === 값 리시버 vs 포인터 리시버 ===
	fmt.Println("\n=== 값 vs 포인터 리시버 ===")
	rect2 := Rectangle{Width: 5, Height: 3}

	// 값 리시버는 복사본을 받음
	area := rect2.Area() // rect2는 변경되지 않음
	fmt.Printf("넓이: %.1f\n", area)

	// 포인터 리시버는 원본을 수정
	rect2.Scale(3)
	fmt.Printf("3배 확대 후: %.1f x %.1f\n", rect2.Width, rect2.Height)

	// Go는 자동으로 & 또는 *를 추가
	(&rect2).Scale(2)  // 명시적
	rect2.Scale(2)     // 암시적 (같은 동작)

	// === 사용자 정의 타입 메서드 ===
	fmt.Println("\n=== 사용자 정의 타입 ===")
	var num MyInt = 42
	fmt.Printf("%d는 짝수? %t\n", num, num.IsEven())
	fmt.Printf("%d의 2배: %d\n", num, num.Double())

	str := MyString("Hello")
	fmt.Printf("길이: %d\n", str.Length())
	fmt.Printf("변환: %s\n", str.Upper())

	// === 슬라이스 메서드 ===
	fmt.Println("\n=== 슬라이스 메서드 ===")
	numbers := IntSlice{1, 2, 3, 4, 5}
	fmt.Printf("숫자: %v\n", numbers)
	fmt.Printf("합계: %d\n", numbers.Sum())
	fmt.Printf("평균: %.2f\n", numbers.Average())

	// === Circle 예제 ===
	fmt.Println("\n=== Circle ===")
	circle := Circle{Radius: 5}
	fmt.Printf("반지름: %.1f\n", circle.Radius)
	fmt.Printf("넓이: %.2f\n", circle.Area())
	fmt.Printf("둘레: %.2f\n", circle.Circumference())

	circle.Grow(3)
	fmt.Printf("3 증가 후 반지름: %.1f\n", circle.Radius)

	circle.Shrink(2)
	fmt.Printf("2 감소 후 반지름: %.1f\n", circle.Radius)

	// === 메서드 체이닝 ===
	fmt.Println("\n=== 메서드 체이닝 ===")
	counter := &Counter{}
	result := counter.Increment().Increment().Add(5).Decrement().Value()
	fmt.Printf("체이닝 결과: %d\n", result)

	// === 다형성 (인터페이스와 함께) ===
	fmt.Println("\n=== 다형성 ===")
	shapes := []Shape{
		Rectangle{Width: 10, Height: 5},
		Square{Side: 7},
	}

	for i, shape := range shapes {
		fmt.Printf("도형 %d:\n", i+1)
		fmt.Printf("  넓이: %.2f\n", shape.Area())
		fmt.Printf("  둘레: %.2f\n", shape.Perimeter())
	}

	// === 메서드 값 ===
	fmt.Println("\n=== 메서드 값 ===")
	person := Person{Name: "홍길동", Age: 25}

	// 메서드를 변수에 할당
	greetFunc := person.Greet
	fmt.Println(greetFunc())

	// 메서드 표현식
	greetFunc2 := Person.Greet
	fmt.Println(greetFunc2(person))

	// === 포인터와 값의 자동 변환 ===
	fmt.Println("\n=== 자동 변환 ===")
	p1 := Person{Name: "김철수", Age: 30}
	p2 := &Person{Name: "이영희", Age: 28}

	// 값으로 메서드 호출
	fmt.Println(p1.Greet())

	// 포인터로 메서드 호출 (자동으로 역참조)
	fmt.Println(p2.Greet())

	// 포인터 리시버 메서드
	p1.HaveBirthday() // Go가 자동으로 &p1로 변환
	fmt.Printf("%s의 새 나이: %d\n", p1.Name, p1.Age)

	p2.HaveBirthday()
	fmt.Printf("%s의 새 나이: %d\n", p2.Name, p2.Age)

	// === 언제 포인터 리시버를 사용할까? ===
	fmt.Println("\n=== 포인터 리시버 사용 시기 ===")
	fmt.Println("1. 메서드가 리시버를 수정해야 할 때")
	fmt.Println("2. 리시버가 큰 구조체일 때 (복사 오버헤드 방지)")
	fmt.Println("3. 일관성: 일부 메서드가 포인터 리시버면 모두 포인터로")
}

/*
메서드 vs 함수:

함수:
  func Area(r Rectangle) float64 {
      return r.Width * r.Height
  }
  사용: Area(rect)

메서드:
  func (r Rectangle) Area() float64 {
      return r.Width * r.Height
  }
  사용: rect.Area()

포인터 리시버를 사용해야 하는 경우:
1. 메서드가 리시버가 가리키는 값을 수정해야 할 때
2. 리시버가 큰 구조체일 때 (복사 비용 절감)
3. 일관성: 타입의 일부 메서드가 포인터 리시버를 가지면,
   모든 메서드가 포인터 리시버를 가져야 함

값 리시버를 사용해야 하는 경우:
1. 리시버를 수정할 필요가 없을 때
2. 리시버가 작은 값 타입일 때
3. 리시버가 맵, 함수, 채널일 때

연습 문제:
1. Triangle 구조체를 만들고 넓이와 둘레를 계산하는 메서드를 추가하세요
2. 온도를 나타내는 타입을 만들고 섭씨를 화씨로 변환하는 메서드를 작성하세요
3. Stack 타입을 만들고 Push, Pop, Peek 메서드를 구현하세요
4. 문자열 슬라이스 타입에 Join 메서드를 추가하세요
5. BankAccount 구조체를 만들고 Deposit, Withdraw 메서드를 구현하세요

실행: go run 01-methods.go
*/

package main

import (
	"fmt"
	"math"
)

// === 인터페이스 기초 ===
// 인터페이스는 메서드의 집합을 정의합니다

type Shape interface {
	Area() float64
	Perimeter() float64
}

type Rectangle struct {
	Width, Height float64
}

func (r Rectangle) Area() float64 {
	return r.Width * r.Height
}

func (r Rectangle) Perimeter() float64 {
	return 2 * (r.Width + r.Height)
}

type Circle struct {
	Radius float64
}

func (c Circle) Area() float64 {
	return math.Pi * c.Radius * c.Radius
}

func (c Circle) Perimeter() float64 {
	return 2 * math.Pi * c.Radius
}

// Shape 인터페이스를 받는 함수
func PrintShapeInfo(s Shape) {
	fmt.Printf("넓이: %.2f\n", s.Area())
	fmt.Printf("둘레: %.2f\n", s.Perimeter())
}

// === 빈 인터페이스 ===
// interface{}는 모든 타입을 받을 수 있습니다

func PrintAnything(v interface{}) {
	fmt.Printf("값: %v, 타입: %T\n", v, v)
}

// === 타입 단언 (Type Assertion) ===
func DescribeValue(v interface{}) {
	// 타입 단언
	if str, ok := v.(string); ok {
		fmt.Printf("문자열: %s (길이: %d)\n", str, len(str))
		return
	}

	if num, ok := v.(int); ok {
		fmt.Printf("정수: %d\n", num)
		return
	}

	fmt.Printf("알 수 없는 타입: %T\n", v)
}

// === 타입 스위치 ===
func TypeSwitch(v interface{}) {
	switch val := v.(type) {
	case int:
		fmt.Printf("정수: %d\n", val)
	case string:
		fmt.Printf("문자열: %s\n", val)
	case bool:
		fmt.Printf("불리언: %t\n", val)
	case Rectangle:
		fmt.Printf("직사각형: %.1f x %.1f\n", val.Width, val.Height)
	case Circle:
		fmt.Printf("원: 반지름 %.1f\n", val.Radius)
	case []int:
		fmt.Printf("정수 슬라이스: %v\n", val)
	default:
		fmt.Printf("알 수 없는 타입: %T\n", val)
	}
}

// === 여러 인터페이스 ===
type Stringer interface {
	String() string
}

type Person struct {
	Name string
	Age  int
}

func (p Person) String() string {
	return fmt.Sprintf("%s (%d세)", p.Name, p.Age)
}

// === 인터페이스 조합 ===
type Reader interface {
	Read() string
}

type Writer interface {
	Write(s string)
}

type ReadWriter interface {
	Reader
	Writer
}

type File struct {
	content string
}

func (f *File) Read() string {
	return f.content
}

func (f *File) Write(s string) {
	f.content = s
}

// === 실용 예제: 동물 ===
type Animal interface {
	Speak() string
	Move() string
}

type Dog struct {
	Name string
}

func (d Dog) Speak() string {
	return "멍멍!"
}

func (d Dog) Move() string {
	return "네 발로 걷습니다"
}

type Bird struct {
	Name string
}

func (b Bird) Speak() string {
	return "짹짹!"
}

func (b Bird) Move() string {
	return "날아갑니다"
}

func AnimalInfo(a Animal) {
	fmt.Printf("소리: %s\n", a.Speak())
	fmt.Printf("이동: %s\n", a.Move())
}

// === 인터페이스를 통한 의존성 주입 ===
type Database interface {
	Save(data string) error
	Load(id string) (string, error)
}

type MemoryDB struct {
	data map[string]string
}

func NewMemoryDB() *MemoryDB {
	return &MemoryDB{data: make(map[string]string)}
}

func (m *MemoryDB) Save(id string, data string) error {
	m.data[id] = data
	return nil
}

func (m *MemoryDB) Load(id string) (string, error) {
	if data, exists := m.data[id]; exists {
		return data, nil
	}
	return "", fmt.Errorf("데이터를 찾을 수 없습니다: %s", id)
}

// === 표준 라이브러리 인터페이스 예제 ===

// fmt.Stringer 인터페이스 구현
type Point struct {
	X, Y int
}

func (p Point) String() string {
	return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

// error 인터페이스 구현
type MyError struct {
	Code    int
	Message string
}

func (e MyError) Error() string {
	return fmt.Sprintf("에러 %d: %s", e.Code, e.Message)
}

// === 빈 인터페이스 활용 ===
type Container struct {
	items []interface{}
}

func (c *Container) Add(item interface{}) {
	c.items = append(c.items, item)
}

func (c *Container) Get(index int) interface{} {
	if index >= 0 && index < len(c.items) {
		return c.items[index]
	}
	return nil
}

func main() {
	// === 기본 인터페이스 사용 ===
	fmt.Println("=== Shape 인터페이스 ===")
	rect := Rectangle{Width: 10, Height: 5}
	circle := Circle{Radius: 7}

	PrintShapeInfo(rect)
	fmt.Println()
	PrintShapeInfo(circle)

	// 인터페이스 슬라이스
	fmt.Println("\n=== 도형 목록 ===")
	shapes := []Shape{
		Rectangle{Width: 5, Height: 3},
		Circle{Radius: 4},
		Rectangle{Width: 8, Height: 2},
	}

	for i, shape := range shapes {
		fmt.Printf("도형 %d: 넓이=%.2f, 둘레=%.2f\n", i+1, shape.Area(), shape.Perimeter())
	}

	// === 빈 인터페이스 ===
	fmt.Println("\n=== 빈 인터페이스 ===")
	PrintAnything(42)
	PrintAnything("Hello")
	PrintAnything(true)
	PrintAnything([]int{1, 2, 3})
	PrintAnything(rect)

	// === 타입 단언 ===
	fmt.Println("\n=== 타입 단언 ===")
	DescribeValue("Go 언어")
	DescribeValue(42)
	DescribeValue(3.14)

	// === 타입 스위치 ===
	fmt.Println("\n=== 타입 스위치 ===")
	values := []interface{}{
		42,
		"Hello",
		true,
		Rectangle{Width: 5, Height: 3},
		Circle{Radius: 2},
		[]int{1, 2, 3},
	}

	for _, v := range values {
		TypeSwitch(v)
	}

	// === Stringer 인터페이스 ===
	fmt.Println("\n=== Stringer ===")
	person := Person{Name: "홍길동", Age: 25}
	fmt.Println(person) // String() 메서드가 자동 호출됨

	// === ReadWriter 인터페이스 ===
	fmt.Println("\n=== ReadWriter ===")
	file := &File{}
	file.Write("Hello, Go!")
	fmt.Println("파일 내용:", file.Read())

	// === Animal 인터페이스 ===
	fmt.Println("\n=== Animal ===")
	dog := Dog{Name: "바둑이"}
	bird := Bird{Name: "짹짹이"}

	fmt.Println("강아지:")
	AnimalInfo(dog)
	fmt.Println("\n새:")
	AnimalInfo(bird)

	// === 인터페이스 값 ===
	fmt.Println("\n=== 인터페이스 값 ===")
	var s Shape
	fmt.Printf("nil 인터페이스: %v, nil? %t\n", s, s == nil)

	s = Rectangle{Width: 10, Height: 5}
	fmt.Printf("값 할당 후: %v, nil? %t\n", s, s == nil)

	// 인터페이스 내부 확인
	fmt.Printf("타입: %T, 값: %v\n", s, s)

	// === 포인터와 인터페이스 ===
	fmt.Println("\n=== 포인터와 인터페이스 ===")
	var rw ReadWriter
	rw = &File{} // File의 메서드가 포인터 리시버이므로 포인터 필요
	rw.Write("포인터로 할당")
	fmt.Println(rw.Read())

	// === Point (fmt.Stringer) ===
	fmt.Println("\n=== Point (Stringer) ===")
	p := Point{X: 10, Y: 20}
	fmt.Println("점:", p) // String() 메서드 호출됨
	fmt.Printf("출력: %v\n", p)

	// === 커스텀 에러 ===
	fmt.Println("\n=== 커스텀 에러 ===")
	err := MyError{Code: 404, Message: "페이지를 찾을 수 없습니다"}
	fmt.Println("에러:", err)

	// error 인터페이스로 사용
	var e error = err
	fmt.Println("error 인터페이스:", e)

	// === 빈 인터페이스 컨테이너 ===
	fmt.Println("\n=== 범용 컨테이너 ===")
	container := &Container{}
	container.Add(42)
	container.Add("Hello")
	container.Add(true)
	container.Add(Rectangle{Width: 5, Height: 3})

	for i := 0; i < 4; i++ {
		item := container.Get(i)
		fmt.Printf("%d: %v (타입: %T)\n", i, item, item)
	}

	// === 인터페이스 체크 ===
	fmt.Println("\n=== 인터페이스 체크 ===")
	var any interface{} = "Hello"

	// 인터페이스가 특정 타입을 구현하는지 체크
	if _, ok := any.(string); ok {
		fmt.Println("any는 string 타입입니다")
	}

	// 구조체가 인터페이스를 구현하는지 컴파일 타임 체크
	var _ Shape = Rectangle{} // 컴파일 에러가 나면 Shape를 구현하지 않은 것
	var _ Shape = Circle{}

	fmt.Println("Rectangle과 Circle은 Shape를 구현합니다")
}

/*
인터페이스 핵심 개념:

1. 암시적 구현:
   - Go의 인터페이스는 암시적으로 구현됩니다
   - "implements" 키워드가 없음
   - 메서드만 일치하면 자동으로 인터페이스 구현

2. 빈 인터페이스 (interface{}):
   - 메서드가 없는 인터페이스
   - 모든 타입이 자동으로 구현
   - 타입 안전성을 잃지만 유연성 증가

3. 인터페이스 값:
   - (타입, 값) 쌍으로 저장됨
   - nil 인터페이스: 타입과 값이 모두 nil
   - 구체적인 값이 nil이어도 인터페이스는 nil이 아님

4. 인터페이스 사용 시기:
   - 여러 타입이 같은 동작을 공유할 때
   - 의존성 주입과 테스트 가능성
   - 다형성 구현

연습 문제:
1. Vehicle 인터페이스를 만들고 Car, Motorcycle로 구현하세요
2. 타입 스위치를 사용해서 JSON 변환 함수를 만드세요
3. Reader와 Writer를 결합한 Copier 인터페이스를 구현하세요
4. error 인터페이스를 구현하는 커스텀 에러 타입을 만드세요
5. sort.Interface를 구현하여 커스텀 정렬을 구현하세요

실행: go run 02-interfaces.go
*/

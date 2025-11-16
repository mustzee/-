package main

import (
	"fmt"
	"time"
)

// === 기본 구조체 정의 ===
type Person struct {
	Name string
	Age  int
	City string
}

// === 필드 태그가 있는 구조체 ===
type Employee struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	Email     string `json:"email"`
	Salary    int    `json:"salary,omitempty"`
}

// === 임베디드 구조체 ===
type Address struct {
	Street  string
	City    string
	ZipCode string
}

type Contact struct {
	Phone string
	Email string
}

type Customer struct {
	Name    string
	Address // 임베디드 (필드명 없이 타입만)
	Contact // 임베디드
}

// === 메서드가 있는 구조체 ===
type Rectangle struct {
	Width  float64
	Height float64
}

// 값 리시버 메서드
func (r Rectangle) Area() float64 {
	return r.Width * r.Height
}

// 포인터 리시버 메서드
func (r *Rectangle) Scale(factor float64) {
	r.Width *= factor
	r.Height *= factor
}

// === 생성자 함수 패턴 ===
func NewPerson(name string, age int) *Person {
	return &Person{
		Name: name,
		Age:  age,
		City: "서울", // 기본값
	}
}

// === 빈 구조체 ===
type Empty struct{}

func main() {
	// 1. 구조체 생성 - 기본
	var p1 Person
	fmt.Println("기본 Person:", p1) // 제로 값

	// 2. 필드 초기화
	p2 := Person{
		Name: "홍길동",
		Age:  25,
		City: "서울",
	}
	fmt.Println("p2:", p2)

	// 3. 필드 순서대로 초기화 (권장하지 않음)
	p3 := Person{"김철수", 30, "부산"}
	fmt.Println("p3:", p3)

	// 4. 일부 필드만 초기화
	p4 := Person{
		Name: "이영희",
		Age:  28,
		// City는 빈 문자열로 초기화됨
	}
	fmt.Println("p4:", p4)

	// 5. 필드 접근 및 수정
	p2.Age = 26
	fmt.Printf("%s의 나이: %d\n", p2.Name, p2.Age)

	// 6. 구조체 포인터
	pp := &Person{
		Name: "박민수",
		Age:  32,
		City: "대구",
	}
	fmt.Println("포인터:", pp)
	fmt.Println("역참조:", *pp)

	// Go는 자동으로 역참조
	fmt.Println("pp.Name:", pp.Name) // (*pp).Name과 동일

	// 7. new로 구조체 생성
	p5 := new(Person) // 제로 값으로 초기화된 포인터 반환
	p5.Name = "최영수"
	p5.Age = 35
	fmt.Println("new로 생성:", p5)

	// 8. 익명 구조체
	fmt.Println("\n=== 익명 구조체 ===")
	book := struct {
		Title  string
		Author string
		Pages  int
	}{
		Title:  "Go 프로그래밍",
		Author: "홍길동",
		Pages:  300,
	}
	fmt.Printf("책: %s, 저자: %s, 페이지: %d\n", book.Title, book.Author, book.Pages)

	// 9. 구조체 비교
	fmt.Println("\n=== 구조체 비교 ===")
	person1 := Person{"홍길동", 25, "서울"}
	person2 := Person{"홍길동", 25, "서울"}
	person3 := Person{"김철수", 30, "부산"}

	fmt.Println("person1 == person2:", person1 == person2) // true
	fmt.Println("person1 == person3:", person1 == person3) // false

	// 10. 구조체 복사
	fmt.Println("\n=== 구조체 복사 ===")
	original := Person{"원본", 20, "서울"}
	copied := original // 값 복사
	copied.Name = "복사본"

	fmt.Println("original:", original)
	fmt.Println("copied:", copied)

	// 포인터는 같은 구조체를 가리킴
	ptr1 := &Person{"참조", 25, "부산"}
	ptr2 := ptr1
	ptr2.Name = "수정됨"

	fmt.Println("ptr1:", ptr1)
	fmt.Println("ptr2:", ptr2)

	// 11. 임베디드 구조체
	fmt.Println("\n=== 임베디드 구조체 ===")
	customer := Customer{
		Name: "홍길동",
		Address: Address{
			Street:  "강남대로 123",
			City:    "서울",
			ZipCode: "12345",
		},
		Contact: Contact{
			Phone: "010-1234-5678",
			Email: "hong@example.com",
		},
	}

	// 임베디드 필드는 직접 접근 가능
	fmt.Println("이름:", customer.Name)
	fmt.Println("도시:", customer.City)    // customer.Address.City도 가능
	fmt.Println("전화:", customer.Phone)   // customer.Contact.Phone도 가능
	fmt.Println("전체:", customer)

	// 12. 메서드 사용
	fmt.Println("\n=== 메서드 ===")
	rect := Rectangle{Width: 10, Height: 5}
	fmt.Printf("직사각형: %.1f x %.1f\n", rect.Width, rect.Height)
	fmt.Printf("넓이: %.1f\n", rect.Area())

	rect.Scale(2)
	fmt.Printf("2배 확대: %.1f x %.1f\n", rect.Width, rect.Height)
	fmt.Printf("새 넓이: %.1f\n", rect.Area())

	// 13. 생성자 함수 사용
	fmt.Println("\n=== 생성자 함수 ===")
	p6 := NewPerson("박영희", 27)
	fmt.Println("생성자로 생성:", p6)

	// 14. 구조체 슬라이스
	fmt.Println("\n=== 구조체 슬라이스 ===")
	people := []Person{
		{Name: "홍길동", Age: 25, City: "서울"},
		{Name: "김철수", Age: 30, City: "부산"},
		{Name: "이영희", Age: 28, City: "대구"},
	}

	for i, person := range people {
		fmt.Printf("%d. %s (%d세, %s)\n", i+1, person.Name, person.Age, person.City)
	}

	// 15. 구조체 맵
	fmt.Println("\n=== 구조체 맵 ===")
	employees := map[int]Employee{
		101: {ID: 101, Name: "홍길동", Email: "hong@company.com", Salary: 5000},
		102: {ID: 102, Name: "김철수", Email: "kim@company.com", Salary: 6000},
	}

	for id, emp := range employees {
		fmt.Printf("ID %d: %s (%s)\n", id, emp.Name, emp.Email)
	}

	// 16. 중첩 구조체
	fmt.Println("\n=== 중첩 구조체 ===")
	type Department struct {
		Name    string
		Manager Person
	}

	type Company struct {
		Name        string
		Departments []Department
	}

	company := Company{
		Name: "테크 회사",
		Departments: []Department{
			{
				Name:    "개발팀",
				Manager: Person{Name: "홍길동", Age: 35, City: "서울"},
			},
			{
				Name:    "마케팅팀",
				Manager: Person{Name: "김철수", Age: 40, City: "부산"},
			},
		},
	}

	fmt.Printf("회사: %s\n", company.Name)
	for _, dept := range company.Departments {
		fmt.Printf("  %s - 매니저: %s\n", dept.Name, dept.Manager.Name)
	}

	// 17. 실용 예제: 시간 추적
	fmt.Println("\n=== 실용 예제: 타임스탬프 ===")
	type Event struct {
		Name      string
		Timestamp time.Time
		Data      map[string]interface{}
	}

	event := Event{
		Name:      "사용자 로그인",
		Timestamp: time.Now(),
		Data: map[string]interface{}{
			"user_id": 12345,
			"ip":      "192.168.1.1",
		},
	}

	fmt.Printf("이벤트: %s\n", event.Name)
	fmt.Printf("시간: %s\n", event.Timestamp.Format("2006-01-02 15:04:05"))
	fmt.Printf("데이터: %v\n", event.Data)

	// 18. 빈 구조체 사용 (메모리 효율)
	fmt.Println("\n=== 빈 구조체 ===")
	set := make(map[string]Empty)
	set["apple"] = Empty{}
	set["banana"] = Empty{}

	if _, exists := set["apple"]; exists {
		fmt.Println("apple이 집합에 있습니다")
	}

	// 19. 메서드 체이닝
	fmt.Println("\n=== 메서드 체이닝 ===")
	type Builder struct {
		result string
	}

	func (b *Builder) Add(s string) *Builder {
		b.result += s
		return b
	}

	func (b *Builder) AddSpace() *Builder {
		b.result += " "
		return b
	}

	func (b *Builder) Build() string {
		return b.result
	}

	builder := &Builder{}
	result := builder.Add("Hello").AddSpace().Add("World").Build()
	fmt.Println("체이닝 결과:", result)
}

/*
연습 문제:
1. 학생 구조체를 만들고 (이름, 학번, 성적), 여러 학생의 평균 성적을 계산하세요
2. 원(Circle) 구조체를 만들고 넓이와 둘레를 계산하는 메서드를 추가하세요
3. 책(Book) 구조체를 만들고, 도서관(Library)을 구조체 슬라이스로 구현하세요
4. 은행 계좌(Account) 구조체를 만들고 입금, 출금 메서드를 구현하세요
5. Point 구조체를 만들고 두 점 사이의 거리를 계산하는 메서드를 작성하세요
6. 이름, 나이를 필드로 가진 구조체를 나이순으로 정렬하세요

실행: go run 08-structs.go
*/

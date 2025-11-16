package main

import (
	"encoding/json"
	"fmt"
	"os"
)

// === 기본 구조체 ===

type Person struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
	City string `json:"city"`
}

// === 다양한 태그 옵션 ===

type User struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"-"`              // JSON에서 제외
	Bio      string `json:"bio,omitempty"` // 빈 값이면 생략
}

// === 중첩 구조체 ===

type Address struct {
	Street  string `json:"street"`
	City    string `json:"city"`
	ZipCode string `json:"zip_code"`
}

type Employee struct {
	Name    string  `json:"name"`
	Age     int     `json:"age"`
	Address Address `json:"address"`
}

// === 슬라이스와 맵 ===

type Team struct {
	Name    string   `json:"name"`
	Members []string `json:"members"`
	Scores  map[string]int `json:"scores"`
}

// === 커스텀 JSON 마샬링 ===

type CustomDate struct {
	Year  int `json:"year"`
	Month int `json:"month"`
	Day   int `json:"day"`
}

func (cd CustomDate) MarshalJSON() ([]byte, error) {
	formatted := fmt.Sprintf(`"%04d-%02d-%02d"`, cd.Year, cd.Month, cd.Day)
	return []byte(formatted), nil
}

func (cd *CustomDate) UnmarshalJSON(data []byte) error {
	var dateStr string
	if err := json.Unmarshal(data, &dateStr); err != nil {
		return err
	}
	fmt.Sscanf(dateStr, "%d-%d-%d", &cd.Year, &cd.Month, &cd.Day)
	return nil
}

type Event struct {
	Name string     `json:"name"`
	Date CustomDate `json:"date"`
}

func main() {
	// === 마샬링 (Go -> JSON) ===
	fmt.Println("=== 마샬링 (Go -> JSON) ===")

	person := Person{
		Name: "홍길동",
		Age:  25,
		City: "서울",
	}

	// 1. json.Marshal
	jsonData, err := json.Marshal(person)
	if err != nil {
		fmt.Println("마샬링 에러:", err)
		return
	}
	fmt.Println("JSON:", string(jsonData))

	// 2. json.MarshalIndent (들여쓰기)
	jsonPretty, err := json.MarshalIndent(person, "", "  ")
	if err != nil {
		fmt.Println("에러:", err)
		return
	}
	fmt.Println("\n예쁜 JSON:")
	fmt.Println(string(jsonPretty))

	// === 언마샬링 (JSON -> Go) ===
	fmt.Println("\n=== 언마샬링 (JSON -> Go) ===")

	jsonStr := `{"name":"김철수","age":30,"city":"부산"}`
	var person2 Person

	err = json.Unmarshal([]byte(jsonStr), &person2)
	if err != nil {
		fmt.Println("언마샬링 에러:", err)
		return
	}
	fmt.Printf("이름: %s, 나이: %d, 도시: %s\n", person2.Name, person2.Age, person2.City)

	// === JSON 태그 ===
	fmt.Println("\n=== JSON 태그 ===")

	user := User{
		ID:       1,
		Username: "gopher",
		Email:    "gopher@example.com",
		Password: "secret123", // JSON에 포함되지 않음
		Bio:      "",           // omitempty로 생략됨
	}

	userJSON, _ := json.MarshalIndent(user, "", "  ")
	fmt.Println("User JSON:")
	fmt.Println(string(userJSON))

	user2 := User{
		ID:       2,
		Username: "admin",
		Email:    "admin@example.com",
		Bio:      "관리자",
	}

	user2JSON, _ := json.MarshalIndent(user2, "", "  ")
	fmt.Println("\nUser2 JSON (bio 포함):")
	fmt.Println(string(user2JSON))

	// === 중첩 구조체 ===
	fmt.Println("\n=== 중첩 구조체 ===")

	employee := Employee{
		Name: "이영희",
		Age:  28,
		Address: Address{
			Street:  "강남대로 123",
			City:    "서울",
			ZipCode: "12345",
		},
	}

	empJSON, _ := json.MarshalIndent(employee, "", "  ")
	fmt.Println(string(empJSON))

	// === 슬라이스와 맵 ===
	fmt.Println("\n=== 슬라이스와 맵 ===")

	team := Team{
		Name:    "개발팀",
		Members: []string{"홍길동", "김철수", "이영희"},
		Scores: map[string]int{
			"Q1": 85,
			"Q2": 90,
			"Q3": 88,
		},
	}

	teamJSON, _ := json.MarshalIndent(team, "", "  ")
	fmt.Println(string(teamJSON))

	// 언마샬링
	var team2 Team
	json.Unmarshal(teamJSON, &team2)
	fmt.Printf("\n팀명: %s\n", team2.Name)
	fmt.Println("멤버:", team2.Members)
	fmt.Println("점수:", team2.Scores)

	// === 맵으로 JSON 다루기 ===
	fmt.Println("\n=== 맵으로 JSON 다루기 ===")

	jsonMap := `{
		"name": "박민수",
		"age": 32,
		"married": true,
		"hobbies": ["독서", "운동", "코딩"]
	}`

	var data map[string]interface{}
	json.Unmarshal([]byte(jsonMap), &data)

	fmt.Println("이름:", data["name"])
	fmt.Println("나이:", data["age"])
	fmt.Println("결혼:", data["married"])
	fmt.Println("취미:", data["hobbies"])

	// === 배열/슬라이스 ===
	fmt.Println("\n=== JSON 배열 ===")

	people := []Person{
		{Name: "홍길동", Age: 25, City: "서울"},
		{Name: "김철수", Age: 30, City: "부산"},
		{Name: "이영희", Age: 28, City: "대구"},
	}

	peopleJSON, _ := json.MarshalIndent(people, "", "  ")
	fmt.Println(string(peopleJSON))

	// 언마샬링
	var people2 []Person
	json.Unmarshal(peopleJSON, &people2)
	for _, p := range people2 {
		fmt.Printf("%s (%d세, %s)\n", p.Name, p.Age, p.City)
	}

	// === 파일로 저장 ===
	fmt.Println("\n=== 파일로 JSON 저장 ===")

	file, err := os.Create("data.json")
	if err != nil {
		fmt.Println("파일 생성 에러:", err)
		return
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	err = encoder.Encode(people)
	if err != nil {
		fmt.Println("인코딩 에러:", err)
		return
	}
	fmt.Println("data.json 저장 완료")

	// === 파일에서 읽기 ===
	fmt.Println("\n=== 파일에서 JSON 읽기 ===")

	file2, err := os.Open("data.json")
	if err != nil {
		fmt.Println("파일 열기 에러:", err)
		return
	}
	defer file2.Close()

	var people3 []Person
	decoder := json.NewDecoder(file2)
	err = decoder.Decode(&people3)
	if err != nil {
		fmt.Println("디코딩 에러:", err)
		return
	}

	fmt.Println("파일에서 읽은 데이터:")
	for _, p := range people3 {
		fmt.Printf("- %s\n", p.Name)
	}

	// === 커스텀 마샬링 ===
	fmt.Println("\n=== 커스텀 마샬링 ===")

	event := Event{
		Name: "컨퍼런스",
		Date: CustomDate{Year: 2024, Month: 12, Day: 25},
	}

	eventJSON, _ := json.MarshalIndent(event, "", "  ")
	fmt.Println(string(eventJSON))

	// 커스텀 언마샬링
	eventStr := `{"name":"워크샵","date":"2024-06-15"}`
	var event2 Event
	json.Unmarshal([]byte(eventStr), &event2)
	fmt.Printf("\n이벤트: %s\n", event2.Name)
	fmt.Printf("날짜: %d년 %d월 %d일\n", event2.Date.Year, event2.Date.Month, event2.Date.Day)

	// === 에러 처리 ===
	fmt.Println("\n=== JSON 에러 처리 ===")

	invalidJSON := `{"name": "테스트", "age": "잘못된값"}`
	var p Person
	err = json.Unmarshal([]byte(invalidJSON), &p)
	if err != nil {
		fmt.Println("파싱 에러:", err)
	}

	// === 정리 ===
	os.Remove("data.json")
	fmt.Println("\n정리 완료")
}

/*
JSON 처리 핵심:

1. 마샬링 (Go -> JSON):
   - json.Marshal(): 압축된 JSON
   - json.MarshalIndent(): 들여쓰기된 JSON
   - json.NewEncoder(): 스트림 인코딩

2. 언마샬링 (JSON -> Go):
   - json.Unmarshal(): 바이트에서 파싱
   - json.NewDecoder(): 스트림 디코딩

3. 구조체 태그:
   - `json:"field_name"`: 필드명 지정
   - `json:"-"`: 필드 제외
   - `json:",omitempty"`: 빈 값 생략
   - `json:",string"`: 문자열로 인코딩

4. 타입:
   - 구조체, 슬라이스, 맵 모두 지원
   - map[string]interface{}: 유연한 JSON 처리
   - 중첩 구조체 지원

5. 커스텀 마샬링:
   - MarshalJSON() 메서드 구현
   - UnmarshalJSON() 메서드 구현

6. 파일 I/O:
   - Encoder/Decoder로 파일 직접 읽기/쓰기
   - 큰 파일은 스트리밍 방식 권장

연습 문제:
1. 설정 파일을 JSON으로 저장하고 읽는 프로그램을 작성하세요
2. API 응답을 JSON으로 파싱하는 함수를 만드세요
3. 구조체를 JSON 파일로 저장하는 Save 메서드를 작성하세요
4. JSON 배열에서 특정 조건의 항목을 필터링하세요
5. 여러 JSON 파일을 하나로 병합하는 프로그램을 작성하세요

실행: go run 08-json.go
*/

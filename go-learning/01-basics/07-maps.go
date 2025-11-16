package main

import (
	"fmt"
	"sort"
)

func main() {
	// === 맵 (Map) ===
	// 맵은 키-값 쌍을 저장하는 자료구조 (해시맵, 딕셔너리)

	// 1. 맵 선언 및 초기화
	var m1 map[string]int // nil 맵 (사용 전에 초기화 필요)
	fmt.Println("nil 맵:", m1, m1 == nil)

	// make로 맵 생성
	m2 := make(map[string]int)
	fmt.Println("빈 맵:", m2)

	// 맵 리터럴로 초기화
	ages := map[string]int{
		"홍길동": 25,
		"김철수": 30,
		"이영희": 28,
	}
	fmt.Println("ages:", ages)

	// 2. 값 할당 및 접근
	ages["박민수"] = 32
	fmt.Println("박민수 추가:", ages)

	fmt.Println("홍길동의 나이:", ages["홍길동"])

	// 3. 값 수정
	ages["홍길동"] = 26
	fmt.Println("홍길동 나이 수정:", ages["홍길동"])

	// 4. 값 존재 확인
	age, exists := ages["홍길동"]
	if exists {
		fmt.Printf("홍길동: %d세\n", age)
	}

	age2, exists2 := ages["없는사람"]
	fmt.Printf("없는사람: %d, 존재: %t\n", age2, exists2)

	// 5. 삭제
	delete(ages, "김철수")
	fmt.Println("김철수 삭제 후:", ages)

	// 존재하지 않는 키 삭제해도 에러 없음
	delete(ages, "없는사람")

	// 6. 맵 길이
	fmt.Println("맵 크기:", len(ages))

	// 7. 맵 순회
	fmt.Println("\n=== 맵 순회 ===")
	scores := map[string]int{
		"수학": 90,
		"영어": 85,
		"과학": 95,
		"국어": 88,
	}

	for subject, score := range scores {
		fmt.Printf("%s: %d점\n", subject, score)
	}

	// 키만 순회
	fmt.Println("\n과목 목록:")
	for subject := range scores {
		fmt.Println("-", subject)
	}

	// 8. 맵은 순서를 보장하지 않음
	// 같은 맵을 여러 번 순회하면 순서가 다를 수 있음
	fmt.Println("\n=== 순서 없음 확인 ===")
	for i := 0; i < 3; i++ {
		fmt.Print("순회 ", i+1, ": ")
		for k := range scores {
			fmt.Print(k, " ")
		}
		fmt.Println()
	}

	// 9. 정렬된 순서로 맵 순회
	fmt.Println("\n=== 키 정렬 후 순회 ===")
	keys := make([]string, 0, len(scores))
	for k := range scores {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	for _, k := range keys {
		fmt.Printf("%s: %d점\n", k, scores[k])
	}

	// 10. 중첩 맵
	fmt.Println("\n=== 중첩 맵 ===")
	students := map[string]map[string]int{
		"홍길동": {
			"수학": 90,
			"영어": 85,
		},
		"김철수": {
			"수학": 95,
			"영어": 80,
		},
	}

	for name, subjects := range students {
		fmt.Printf("%s의 성적:\n", name)
		for subject, score := range subjects {
			fmt.Printf("  %s: %d점\n", subject, score)
		}
	}

	// 중첩 맵에 값 추가
	students["이영희"] = map[string]int{
		"수학": 88,
		"영어": 92,
	}
	fmt.Println("\n이영희 추가 후:", students["이영희"])

	// 11. 맵과 구조체 결합
	fmt.Println("\n=== 맵 + 구조체 ===")
	type Person struct {
		Name string
		Age  int
		City string
	}

	people := map[int]Person{
		1: {Name: "홍길동", Age: 25, City: "서울"},
		2: {Name: "김철수", Age: 30, City: "부산"},
		3: {Name: "이영희", Age: 28, City: "대구"},
	}

	for id, person := range people {
		fmt.Printf("ID %d: %s (%d세, %s)\n", id, person.Name, person.Age, person.City)
	}

	// 12. 맵 복사
	// 맵은 참조 타입이므로 단순 할당은 복사가 아님
	fmt.Println("\n=== 맵 복사 ===")
	original := map[string]int{"a": 1, "b": 2}
	reference := original // 같은 맵을 가리킴
	reference["a"] = 100

	fmt.Println("original:", original)   // {a:100 b:2}
	fmt.Println("reference:", reference) // {a:100 b:2}

	// 실제 복사
	deepCopy := make(map[string]int)
	for k, v := range original {
		deepCopy[k] = v
	}
	deepCopy["a"] = 200

	fmt.Println("original:", original)   // {a:100 b:2}
	fmt.Println("deepCopy:", deepCopy)   // {a:200 b:2}

	// 13. 맵을 집합(Set)처럼 사용
	fmt.Println("\n=== 집합(Set) 구현 ===")
	set := make(map[string]bool)
	set["apple"] = true
	set["banana"] = true
	set["orange"] = true

	// 존재 확인
	if set["apple"] {
		fmt.Println("apple이 집합에 있습니다")
	}

	// 삭제
	delete(set, "banana")

	// 순회
	fmt.Print("집합 요소: ")
	for item := range set {
		fmt.Print(item, " ")
	}
	fmt.Println()

	// 14. 실용 예제: 단어 빈도수 계산
	fmt.Println("\n=== 단어 빈도수 ===")
	text := "go is great go is simple go is fast"
	words := []string{"go", "is", "great", "go", "is", "simple", "go", "is", "fast"}

	wordCount := make(map[string]int)
	for _, word := range words {
		wordCount[word]++
	}

	for word, count := range wordCount {
		fmt.Printf("%s: %d번\n", word, count)
	}

	// 15. 실용 예제: 그룹핑
	fmt.Println("\n=== 나이별 그룹핑 ===")
	allPeople := []Person{
		{Name: "홍길동", Age: 25, City: "서울"},
		{Name: "김철수", Age: 30, City: "부산"},
		{Name: "이영희", Age: 25, City: "대구"},
		{Name: "박민수", Age: 30, City: "인천"},
	}

	groupByAge := make(map[int][]Person)
	for _, person := range allPeople {
		groupByAge[person.Age] = append(groupByAge[person.Age], person)
	}

	for age, group := range groupByAge {
		fmt.Printf("%d세:\n", age)
		for _, person := range group {
			fmt.Printf("  - %s (%s)\n", person.Name, person.City)
		}
	}

	// 16. 실용 예제: 캐시 구현
	fmt.Println("\n=== 간단한 캐시 ===")
	cache := make(map[string]string)

	// 캐시에 데이터 저장
	cache["user:1"] = "홍길동"
	cache["user:2"] = "김철수"

	// 캐시에서 데이터 조회
	if value, found := cache["user:1"]; found {
		fmt.Println("캐시 히트:", value)
	} else {
		fmt.Println("캐시 미스")
	}

	// 17. 빈 구조체를 값으로 사용 (메모리 효율적)
	fmt.Println("\n=== 메모리 효율적인 Set ===")
	efficientSet := make(map[string]struct{})
	efficientSet["item1"] = struct{}{}
	efficientSet["item2"] = struct{}{}

	if _, exists := efficientSet["item1"]; exists {
		fmt.Println("item1이 집합에 있습니다")
	}
}

/*
연습 문제:
1. 맵을 사용해서 전화번호부를 만드세요
2. 문자열에서 각 문자의 빈도수를 계산하세요
3. 두 맵을 병합하는 함수를 작성하세요
4. 맵의 키와 값을 바꾼 새로운 맵을 만드세요
5. 학생 이름을 키로, 과목별 점수를 값으로 하는 중첩 맵을 만들고
   각 학생의 평균 점수를 계산하세요
6. 맵을 사용해서 애너그램(철자 순서만 다른 단어)을 찾으세요

실행: go run 07-maps.go
*/

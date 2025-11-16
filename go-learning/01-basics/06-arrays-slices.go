package main

import "fmt"

func main() {
	// === 배열 (Array) ===
	// 배열은 고정된 크기를 가지며, 크기는 타입의 일부입니다

	// 1. 배열 선언
	var arr1 [5]int // 크기 5인 int 배열, 모든 요소는 0으로 초기화
	fmt.Println("arr1:", arr1)

	// 2. 배열 초기화
	arr2 := [5]int{1, 2, 3, 4, 5}
	fmt.Println("arr2:", arr2)

	// 3. 부분 초기화
	arr3 := [5]int{1, 2, 3} // 나머지는 0
	fmt.Println("arr3:", arr3)

	// 4. 크기 자동 추론
	arr4 := [...]int{1, 2, 3, 4} // 크기 4로 자동 설정
	fmt.Println("arr4:", arr4)

	// 5. 인덱스로 접근
	arr2[0] = 10
	fmt.Println("arr2[0] =", arr2[0])
	fmt.Println("수정된 arr2:", arr2)

	// 6. 배열 길이
	fmt.Println("arr2의 길이:", len(arr2))

	// 7. 배열 순회
	fmt.Print("arr2 순회: ")
	for i := 0; i < len(arr2); i++ {
		fmt.Print(arr2[i], " ")
	}
	fmt.Println()

	// 8. range로 순회
	fmt.Println("range로 순회:")
	for index, value := range arr2 {
		fmt.Printf("  arr2[%d] = %d\n", index, value)
	}

	// 9. 다차원 배열
	matrix := [3][3]int{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}
	fmt.Println("3x3 행렬:")
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			fmt.Printf("%d ", matrix[i][j])
		}
		fmt.Println()
	}

	// === 슬라이스 (Slice) ===
	// 슬라이스는 동적 크기의 배열과 같습니다

	// 1. 슬라이스 선언 및 초기화
	slice1 := []int{1, 2, 3, 4, 5}
	fmt.Println("\nslice1:", slice1)

	// 2. make로 슬라이스 생성
	slice2 := make([]int, 5)    // 길이 5, 용량 5
	slice3 := make([]int, 3, 5) // 길이 3, 용량 5
	fmt.Println("slice2:", slice2)
	fmt.Println("slice3:", slice3)
	fmt.Printf("slice3 길이: %d, 용량: %d\n", len(slice3), cap(slice3))

	// 3. nil 슬라이스
	var slice4 []int
	fmt.Println("nil 슬라이스:", slice4, slice4 == nil)

	// 4. 슬라이스 인덱싱
	slice1[0] = 10
	fmt.Println("수정된 slice1:", slice1)

	// 5. 슬라이싱 (부분 슬라이스 생성)
	numbers := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	fmt.Println("\nnumbers:", numbers)
	fmt.Println("numbers[2:5]:", numbers[2:5])   // 인덱스 2부터 4까지
	fmt.Println("numbers[:4]:", numbers[:4])     // 처음부터 3까지
	fmt.Println("numbers[5:]:", numbers[5:])     // 5부터 끝까지
	fmt.Println("numbers[:]:", numbers[:])       // 전체

	// 6. append - 요소 추가
	fruits := []string{"사과", "바나나"}
	fmt.Println("\n초기 fruits:", fruits)

	fruits = append(fruits, "오렌지")
	fmt.Println("추가 후:", fruits)

	fruits = append(fruits, "포도", "수박")
	fmt.Println("여러 개 추가:", fruits)

	// 슬라이스 합치기
	moreFruits := []string{"딸기", "키위"}
	fruits = append(fruits, moreFruits...)
	fmt.Println("슬라이스 합치기:", fruits)

	// 7. copy - 슬라이스 복사
	original := []int{1, 2, 3}
	copied := make([]int, len(original))
	copy(copied, original)
	fmt.Println("\noriginal:", original)
	fmt.Println("copied:", copied)

	copied[0] = 100
	fmt.Println("copied 수정 후:")
	fmt.Println("  original:", original)
	fmt.Println("  copied:", copied)

	// 8. 슬라이스의 내부 구조
	// 슬라이스는 배열에 대한 참조입니다
	arr := [5]int{1, 2, 3, 4, 5}
	s1 := arr[1:4] // [2, 3, 4]
	s2 := arr[2:5] // [3, 4, 5]

	fmt.Println("\narr:", arr)
	fmt.Println("s1:", s1)
	fmt.Println("s2:", s2)

	s1[1] = 100 // s1의 두 번째 요소(arr[2])를 수정
	fmt.Println("s1[1] = 100 후:")
	fmt.Println("  arr:", arr)  // arr도 변경됨!
	fmt.Println("  s1:", s1)
	fmt.Println("  s2:", s2)    // s2도 영향받음!

	// 9. 슬라이스 확장
	fmt.Println("\n=== 슬라이스 확장 ===")
	s := make([]int, 0, 3)
	fmt.Printf("초기: len=%d cap=%d %v\n", len(s), cap(s), s)

	for i := 0; i < 5; i++ {
		s = append(s, i)
		fmt.Printf("append %d: len=%d cap=%d %v\n", i, len(s), cap(s), s)
	}

	// 10. 슬라이스에서 요소 제거
	fmt.Println("\n=== 요소 제거 ===")
	nums := []int{1, 2, 3, 4, 5}
	fmt.Println("원본:", nums)

	// 인덱스 2 제거 (3을 제거)
	index := 2
	nums = append(nums[:index], nums[index+1:]...)
	fmt.Println("인덱스 2 제거:", nums)

	// 11. 슬라이스 역순 정렬
	fmt.Println("\n=== 역순 정렬 ===")
	values := []int{1, 2, 3, 4, 5}
	fmt.Println("원본:", values)

	// 역순으로 만들기
	for i, j := 0, len(values)-1; i < j; i, j = i+1, j-1 {
		values[i], values[j] = values[j], values[i]
	}
	fmt.Println("역순:", values)

	// 12. 2차원 슬라이스
	fmt.Println("\n=== 2차원 슬라이스 ===")
	board := [][]int{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
	}
	fmt.Println("2차원 슬라이스:")
	for i, row := range board {
		fmt.Printf("행 %d: %v\n", i, row)
	}

	// 가변 길이 2차원 슬라이스
	triangle := make([][]int, 4)
	for i := range triangle {
		triangle[i] = make([]int, i+1)
		for j := range triangle[i] {
			triangle[i][j] = i + j
		}
	}
	fmt.Println("\n삼각형 슬라이스:")
	for i, row := range triangle {
		fmt.Printf("행 %d: %v\n", i, row)
	}

	// 13. 실용 예제: 필터링
	fmt.Println("\n=== 필터링 ===")
	allNumbers := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	var evenNumbers []int
	for _, num := range allNumbers {
		if num%2 == 0 {
			evenNumbers = append(evenNumbers, num)
		}
	}
	fmt.Println("짝수만:", evenNumbers)

	// 14. 실용 예제: 맵핑
	fmt.Println("\n=== 맵핑 (제곱) ===")
	original2 := []int{1, 2, 3, 4, 5}
	squared := make([]int, len(original2))
	for i, num := range original2 {
		squared[i] = num * num
	}
	fmt.Println("원본:", original2)
	fmt.Println("제곱:", squared)
}

/*
연습 문제:
1. 배열의 모든 요소의 합과 평균을 계산하세요
2. 슬라이스를 역순으로 출력하는 함수를 작성하세요
3. 두 슬라이스를 병합하고 중복을 제거하세요
4. 슬라이스에서 최대값과 최소값의 인덱스를 찾으세요
5. 2차원 슬라이스로 구구단 표를 만드세요
6. 슬라이스에서 특정 값을 모두 제거하는 함수를 작성하세요

실행: go run 06-arrays-slices.go
*/

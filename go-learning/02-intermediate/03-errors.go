package main

import (
	"errors"
	"fmt"
	"os"
)

// === 기본 에러 처리 ===

func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("0으로 나눌 수 없습니다")
	}
	return a / b, nil
}

// === fmt.Errorf로 에러 생성 ===

func findUser(id int) (string, error) {
	users := map[int]string{
		1: "홍길동",
		2: "김철수",
		3: "이영희",
	}

	if name, exists := users[id]; exists {
		return name, nil
	}

	return "", fmt.Errorf("사용자를 찾을 수 없습니다: ID=%d", id)
}

// === 커스텀 에러 타입 ===

type ValidationError struct {
	Field   string
	Message string
}

func (e ValidationError) Error() string {
	return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

func validateAge(age int) error {
	if age < 0 {
		return ValidationError{
			Field:   "age",
			Message: "나이는 0보다 커야 합니다",
		}
	}
	if age > 150 {
		return ValidationError{
			Field:   "age",
			Message: "나이가 너무 큽니다",
		}
	}
	return nil
}

// === 에러 래핑 (Go 1.13+) ===

func readConfig(filename string) error {
	_, err := os.ReadFile(filename)
	if err != nil {
		return fmt.Errorf("설정 파일 읽기 실패 %s: %w", filename, err)
	}
	return nil
}

// === 여러 에러 타입 ===

type NotFoundError struct {
	Resource string
}

func (e NotFoundError) Error() string {
	return fmt.Sprintf("%s를 찾을 수 없습니다", e.Resource)
}

type PermissionError struct {
	User   string
	Action string
}

func (e PermissionError) Error() string {
	return fmt.Sprintf("%s는 %s 권한이 없습니다", e.User, e.Action)
}

func accessResource(user string, resourceID int) error {
	if user == "" {
		return errors.New("사용자 이름이 필요합니다")
	}

	if resourceID < 0 {
		return NotFoundError{Resource: fmt.Sprintf("리소스 #%d", resourceID)}
	}

	if user != "admin" {
		return PermissionError{User: user, Action: "접근"}
	}

	return nil
}

// === 에러 체크 패턴 ===

func processData(data string) error {
	// 1단계
	if len(data) == 0 {
		return errors.New("데이터가 비어있습니다")
	}

	// 2단계
	if len(data) > 100 {
		return errors.New("데이터가 너무 깁니다")
	}

	// 3단계
	fmt.Println("데이터 처리:", data)
	return nil
}

// === defer로 에러 처리 ===

func writeFile(filename, content string) (err error) {
	f, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("파일 생성 실패: %w", err)
	}
	defer func() {
		if closeErr := f.Close(); closeErr != nil && err == nil {
			err = fmt.Errorf("파일 닫기 실패: %w", closeErr)
		}
	}()

	_, err = f.WriteString(content)
	if err != nil {
		return fmt.Errorf("쓰기 실패: %w", err)
	}

	return nil
}

// === 에러 무시하기 (권장하지 않음) ===

func ignoreError() {
	// 에러를 무시 (좋지 않은 방법)
	// _ = someFunction()

	// 대신 최소한 로그라도 남기기
	// if err := someFunction(); err != nil {
	//     log.Println("에러 발생:", err)
	// }
}

// === panic과 recover ===

func riskyOperation() {
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("패닉 복구:", r)
		}
	}()

	fmt.Println("위험한 작업 시작")
	panic("치명적인 에러!")
	fmt.Println("이 줄은 실행되지 않음")
}

func causesPanic() {
	panic("의도적인 패닉")
}

// === 실용 예제: 체인 에러 처리 ===

type DataProcessor struct {
	data []int
}

func (dp *DataProcessor) Load(filename string) error {
	// 파일 로드 시뮬레이션
	if filename == "" {
		return errors.New("파일명이 비어있습니다")
	}
	dp.data = []int{1, 2, 3, 4, 5}
	return nil
}

func (dp *DataProcessor) Validate() error {
	if len(dp.data) == 0 {
		return errors.New("데이터가 비어있습니다")
	}
	return nil
}

func (dp *DataProcessor) Process() error {
	if err := dp.Validate(); err != nil {
		return fmt.Errorf("검증 실패: %w", err)
	}

	sum := 0
	for _, v := range dp.data {
		sum += v
	}
	fmt.Println("합계:", sum)
	return nil
}

func main() {
	// === 기본 에러 처리 ===
	fmt.Println("=== 기본 에러 처리 ===")
	result, err := divide(10, 2)
	if err != nil {
		fmt.Println("에러:", err)
	} else {
		fmt.Println("10 / 2 =", result)
	}

	_, err = divide(10, 0)
	if err != nil {
		fmt.Println("에러:", err)
	}

	// === 에러 반환 패턴 ===
	fmt.Println("\n=== 에러 반환 ===")
	name, err := findUser(1)
	if err != nil {
		fmt.Println("에러:", err)
	} else {
		fmt.Println("사용자:", name)
	}

	_, err = findUser(999)
	if err != nil {
		fmt.Println("에러:", err)
	}

	// === 커스텀 에러 ===
	fmt.Println("\n=== 커스텀 에러 ===")
	if err := validateAge(25); err != nil {
		fmt.Println("검증 실패:", err)
	} else {
		fmt.Println("나이 검증 통과")
	}

	if err := validateAge(-5); err != nil {
		fmt.Println("검증 실패:", err)

		// 타입 단언으로 에러 상세 정보 확인
		if ve, ok := err.(ValidationError); ok {
			fmt.Printf("  필드: %s\n", ve.Field)
			fmt.Printf("  메시지: %s\n", ve.Message)
		}
	}

	// === 에러 래핑 ===
	fmt.Println("\n=== 에러 래핑 ===")
	err = readConfig("nonexistent.conf")
	if err != nil {
		fmt.Println("에러:", err)

		// errors.Unwrap으로 원본 에러 확인
		if unwrapped := errors.Unwrap(err); unwrapped != nil {
			fmt.Println("원본 에러:", unwrapped)
		}

		// errors.Is로 특정 에러인지 확인
		if errors.Is(err, os.ErrNotExist) {
			fmt.Println("파일이 존재하지 않습니다")
		}
	}

	// === 여러 에러 타입 처리 ===
	fmt.Println("\n=== 다양한 에러 ===")
	testCases := []struct {
		user string
		id   int
	}{
		{"admin", 100},
		{"user", 100},
		{"", 100},
		{"admin", -1},
	}

	for _, tc := range testCases {
		err := accessResource(tc.user, tc.id)
		if err != nil {
			fmt.Printf("user=%s, id=%d: %v\n", tc.user, tc.id, err)

			// 타입 스위치로 에러 처리
			switch e := err.(type) {
			case NotFoundError:
				fmt.Println("  -> 리소스를 찾을 수 없음:", e.Resource)
			case PermissionError:
				fmt.Printf("  -> 권한 없음: %s가 %s 시도\n", e.User, e.Action)
			default:
				fmt.Println("  -> 일반 에러")
			}
		} else {
			fmt.Printf("user=%s, id=%d: 성공\n", tc.user, tc.id)
		}
	}

	// === 에러 체크 패턴 ===
	fmt.Println("\n=== 에러 체크 ===")
	if err := processData(""); err != nil {
		fmt.Println("에러:", err)
		return // early return
	}

	if err := processData("유효한 데이터"); err != nil {
		fmt.Println("에러:", err)
	}

	// === panic과 recover ===
	fmt.Println("\n=== panic과 recover ===")
	riskyOperation()
	fmt.Println("프로그램 계속 실행")

	// recover 없이 panic (프로그램 종료)
	// causesPanic() // 주석 해제하면 프로그램 종료

	// === DataProcessor 예제 ===
	fmt.Println("\n=== DataProcessor ===")
	processor := &DataProcessor{}

	if err := processor.Load("data.txt"); err != nil {
		fmt.Println("로드 실패:", err)
		return
	}

	if err := processor.Process(); err != nil {
		fmt.Println("처리 실패:", err)
		return
	}

	// === 모범 사례 ===
	fmt.Println("\n=== 에러 처리 모범 사례 ===")
	fmt.Println("1. 에러를 무시하지 마세요")
	fmt.Println("2. 에러 메시지는 명확하게")
	fmt.Println("3. 필요한 경우에만 panic 사용")
	fmt.Println("4. 에러를 래핑하여 컨텍스트 추가")
	fmt.Println("5. 커스텀 에러 타입으로 상세 정보 제공")
}

/*
에러 처리 가이드라인:

1. 에러 반환:
   - 마지막 반환값으로 error 반환
   - 에러가 없으면 nil 반환
   - errors.New() 또는 fmt.Errorf() 사용

2. 에러 체크:
   - 항상 에러를 체크
   - if err != nil 패턴 사용
   - early return으로 에러 처리

3. 커스텀 에러:
   - Error() 메서드 구현
   - 타입 단언으로 상세 정보 접근

4. 에러 래핑 (Go 1.13+):
   - fmt.Errorf("%w", err)로 래핑
   - errors.Is()로 에러 타입 확인
   - errors.As()로 타입 단언
   - errors.Unwrap()로 원본 에러 확인

5. panic vs error:
   - 일반적인 경우: error 사용
   - 복구 불가능한 경우만 panic
   - 라이브러리는 panic 대신 error 반환

6. defer와 에러:
   - defer로 리소스 정리
   - named return으로 defer에서 에러 수정 가능

연습 문제:
1. 파일을 읽고 에러를 처리하는 함수를 작성하세요
2. 여러 검증 규칙을 적용하는 Validator를 만드세요
3. 에러를 로깅하는 래퍼 함수를 만드세요
4. 재시도 로직을 포함한 에러 처리를 구현하세요
5. 에러를 수집하고 한 번에 반환하는 함수를 만드세요

실행: go run 03-errors.go
*/

package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func main() {
	// === 파일 쓰기 ===
	fmt.Println("=== 파일 쓰기 ===")

	// 1. os.WriteFile (간단한 방법)
	content := []byte("Hello, Go!\n안녕하세요, Go 언어!")
	err := os.WriteFile("test.txt", content, 0644)
	if err != nil {
		fmt.Println("쓰기 에러:", err)
		return
	}
	fmt.Println("test.txt 생성 완료")

	// === 파일 읽기 ===
	fmt.Println("\n=== 파일 읽기 ===")

	// 1. os.ReadFile (전체 읽기)
	data, err := os.ReadFile("test.txt")
	if err != nil {
		fmt.Println("읽기 에러:", err)
		return
	}
	fmt.Println("파일 내용:")
	fmt.Println(string(data))

	// === 파일 열기 및 닫기 ===
	fmt.Println("\n=== 파일 열기/닫기 ===")

	file, err := os.Open("test.txt")
	if err != nil {
		fmt.Println("열기 에러:", err)
		return
	}
	defer file.Close() // 중요: 파일 닫기

	// 파일 정보
	fileInfo, err := file.Stat()
	if err != nil {
		fmt.Println("정보 에러:", err)
		return
	}
	fmt.Printf("파일명: %s\n", fileInfo.Name())
	fmt.Printf("크기: %d bytes\n", fileInfo.Size())
	fmt.Printf("권한: %v\n", fileInfo.Mode())
	fmt.Printf("수정 시간: %v\n", fileInfo.ModTime())

	// === 버퍼 읽기 ===
	fmt.Println("\n=== 버퍼 읽기 ===")

	file2, err := os.Open("test.txt")
	if err != nil {
		fmt.Println("에러:", err)
		return
	}
	defer file2.Close()

	scanner := bufio.NewScanner(file2)
	lineNum := 1
	for scanner.Scan() {
		fmt.Printf("%d: %s\n", lineNum, scanner.Text())
		lineNum++
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("스캔 에러:", err)
	}

	// === 파일 생성 및 쓰기 ===
	fmt.Println("\n=== 파일 생성 및 쓰기 ===")

	outFile, err := os.Create("output.txt")
	if err != nil {
		fmt.Println("생성 에러:", err)
		return
	}
	defer outFile.Close()

	// 문자열 쓰기
	outFile.WriteString("첫 번째 줄\n")
	outFile.WriteString("두 번째 줄\n")

	// fmt.Fprintf 사용
	fmt.Fprintf(outFile, "숫자: %d\n", 42)
	fmt.Fprintf(outFile, "이름: %s\n", "Go")

	fmt.Println("output.txt 생성 완료")

	// === 버퍼 쓰기 ===
	fmt.Println("\n=== 버퍼 쓰기 ===")

	bufFile, err := os.Create("buffered.txt")
	if err != nil {
		fmt.Println("에러:", err)
		return
	}
	defer bufFile.Close()

	writer := bufio.NewWriter(bufFile)
	for i := 1; i <= 10; i++ {
		writer.WriteString(fmt.Sprintf("줄 %d\n", i))
	}
	writer.Flush() // 버퍼 비우기 (중요!)

	fmt.Println("buffered.txt 생성 완료")

	// === 파일 추가 (Append) ===
	fmt.Println("\n=== 파일 추가 ===")

	appendFile, err := os.OpenFile("test.txt", os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("에러:", err)
		return
	}
	defer appendFile.Close()

	appendFile.WriteString("\n추가된 내용")
	fmt.Println("test.txt에 내용 추가 완료")

	// === 바이트 단위 읽기 ===
	fmt.Println("\n=== 바이트 단위 읽기 ===")

	byteFile, err := os.Open("test.txt")
	if err != nil {
		fmt.Println("에러:", err)
		return
	}
	defer byteFile.Close()

	buffer := make([]byte, 10)
	n, err := byteFile.Read(buffer)
	if err != nil && err != io.EOF {
		fmt.Println("읽기 에러:", err)
		return
	}
	fmt.Printf("읽은 바이트 수: %d\n", n)
	fmt.Printf("내용: %s\n", string(buffer[:n]))

	// === 파일 복사 ===
	fmt.Println("\n=== 파일 복사 ===")

	sourceFile, err := os.Open("test.txt")
	if err != nil {
		fmt.Println("에러:", err)
		return
	}
	defer sourceFile.Close()

	destFile, err := os.Create("copy.txt")
	if err != nil {
		fmt.Println("에러:", err)
		return
	}
	defer destFile.Close()

	bytesWritten, err := io.Copy(destFile, sourceFile)
	if err != nil {
		fmt.Println("복사 에러:", err)
		return
	}
	fmt.Printf("%d bytes 복사 완료\n", bytesWritten)

	// === 파일 존재 확인 ===
	fmt.Println("\n=== 파일 존재 확인 ===")

	if _, err := os.Stat("test.txt"); err == nil {
		fmt.Println("test.txt 존재함")
	} else if os.IsNotExist(err) {
		fmt.Println("test.txt 존재하지 않음")
	}

	// === 디렉토리 생성 ===
	fmt.Println("\n=== 디렉토리 생성 ===")

	err = os.Mkdir("testdir", 0755)
	if err != nil && !os.IsExist(err) {
		fmt.Println("디렉토리 생성 에러:", err)
	} else {
		fmt.Println("testdir 생성 완료")
	}

	// 중첩 디렉토리 생성
	err = os.MkdirAll("path/to/nested", 0755)
	if err != nil {
		fmt.Println("에러:", err)
	} else {
		fmt.Println("중첩 디렉토리 생성 완료")
	}

	// === 디렉토리 읽기 ===
	fmt.Println("\n=== 디렉토리 읽기 ===")

	entries, err := os.ReadDir(".")
	if err != nil {
		fmt.Println("에러:", err)
		return
	}

	fmt.Println("현재 디렉토리 내용:")
	for _, entry := range entries {
		if entry.IsDir() {
			fmt.Printf("[DIR]  %s\n", entry.Name())
		} else {
			fmt.Printf("[FILE] %s\n", entry.Name())
		}
	}

	// === filepath 패키지 ===
	fmt.Println("\n=== filepath 패키지 ===")

	path := filepath.Join("path", "to", "file.txt")
	fmt.Println("결합된 경로:", path)

	fmt.Println("디렉토리:", filepath.Dir(path))
	fmt.Println("파일명:", filepath.Base(path))
	fmt.Println("확장자:", filepath.Ext(path))

	// 절대 경로
	absPath, err := filepath.Abs("test.txt")
	if err != nil {
		fmt.Println("에러:", err)
	} else {
		fmt.Println("절대 경로:", absPath)
	}

	// === 파일 삭제 ===
	fmt.Println("\n=== 파일 삭제 ===")

	// 테스트 파일 삭제
	filesToDelete := []string{"test.txt", "output.txt", "buffered.txt", "copy.txt"}
	for _, f := range filesToDelete {
		err := os.Remove(f)
		if err != nil {
			fmt.Printf("%s 삭제 실패: %v\n", f, err)
		} else {
			fmt.Printf("%s 삭제 완료\n", f)
		}
	}

	// 디렉토리 삭제
	err = os.RemoveAll("path")
	if err != nil {
		fmt.Println("디렉토리 삭제 에러:", err)
	} else {
		fmt.Println("path 디렉토리 삭제 완료")
	}

	err = os.Remove("testdir")
	if err != nil {
		fmt.Println("에러:", err)
	} else {
		fmt.Println("testdir 삭제 완료")
	}
}

/*
파일 입출력 핵심:

1. 간단한 방법:
   - os.ReadFile(): 전체 파일 읽기
   - os.WriteFile(): 전체 파일 쓰기

2. 세밀한 제어:
   - os.Open(): 읽기 전용
   - os.Create(): 쓰기 (덮어쓰기)
   - os.OpenFile(): 플래그로 세밀한 제어
   - defer file.Close(): 항상 파일 닫기

3. 버퍼 I/O:
   - bufio.Scanner: 줄 단위 읽기
   - bufio.Reader: 버퍼 읽기
   - bufio.Writer: 버퍼 쓰기

4. 유틸리티:
   - io.Copy(): 파일 복사
   - filepath.Join(): 경로 결합
   - os.Stat(): 파일 정보

5. 디렉토리:
   - os.Mkdir(): 디렉토리 생성
   - os.MkdirAll(): 중첩 디렉토리 생성
   - os.ReadDir(): 디렉토리 읽기
   - os.Remove()/RemoveAll(): 삭제

6. 에러 처리:
   - 항상 에러 체크
   - defer로 리소스 정리
   - os.IsNotExist() 등으로 에러 타입 확인

연습 문제:
1. 텍스트 파일의 줄 수를 세는 프로그램을 작성하세요
2. 여러 파일을 하나로 합치는 함수를 만드세요
3. 디렉토리의 모든 파일 크기 합계를 계산하세요
4. CSV 파일을 읽고 쓰는 함수를 작성하세요
5. 로그 파일에 타임스탬프와 함께 메시지를 추가하세요

실행: go run 07-file-io.go
*/

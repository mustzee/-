package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Todo struct {
	ID        int    `json:"id"`
	Task      string `json:"task"`
	Completed bool   `json:"completed"`
}

type TodoList struct {
	Todos    []Todo `json:"todos"`
	NextID   int    `json:"next_id"`
	filename string
}

func NewTodoList(filename string) *TodoList {
	tl := &TodoList{
		Todos:    []Todo{},
		NextID:   1,
		filename: filename,
	}
	tl.Load()
	return tl
}

func (tl *TodoList) Load() error {
	data, err := os.ReadFile(tl.filename)
	if err != nil {
		if os.IsNotExist(err) {
			return nil // 파일이 없으면 새로 시작
		}
		return err
	}

	return json.Unmarshal(data, tl)
}

func (tl *TodoList) Save() error {
	data, err := json.MarshalIndent(tl, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile(tl.filename, data, 0644)
}

func (tl *TodoList) Add(task string) {
	todo := Todo{
		ID:        tl.NextID,
		Task:      task,
		Completed: false,
	}
	tl.Todos = append(tl.Todos, todo)
	tl.NextID++
	tl.Save()
	fmt.Printf("할 일 추가됨: #%d %s\n", todo.ID, todo.Task)
}

func (tl *TodoList) List() {
	if len(tl.Todos) == 0 {
		fmt.Println("할 일이 없습니다.")
		return
	}

	fmt.Println("\n=== 할 일 목록 ===")
	for _, todo := range tl.Todos {
		status := " "
		if todo.Completed {
			status = "✓"
		}
		fmt.Printf("[%s] %d. %s\n", status, todo.ID, todo.Task)
	}
	fmt.Println()
}

func (tl *TodoList) Complete(id int) {
	for i, todo := range tl.Todos {
		if todo.ID == id {
			tl.Todos[i].Completed = true
			tl.Save()
			fmt.Printf("완료됨: #%d %s\n", id, todo.Task)
			return
		}
	}
	fmt.Printf("할 일을 찾을 수 없습니다: #%d\n", id)
}

func (tl *TodoList) Delete(id int) {
	for i, todo := range tl.Todos {
		if todo.ID == id {
			tl.Todos = append(tl.Todos[:i], tl.Todos[i+1:]...)
			tl.Save()
			fmt.Printf("삭제됨: #%d %s\n", id, todo.Task)
			return
		}
	}
	fmt.Printf("할 일을 찾을 수 없습니다: #%d\n", id)
}

func printHelp() {
	fmt.Println("\n=== TODO CLI ===")
	fmt.Println("명령어:")
	fmt.Println("  add <task>    - 할 일 추가")
	fmt.Println("  list          - 목록 보기")
	fmt.Println("  done <id>     - 완료 표시")
	fmt.Println("  delete <id>   - 삭제")
	fmt.Println("  help          - 도움말")
	fmt.Println("  quit          - 종료")
	fmt.Println()
}

func main() {
	todoList := NewTodoList("todos.json")
	scanner := bufio.NewScanner(os.Stdin)

	fmt.Println("TODO 앱에 오신 것을 환영합니다!")
	printHelp()

	for {
		fmt.Print("> ")
		if !scanner.Scan() {
			break
		}

		input := strings.TrimSpace(scanner.Text())
		if input == "" {
			continue
		}

		parts := strings.SplitN(input, " ", 2)
		command := parts[0]

		switch command {
		case "add":
			if len(parts) < 2 {
				fmt.Println("사용법: add <task>")
				continue
			}
			todoList.Add(parts[1])

		case "list":
			todoList.List()

		case "done":
			if len(parts) < 2 {
				fmt.Println("사용법: done <id>")
				continue
			}
			id, err := strconv.Atoi(parts[1])
			if err != nil {
				fmt.Println("유효한 ID를 입력하세요")
				continue
			}
			todoList.Complete(id)

		case "delete":
			if len(parts) < 2 {
				fmt.Println("사용법: delete <id>")
				continue
			}
			id, err := strconv.Atoi(parts[1])
			if err != nil {
				fmt.Println("유효한 ID를 입력하세요")
				continue
			}
			todoList.Delete(id)

		case "help":
			printHelp()

		case "quit", "exit":
			fmt.Println("안녕히 가세요!")
			return

		default:
			fmt.Printf("알 수 없는 명령어: %s\n", command)
			fmt.Println("'help'를 입력하여 사용 가능한 명령어를 확인하세요")
		}
	}
}

/*
TODO CLI 앱

기능:
- 할 일 추가
- 목록 보기
- 완료 표시
- 삭제
- JSON 파일로 저장

실행:
  go run main.go

예제 사용:
  > add Go 공부하기
  > add 프로젝트 만들기
  > list
  > done 1
  > delete 2
  > quit
*/

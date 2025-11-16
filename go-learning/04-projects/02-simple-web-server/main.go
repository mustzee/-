package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
)

type User struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
	Email string `json:"email"`
}

type Server struct {
	users  map[int]User
	nextID int
	mu     sync.RWMutex
}

func NewServer() *Server {
	return &Server{
		users:  make(map[int]User),
		nextID: 1,
	}
}

// GET /
func (s *Server) handleHome(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<h1>Go 웹 서버</h1>")
	fmt.Fprintf(w, "<p>API 엔드포인트:</p>")
	fmt.Fprintf(w, "<ul>")
	fmt.Fprintf(w, "<li>GET /api/users - 모든 사용자</li>")
	fmt.Fprintf(w, "<li>POST /api/users - 사용자 생성</li>")
	fmt.Fprintf(w, "<li>GET /api/users/{id} - 사용자 조회</li>")
	fmt.Fprintf(w, "</ul>")
}

// GET /api/users
func (s *Server) handleGetUsers(w http.ResponseWriter, r *http.Request) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	users := make([]User, 0, len(s.users))
	for _, user := range s.users {
		users = append(users, user)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(users)
}

// POST /api/users
func (s *Server) handleCreateUser(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	s.mu.Lock()
	user.ID = s.nextID
	s.nextID++
	s.users[user.ID] = user
	s.mu.Unlock()

	w.Header().Set("Content-Type", "application/json")
	w.WriteStatus(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}

// 라우터
func (s *Server) routes() {
	http.HandleFunc("/", s.handleHome)
	http.HandleFunc("/api/users", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			s.handleGetUsers(w, r)
		case http.MethodPost:
			s.handleCreateUser(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})
}

func main() {
	server := NewServer()
	server.routes()

	// 샘플 데이터
	server.users[1] = User{ID: 1, Name: "홍길동", Email: "hong@example.com"}
	server.users[2] = User{ID: 2, Name: "김철수", Email: "kim@example.com"}
	server.nextID = 3

	port := ":8080"
	fmt.Printf("서버 시작: http://localhost%s\n", port)
	log.Fatal(http.ListenAndServe(port, nil))
}

/*
간단한 웹 서버

기능:
- RESTful API
- JSON 응답
- 동시성 안전 (Mutex)

실행:
  go run main.go

테스트:
  # 홈페이지
  curl http://localhost:8080

  # 모든 사용자 조회
  curl http://localhost:8080/api/users

  # 사용자 생성
  curl -X POST http://localhost:8080/api/users \
    -H "Content-Type: application/json" \
    -d '{"name":"이영희","email":"lee@example.com"}'
*/

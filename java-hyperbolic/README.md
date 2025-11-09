# Order-3 Heptagonal Tiling - Java Swing

Java Swing으로 구현한 데스크톱 쌍곡 기하학 시각화!

## 🚀 실행 방법

### 방법 1: Maven 사용 (권장)

```bash
cd java-hyperbolic

# 컴파일 및 실행
mvn compile exec:java -Dexec.mainClass="hyperbolic.HyperbolicViewer"

# 또는 실행 가능한 JAR 빌드
mvn clean package
java -jar target/hyperbolic-tiling.jar
```

### 방법 2: javac 직접 사용

```bash
cd java-hyperbolic/src/main/java

# 컴파일
javac hyperbolic/*.java

# 실행
java hyperbolic.HyperbolicViewer
```

## ✨ 특징

### 🎬 애니메이션
- **Animate Generation**: 타일이 단계별로 생성되는 과정 시각화
- **Play/Pause**: 애니메이션 제어
- **Progress 표시**: 실시간 진행률

### 🎮 컨트롤
- **Depth 슬라이더** (1-6): 타일링 깊이 조절
- **Show Edges**: 경계선 표시/숨김
- **Color Tiles**: 색상 모드
- **Reset View**: 초기화

### 🖥️ Java Swing UI
- 네이티브 데스크톱 애플리케이션
- 안티앨리어싱 고품질 렌더링
- 다크 테마 디자인

## 📁 프로젝트 구조

```
java-hyperbolic/
├── src/main/java/hyperbolic/
│   ├── Complex.java              # 복소수 클래스
│   ├── MobiusTransform.java      # Möbius 변환
│   ├── HeptagonalTiling.java     # 타일링 생성기
│   ├── PoincarePanel.java        # 렌더링 패널
│   └── HyperbolicViewer.java     # 메인 애플리케이션
├── pom.xml                        # Maven 빌드 설정
└── README.md
```

## 🏗️ 주요 클래스

### `Complex.java`
복소수 연산 (덧셈, 뺄셈, 곱셈, 나눗셈, 절댓값 등)

### `MobiusTransform.java`
Möbius 변환으로 쌍곡 등거리 변환 구현

### `HeptagonalTiling.java`
- BFS 알고리즘으로 타일 생성
- {7,3} 타일링의 기하학적 매개변수 계산

### `PoincarePanel.java`
- `JPanel`을 상속한 커스텀 렌더링 패널
- `Graphics2D`로 측지선(곡선) 그리기
- 안티앨리어싱 적용

### `HyperbolicViewer.java`
- 메인 애플리케이션 프레임
- UI 컨트롤 구성
- 이벤트 핸들링

## 🎯 사용 예시

### 애니메이션 실행
1. **Animate Generation** 체크
2. Depth를 5로 설정
3. **Play** 버튼 클릭
4. 타일이 하나씩 생성되는 모습 관찰!

### 고해상도 렌더링
1. **Animate Generation** 체크 해제
2. Depth 6으로 설정
3. **Color Tiles** 활성화
4. 약 800개의 칠각형 타일 생성

## 📦 요구사항

- **Java**: JDK 11 이상
- **Maven**: 3.6+ (선택사항, 빌드용)
- **OS**: Windows, macOS, Linux 모두 지원

## 🎨 렌더링 기술

### Graphics2D API
- `Arc2D`: 측지선(원호) 렌더링
- `Path2D`: 곡선 다각형 채우기
- `RenderingHints`: 안티앨리어싱 및 고품질 렌더링

### 색상 테마
```java
- Background: #0f0f1e (어두운 파랑)
- Panel: #16213e (진한 파랑)
- Accent: #00ff88 (네온 그린)
- Tiles: 7가지 파스텔 색상 (150 alpha)
```

## 🆚 구현 비교

| 특징 | Java Swing | React | Python |
|------|-----------|-------|--------|
| 플랫폼 | 데스크톱 | 웹 | 데스크톱 |
| 설치 | JDK 필요 | npm 필요 | pip 필요 |
| 성능 | 매우 우수 | 우수 | 우수 |
| UI | Swing | HTML/CSS | matplotlib |
| 애니메이션 | Timer | setTimeout | Timer |
| 배포 | JAR | 웹 호스팅 | exe/app |
| 크로스플랫폼 | ✅ | ✅ | ✅ |

## 🚀 배포

### 실행 가능한 JAR 생성
```bash
mvn clean package
# target/hyperbolic-tiling.jar 생성됨
```

### 실행
```bash
java -jar target/hyperbolic-tiling.jar
```

JAR 파일을 다른 컴퓨터에 복사해도 Java만 설치되어 있으면 실행 가능!

## 📝 라이선스

MIT License

## 🎓 교육적 가치

이 프로젝트는 다음을 배우는 데 유용합니다:
- **쌍곡 기하학**: Poincaré disk 모델
- **복소수 연산**: 기하학적 변환
- **Java Swing**: 커스텀 UI 컴포넌트
- **Graphics2D**: 고급 2D 렌더링
- **BFS 알고리즘**: 타일 생성
- **객체지향 설계**: 클래스 분리 및 캡슐화

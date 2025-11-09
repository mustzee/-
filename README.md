# Order-3 Heptagonal Tiling - Poincaré Disk Visualization

수학적으로 정확한 쌍곡 기하학 시각화: **{7,3} 타일링**

## 개요

이 프로젝트는 Poincaré disk 모델을 사용하여 Order-3 heptagonal tiling을 시각화합니다. 이는 각 꼭짓점에 3개의 정칠각형이 만나는 쌍곡 평면의 정규 타일링입니다.

## 수학적 배경

- **Schläfli 기호**: {7,3}
- **기하학**: 쌍곡 기하학 (H²)
- **구조**: 각 꼭짓점에 정확히 3개의 정칠각형이 만남
- **모델**: Poincaré disk - 쌍곡 평면을 단위 원판에 투영

### 왜 쌍곡 기하학인가?

정칠각형의 내각은 약 128.57°입니다. 유클리드 평면에서 3개의 정칠각형을 한 점에 모으면 385.71°가 되어 평면에 맞지 않습니다. 쌍곡 공간의 음의 곡률이 이를 가능하게 합니다.

## 주요 기능

### 수학적 정확성
- **복소수 기반 계산**: 복소 평면에서의 Möbius 변환
- **측지선 렌더링**: 쌍곡 기하학에서의 "직선" (Poincaré disk에서는 원호)
- **정확한 타일 배치**: 쌍곡 등거리 변환을 통한 타일 생성

### 시각화 특징
- 정교한 타일 경계 표현
- 각 타일의 색상 구분
- 인터랙티브 탐색 (팬, 줌)
- 타일 깊이 조절 가능

## 사용 방법

### 로컬에서 실행

```bash
# Python 3으로 간단한 서버 실행
python3 -m http.server 8000

# 또는 Python 2
python -m SimpleHTTPServer 8000

# 브라우저에서 열기
open http://localhost:8000
```

### 컨트롤

- **Depth 슬라이더**: 타일링의 재귀 깊이 조절 (1-6)
- **Show Edges**: 타일 경계선 표시/숨김
- **Color Tiles**: 타일 색상 모드 전환
- **마우스 드래그**: 뷰 이동 (팬)
- **마우스 휠**: 줌 인/아웃
- **Reset View**: 초기 뷰로 복귀

## 구현 세부사항

### 핵심 알고리즘

1. **Complex 클래스**: 복소수 연산 (덧셈, 곱셈, 나눗셈, 켤레)
2. **MobiusTransform**: Möbius 변환으로 쌍곡 등거리 변환 구현
3. **측지선 계산**: 두 점을 잇는 쌍곡 "직선" (단위원과 직교하는 원호)
4. **타일 생성**: BFS 알고리즘으로 중앙에서 확장

### 수학 공식

**쌍곡 거리**:
```
d(z₁, z₂) = acosh(1 + 2|z₁ - z₂|² / ((1 - |z₁|²)(1 - |z₂|²)))
```

**Möbius 변환**:
```
f(z) = (az + b) / (cz + d)
```

**측지선**: Poincaré disk에서 측지선은 단위원과 직교하는 원의 호

## 파일 구조

```
.
├── index.html          # HTML 구조 및 UI
├── hyperbolic.js       # 쌍곡 기하학 구현
└── README.md          # 이 파일
```

## 기술 스택

- **순수 JavaScript**: 외부 라이브러리 없음
- **HTML5 Canvas**: 고성능 렌더링
- **수학**: 복소수 연산, Möbius 변환, 쌍곡 기하학

## 성능

- 깊이 4: ~100-200 타일
- 깊이 5: ~300-500 타일
- 깊이 6: ~800-1000 타일 (최대 제한)

## 참고 자료

- [Order-3 heptagonal tiling - Verse and Dimensions Wiki](https://verse-and-dimensions.fandom.com/wiki/Order-3_heptagonal_tiling)
- Poincaré disk model - Wikipedia
- Hyperbolic geometry - 쌍곡 기하학 이론

## 라이선스

MIT License

## 작성자

Claude Code - Hyperbolic Geometry Visualization Project

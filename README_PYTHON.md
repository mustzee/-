# Order-3 Heptagonal Tiling - Python 버전

파이썬과 matplotlib을 사용한 쌍곡 기하학 시각화

## 설치

```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# 또는 직접 설치
pip install numpy matplotlib
```

## 실행

```bash
python hyperbolic_tiling.py
```

또는 실행 권한을 주고:

```bash
chmod +x hyperbolic_tiling.py
./hyperbolic_tiling.py
```

## 기능

### 인터랙티브 컨트롤

- **Depth 슬라이더**: 타일링 재귀 깊이 조절 (1-6)
  - Depth 1: 1개 타일
  - Depth 2: ~8개 타일
  - Depth 3: ~50개 타일
  - Depth 4: ~150개 타일
  - Depth 5: ~400개 타일
  - Depth 6: ~800개 타일

- **Show Edges 체크박스**: 타일 경계선 표시/숨김
- **Color Tiles 체크박스**: 타일 색상 모드 전환
- **Reset View 버튼**: 초기 뷰로 복귀

## 수학적 구현

### 핵심 알고리즘

1. **복소수 기반 계산**: 파이썬 내장 `complex` 타입 활용
2. **Möbius 변환**: 쌍곡 등거리 변환 구현
3. **측지선 렌더링**: 단위원과 직교하는 원호
4. **BFS 타일 생성**: 중앙에서 재귀적으로 확장

### 주요 클래스

- `MobiusTransform`: Möbius 변환 (쌍곡 등거리)
- `PoincareRenderer`: Poincaré disk 렌더링
- `HeptagonalTiling`: {7,3} 타일링 생성
- `HyperbolicVisualization`: 인터랙티브 UI

## 특징

- 🎨 **고품질 렌더링**: matplotlib 기반
- 🔢 **수학적 정확성**: 정확한 쌍곡 기하학 계산
- 🎮 **인터랙티브**: 실시간 파라미터 조정
- 📊 **정보 표시**: 타일 개수 등 통계

## HTML 버전과의 비교

| 기능 | Python | HTML |
|------|--------|------|
| 설치 필요 | ✓ (numpy, matplotlib) | ✗ (브라우저만) |
| 인터랙티브 | ✓ (슬라이더, 체크박스) | ✓ (마우스 드래그, 줌) |
| 성능 | 우수 | 매우 우수 |
| 사용 편의성 | 터미널 실행 | 브라우저에서 바로 |
| 확장성 | 매우 우수 | 우수 |

## 요구사항

- Python 3.7+
- NumPy 1.20+
- Matplotlib 3.3+

## 라이선스

MIT License

# pyDrone 제어 모듈 - Claude와 함께 개발

> **pyDrone vs Tello**: 실제 개발 가능성 검증 프로젝트

## 프로젝트 개요

이 프로젝트는 **pyDrone 오픈소스 드론**으로 **Claude AI와 함께 어떤 수준까지 제어 모듈 개발이 가능한지**를 실제로 검증하기 위해 만들어졌습니다.

Gemini가 Tello를 추천했지만, **진정한 드론 개발과 제어 학습**을 원한다면 pyDrone이 훨씬 더 적합합니다!

## 디렉토리 구조

```
pydrone_modules/
├── flight_control/          # 비행 제어 모듈
│   └── pid_controller.py    # PID 컨트롤러 (Tello 불가능!)
├── sensors/                 # 센서 처리 모듈
│   └── sensor_fusion.py     # 센서 퓨전 (Tello 불가능!)
├── navigation/              # 네비게이션 모듈
│   └── waypoint_navigation.py  # 웨이포인트 비행
├── telemetry/              # 텔레메트리 (향후 추가)
└── examples/               # 사용 예제
    └── pydrone_vs_tello_demo.py  # 비교 데모
```

## 핵심 기능

### ✅ pyDrone으로만 가능한 기능들

#### 1. PID 컨트롤러 (`flight_control/pid_controller.py`)

```python
from flight_control.pid_controller import AttitudePIDController

# PID 컨트롤러 초기화
pid = AttitudePIDController()

# 실시간 게인 튜닝 (Tello 불가능!)
pid.roll_pid.set_gains(kp=2.0, ki=0.02, kd=0.6)

# 자세 제어
control = pid.update(target_attitude, current_attitude, time_ms())
```

**Tello는 왜 불가능?**
- 내부 PID 컨트롤러에 접근 불가
- 게인 값 조정 불가
- 알고리즘 커스터마이징 불가

#### 2. 센서 퓨전 (`sensors/sensor_fusion.py`)

```python
from sensors.sensor_fusion import SensorFusion

# 센서 퓨전 시스템 초기화
fusion = SensorFusion()

# 센서 캘리브레이션 (Tello 불가능!)
fusion.calibrate_gyro(samples=100)

# Raw 센서 데이터 처리
state = fusion.process_raw_sensor_data(
    mpu_data,   # 가속도/자이로
    baro_data,  # 기압계
    mag_data,   # 나침반
    dt=0.01
)
```

**Tello는 왜 불가능?**
- Raw 센서 데이터 접근 불가
- 캘리브레이션 불가
- 커스텀 필터 알고리즘 적용 불가

#### 3. 웨이포인트 네비게이션 (`navigation/waypoint_navigation.py`)

```python
from navigation.waypoint_navigation import WaypointNavigator

# 네비게이터 초기화
navigator = WaypointNavigator(drone)

# 미션 설정
navigator.set_home({'x': 0, 'y': 0, 'z': 0})
navigator.add_waypoint(100, 0, 100, speed=50)
navigator.add_waypoint(100, 100, 100, speed=50, action='rotate')

# 자율 비행 실행
navigator.execute_mission()
```

**pyDrone의 장점:**
- PID 제어로 정밀한 위치 제어
- S-커브 가속/감속으로 부드러운 비행
- 실시간 궤적 조정

**Tello의 제한:**
- `go x y z` 명령으로 직선 이동만 가능
- 위치 정밀도 낮음
- 부드러운 가속/감속 불가

## pyDrone vs Tello 비교

| 기능 | pyDrone | Tello | 중요도 |
|------|---------|-------|--------|
| 센서 Raw 데이터 접근 | ✅ 완전히 가능 | ❌ 불가능 | ⭐⭐⭐⭐⭐ |
| PID 게인 튜닝 | ✅ 실시간 조정 | ❌ 불가능 | ⭐⭐⭐⭐⭐ |
| 센서 캘리브레이션 | ✅ 직접 수행 | ❌ 불가능 | ⭐⭐⭐⭐ |
| 펌웨어 수정 | ✅ 오픈소스 | ❌ 클로즈드 | ⭐⭐⭐⭐⭐ |
| 하드웨어 확장 | ✅ 가능 | ❌ 불가능 | ⭐⭐⭐⭐ |
| 데이터 로깅 | ✅ 모든 데이터 | ❌ 제한적 | ⭐⭐⭐⭐ |
| 비행 알고리즘 개발 | ✅ 완전 자유 | ❌ SDK만 | ⭐⭐⭐⭐⭐ |
| 즉시 사용 가능 | ⚠️ 조립 필요 | ✅ 즉시 사용 | ⭐⭐⭐ |
| 비행 안정성 | ⚠️ 튜닝 필요 | ✅ 검증됨 | ⭐⭐⭐⭐ |

## 데모 실행

비교 데모를 실행해보세요:

```bash
python3 examples/pydrone_vs_tello_demo.py
```

출력 내용:
- pyDrone의 고급 제어 코드 예제
- Tello의 제한적인 제어 코드
- 기능별 상세 비교표
- Claude와 함께 개발 가능한 프로젝트 시나리오
- 최종 추천

## Claude와 함께 개발 가능한 프로젝트

### pyDrone으로만 가능한 프로젝트

1. **커스텀 PID 컨트롤러 개발 및 자동 튜닝**
   - 실시간 센서 데이터로 PID 게인 자동 조정
   - Ziegler-Nichols 방법 구현
   - 비행 데이터 기반 머신러닝 튜닝

2. **고급 센서 퓨전 알고리즘**
   - Extended Kalman Filter (EKF) 구현
   - Madgwick 필터로 자세 추정
   - 센서 오차 보정 알고리즘

3. **자율 비행 연구**
   - SLAM (Simultaneous Localization and Mapping)
   - 장애물 회피 알고리즘
   - 경로 계획 알고리즘 (A*, RRT)

4. **하드웨어 확장 프로젝트**
   - GPS 모듈 추가
   - Lidar 센서 통합
   - FPV 카메라 시스템

5. **실시간 데이터 분석**
   - 비행 중 진동 분석
   - 모터 성능 모니터링
   - 배터리 수명 예측

## 최종 결론

### pyDrone을 선택해야 하는 경우 ✅

- 드론 알고리즘을 깊이 있게 배우고 싶다
- 센서 데이터와 제어 이론을 실습하고 싶다
- 연구/개발 프로젝트를 진행한다
- 하드웨어 확장을 계획하고 있다
- 완전한 제어권이 필요하다
- **Claude와 함께 고급 알고리즘을 개발하고 싶다** ⭐

### Tello를 선택해야 하는 경우 ⚠️

- 즉시 비행을 시작하고 싶다
- 안정적이고 검증된 플랫폼이 필요하다
- 드론 조립/튜닝에 시간을 쓰고 싶지 않다
- 고수준 애플리케이션 개발에만 집중하고 싶다

## 다음 단계

1. **pyDrone 구매 및 조립**
   - 공식 사이트: https://github.com/01studio-lab/pyDrone
   - 가격: ~$80-100

2. **MicroPython 펌웨어 설치**
   - 문서: https://wiki.01studio.cc/docs/pydrone/download

3. **Claude와 함께 개발 시작**
   - PID 컨트롤러 튜닝
   - 센서 캘리브레이션
   - 고급 비행 모드 개발

## 기술 스택

- **언어**: Python 3.x / MicroPython
- **하드웨어**: ESP32-S3
- **센서**: MPU6050, SPL06-001, QMC5883L
- **제어**: PID, 센서 퓨전, 웨이포인트 네비게이션
- **개발 도구**: Claude AI 🤖

## 라이센스

MIT License

## 기여

이 프로젝트는 pyDrone의 개발 가능성을 검증하기 위한 데모입니다.
실제 pyDrone 하드웨어가 있다면, 이 코드를 기반으로 실제 비행 제어를 구현할 수 있습니다.

---

**결론**: Gemini가 Tello를 추천한 이유는 '즉시 사용 가능'하기 때문입니다.
하지만 **진정한 드론 제어 모듈 개발**을 원한다면, **pyDrone이 압도적으로 우수**합니다!

Claude와 함께라면 이 모든 것을 개발할 수 있습니다! 🚀

# pyDrone 디버깅 완벽 가이드

> 문제 발생 시 해결 방법 총정리

## 🐛 디버깅 기본 원칙

```
1. 에러 메시지를 꼼꼼히 읽기
2. 가장 간단한 것부터 확인
3. 한 번에 하나씩 변경
4. 변경 사항 기록
5. Claude Code에게 도움 요청!
```

---

## 🔍 레벨 1: 기본 디버깅

### 1-1. Print 디버깅 (가장 기본!)

```python
# 나쁜 예
def update_pid(self, error):
    output = self.kp * error  # 뭔가 이상한데...
    return output

# 좋은 예
def update_pid(self, error):
    print(f"[DEBUG] error = {error}")  # 입력 확인

    output = self.kp * error
    print(f"[DEBUG] kp = {self.kp}, output = {output}")  # 중간 확인

    return output
```

### 1-2. 센서 데이터 확인

```python
# sensor_check.py

from mpu6050 import MPU6050
import time

mpu = MPU6050()

print("센서 데이터 확인 (10초)")
print("=" * 50)

for i in range(100):
    accel = mpu.get_accel()
    gyro = mpu.get_gyro()

    print(f"[{i}] Accel: ({accel['x']:.2f}, {accel['y']:.2f}, {accel['z']:.2f}) "
          f"Gyro: ({gyro['x']:.2f}, {gyro['y']:.2f}, {gyro['z']:.2f})")

    time.sleep(0.1)

    # 이상한 값 감지
    if abs(accel['x']) > 2 or abs(accel['y']) > 2:
        print("⚠️ 가속도 값 이상!")

    if abs(gyro['x']) > 200 or abs(gyro['y']) > 200:
        print("⚠️ 자이로 값 이상!")
```

### 1-3. 모터 출력 확인

```python
# motor_debug.py
# ⚠️ 프로펠러 제거 필수!

from machine import Pin, PWM
import time

motors = [
    PWM(Pin(25), freq=50),  # Motor 1
    PWM(Pin(26), freq=50),  # Motor 2
    PWM(Pin(27), freq=50),  # Motor 3
    PWM(Pin(14), freq=50),  # Motor 4
]

def test_motor(motor_num, duty):
    """특정 모터 테스트"""
    print(f"모터 {motor_num}: duty={duty}")
    motors[motor_num].duty(duty)
    time.sleep(2)
    motors[motor_num].duty(0)

print("⚠️ 프로펠러를 제거했는지 확인하세요!")
time.sleep(3)

# 각 모터를 순서대로 테스트
for i in range(4):
    print(f"\n모터 {i+1} 테스트...")
    test_motor(i, 300)  # 낮은 출력으로 시작

print("\n테스트 완료!")
```

---

## 🔬 레벨 2: 중급 디버깅

### 2-1. 메모리 사용량 확인

```python
import gc

# 가비지 컬렉션 실행
gc.collect()

# 메모리 정보
free = gc.mem_free()
allocated = gc.mem_alloc()
total = free + allocated

print(f"메모리 사용률:")
print(f"  Free: {free} bytes ({free/1024:.1f} KB)")
print(f"  Allocated: {allocated} bytes ({allocated/1024:.1f} KB)")
print(f"  Total: {total} bytes ({total/1024:.1f} KB)")
print(f"  Usage: {allocated/total*100:.1f}%")

# 경고: 사용률 80% 이상이면 위험!
if allocated/total > 0.8:
    print("⚠️ 메모리 부족! 최적화 필요!")
```

함수별 메모리 사용량:

```python
import gc

def measure_memory(func):
    """함수 실행 전후 메모리 측정 데코레이터"""
    def wrapper(*args, **kwargs):
        gc.collect()
        mem_before = gc.mem_free()

        result = func(*args, **kwargs)

        gc.collect()
        mem_after = gc.mem_free()
        used = mem_before - mem_after

        print(f"[MEM] {func.__name__}: {used} bytes")

        return result
    return wrapper

# 사용 예
@measure_memory
def heavy_function():
    big_list = [0] * 1000
    return big_list

heavy_function()
# 출력: [MEM] heavy_function: 4024 bytes
```

### 2-2. 실행 시간 측정 (프로파일링)

```python
import time

def profile(func):
    """함수 실행 시간 측정 데코레이터"""
    def wrapper(*args, **kwargs):
        start = time.ticks_us()
        result = func(*args, **kwargs)
        elapsed = time.ticks_diff(time.ticks_us(), start)

        print(f"[TIME] {func.__name__}: {elapsed} μs ({elapsed/1000:.2f} ms)")

        return result
    return wrapper

# 사용 예
@profile
def update_pid(error):
    # PID 계산...
    time.sleep_us(500)  # 시뮬레이션
    return error * 1.5

result = update_pid(10)
# 출력: [TIME] update_pid: 523 μs (0.52 ms)
```

제어 루프 성능 측정:

```python
import time

# 목표: 100Hz (10ms per loop)
TARGET_LOOP_TIME = 10  # ms

loop_times = []
max_time = 0
min_time = float('inf')

for i in range(1000):
    start = time.ticks_ms()

    # === 제어 루프 ===
    sensor_data = read_sensors()
    control_output = calculate_pid(sensor_data)
    apply_motors(control_output)
    # ==================

    elapsed = time.ticks_diff(time.ticks_ms(), start)

    loop_times.append(elapsed)
    max_time = max(max_time, elapsed)
    min_time = min(min_time, elapsed)

    if elapsed > TARGET_LOOP_TIME:
        print(f"⚠️ Loop {i}: {elapsed}ms (목표: {TARGET_LOOP_TIME}ms)")

# 통계
avg_time = sum(loop_times) / len(loop_times)
print(f"\n루프 성능:")
print(f"  평균: {avg_time:.2f}ms")
print(f"  최소: {min_time}ms")
print(f"  최대: {max_time}ms")
print(f"  목표: {TARGET_LOOP_TIME}ms")

if avg_time > TARGET_LOOP_TIME:
    print(f"⚠️ 성능 부족! 최적화 필요!")
```

### 2-3. 로깅 시스템

```python
# logger.py

import time

class Logger:
    """간단한 로깅 시스템"""

    LEVEL_DEBUG = 0
    LEVEL_INFO = 1
    LEVEL_WARNING = 2
    LEVEL_ERROR = 3

    def __init__(self, level=LEVEL_INFO, filename=None):
        self.level = level
        self.filename = filename

        if filename:
            # 파일 초기화
            with open(filename, 'w') as f:
                f.write(f"# Log started at {time.time()}\n")

    def _log(self, level, message):
        """내부 로깅 함수"""
        if level < self.level:
            return  # 레벨이 낮으면 무시

        level_names = ['DEBUG', 'INFO', 'WARN', 'ERROR']
        timestamp = time.ticks_ms()
        log_line = f"[{timestamp}] [{level_names[level]}] {message}"

        # 콘솔 출력
        print(log_line)

        # 파일 저장
        if self.filename:
            with open(self.filename, 'a') as f:
                f.write(log_line + '\n')

    def debug(self, message):
        self._log(self.LEVEL_DEBUG, message)

    def info(self, message):
        self._log(self.LEVEL_INFO, message)

    def warning(self, message):
        self._log(self.LEVEL_WARNING, message)

    def error(self, message):
        self._log(self.LEVEL_ERROR, message)


# 사용 예
log = Logger(level=Logger.LEVEL_DEBUG, filename='/sd/flight.log')

log.info("드론 시작")
log.debug(f"센서 값: roll={roll}, pitch={pitch}")
log.warning("배터리 낮음!")
log.error("IMU 센서 응답 없음!")
```

---

## 🚨 레벨 3: 고급 디버깅

### 3-1. 예외 처리 및 추적

```python
import sys
import io

def safe_execute(func, *args, **kwargs):
    """안전한 함수 실행 (예외 처리)"""
    try:
        return func(*args, **kwargs)

    except Exception as e:
        # 에러 정보 수집
        print("=" * 50)
        print(f"⚠️ Exception in {func.__name__}")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")

        # 스택 트레이스
        print("\nStack trace:")
        sys.print_exception(e)
        print("=" * 50)

        return None

# 사용 예
def risky_function(x):
    return 10 / x  # x=0이면 에러!

result = safe_execute(risky_function, 0)
# 에러 정보가 깔끔하게 출력됨
```

### 3-2. 실시간 변수 모니터링

```python
# variable_monitor.py

import time

class VariableMonitor:
    """변수 값 실시간 모니터링"""

    def __init__(self):
        self.variables = {}
        self.history = {}

    def watch(self, name, value):
        """변수 감시"""
        # 이전 값과 비교
        if name in self.variables:
            old_value = self.variables[name]
            delta = value - old_value

            # 큰 변화 감지
            if abs(delta) > abs(old_value) * 0.5:  # 50% 이상 변화
                print(f"⚠️ {name}: {old_value:.2f} → {value:.2f} (Δ{delta:+.2f})")

        self.variables[name] = value

        # 히스토리 저장
        if name not in self.history:
            self.history[name] = []
        self.history[name].append((time.ticks_ms(), value))

    def get_stats(self, name):
        """변수 통계"""
        if name not in self.history:
            return None

        values = [v for t, v in self.history[name]]

        return {
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'count': len(values)
        }

# 사용 예
monitor = VariableMonitor()

for i in range(100):
    # 센서 읽기
    roll = read_roll()
    pitch = read_pitch()

    # 모니터링
    monitor.watch('roll', roll)
    monitor.watch('pitch', pitch)

    time.sleep(0.1)

# 통계 출력
print(monitor.get_stats('roll'))
# {'min': -5.2, 'max': 5.8, 'avg': 0.3, 'count': 100}
```

### 3-3. 센서 캘리브레이션 검증

```python
# calibration_check.py

import time
from mpu6050 import MPU6050

mpu = MPU6050()

print("센서를 평평한 곳에 두세요...")
print("5초 후 캘리브레이션 확인 시작")
time.sleep(5)

# 100개 샘플 수집
samples = {
    'accel_x': [],
    'accel_y': [],
    'accel_z': [],
    'gyro_x': [],
    'gyro_y': [],
    'gyro_z': []
}

print("샘플 수집 중...")
for i in range(100):
    accel = mpu.get_accel()
    gyro = mpu.get_gyro()

    samples['accel_x'].append(accel['x'])
    samples['accel_y'].append(accel['y'])
    samples['accel_z'].append(accel['z'])
    samples['gyro_x'].append(gyro['x'])
    samples['gyro_y'].append(gyro['y'])
    samples['gyro_z'].append(gyro['z'])

    time.sleep(0.01)

# 통계 계산
def stats(data):
    avg = sum(data) / len(data)
    variance = sum((x - avg)**2 for x in data) / len(data)
    stddev = variance ** 0.5
    return avg, stddev

print("\n캘리브레이션 검증 결과:")
print("=" * 60)

print("\n가속도계 (정지 시 X≈0, Y≈0, Z≈1g):")
for axis in ['accel_x', 'accel_y', 'accel_z']:
    avg, std = stats(samples[axis])
    print(f"  {axis}: 평균={avg:.3f}, 표준편차={std:.3f}")

    expected = 1.0 if axis == 'accel_z' else 0.0
    error = abs(avg - expected)

    if error > 0.1:
        print(f"    ⚠️ 오차 큼! ({error:.3f}g) - 재캘리브레이션 필요")

print("\n자이로스코프 (정지 시 모두 ≈0):")
for axis in ['gyro_x', 'gyro_y', 'gyro_z']:
    avg, std = stats(samples[axis])
    print(f"  {axis}: 평균={avg:.3f}, 표준편차={std:.3f}")

    if abs(avg) > 2.0:  # 2도/s 이상이면 문제
        print(f"    ⚠️ 드리프트 발생! - 재캘리브레이션 필요")

    if std > 1.0:  # 노이즈가 크면 문제
        print(f"    ⚠️ 노이즈 큼! - 필터링 필요")
```

---

## 🔧 일반적인 문제 해결

### 문제 1: "ImportError: no module named 'xxx'"

```python
# 원인: 모듈 파일이 pyDrone에 없음

# 해결:
# 1. 파일 존재 확인
>>> import os
>>> os.listdir()
['boot.py', 'main.py']  # xxx.py가 없음!

# 2. 파일 업로드
# rshell 또는 WebREPL로 업로드

# 3. 경로 확인
>>> os.listdir('/lib')  # lib 폴더 확인
```

### 문제 2: "MemoryError"

```python
# 원인: 메모리 부족

# 해결 1: 가비지 컬렉션
import gc
gc.collect()  # 사용하지 않는 메모리 해제

# 해결 2: 큰 변수 삭제
del big_list
gc.collect()

# 해결 3: 코드 최적화
# 나쁜 예: 큰 리스트 생성
data = [0] * 10000

# 좋은 예: 제너레이터 사용
data = (0 for _ in range(10000))

# 해결 4: 모듈 언로드
import sys
del sys.modules['heavy_module']
gc.collect()
```

### 문제 3: "OSError: [Errno 28] No space left on device"

```python
# 원인: 플래시 메모리 가득 참

# 해결 1: 파일 확인
>>> import os
>>> os.listdir()

# 해결 2: 불필요한 파일 삭제
>>> os.remove('old_file.py')

# 해결 3: 로그 파일 정리
>>> os.remove('/sd/old_log.csv')

# 해결 4: 펌웨어 재설치 (모든 파일 삭제됨!)
```

### 문제 4: 센서 값이 이상해요

```python
# 증상: NaN, inf, 또는 말도 안 되는 값

# 체크리스트:
# 1. I2C 연결 확인
>>> from machine import I2C, Pin
>>> i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
>>> i2c.scan()
[104, 118, 13]  # 센서 주소가 보여야 함

# 2. 전원 확인
#    - 배터리 전압 충분한지
#    - 센서 VCC 연결 확인

# 3. 센서 초기화 확인
>>> from mpu6050 import MPU6050
>>> mpu = MPU6050()
>>> mpu.test_connection()
True  # True여야 정상

# 4. 값 범위 확인
>>> accel = mpu.get_accel()
>>> print(accel)
{'x': 0.05, 'y': -0.02, 'z': 0.98}  # 정상 (±2g 이내)

# 5. 재캘리브레이션
# (위 3-3 섹션 참고)
```

### 문제 5: 모터가 안 돌아가요

```python
# ⚠️ 프로펠러 제거 확인!

# 체크리스트:
# 1. 모터 연결 확인
#    - 커넥터 단단히 연결되었는지
#    - 4개 모터 모두 연결되었는지

# 2. ESC 초기화 확인
from machine import Pin, PWM

motor = PWM(Pin(25), freq=50)
motor.duty(0)  # 먼저 0으로

# ESC 초기화 시퀀스
motor.duty(1023)  # 최대
time.sleep(2)
motor.duty(0)  # 최소
time.sleep(2)
motor.duty(300)  # 테스트 (모터 회전해야 함)

# 3. PWM 주파수 확인
#    - 일반적으로 50Hz 또는 490Hz

# 4. Duty 범위 확인
#    - 0~1023 (10비트)
#    - 너무 낮으면 안 돌아감 (>200 필요)
```

---

## 💬 Claude Code에게 도움 요청하기

### 효과적인 질문 방법

#### ❌ 나쁜 예

```
"드론이 안 돼요"
```

#### ✅ 좋은 예

```
"pyDrone의 PID 컨트롤러를 테스트 중인데 다음 문제가 발생했어요:

증상:
- Roll 값이 -5°~5° 사이에서 계속 진동
- 주파수: 약 2Hz
- 목표 값: 0°

환경:
- pyDrone ESP32-S3
- MicroPython 1.20
- lib/pid_controller.py 사용 중

코드:
```python
pid = PIDController(kp=2.0, ki=0.1, kd=0.5)
output = pid.update(0, current_roll, time_ms)
```

로그 데이터:
[첨부: pid_log.csv]

어떻게 해결할 수 있을까요?"
```

Claude가 분석할 수 있는 정보:
1. 구체적인 증상
2. 환경 정보
3. 사용 중인 코드
4. 로그 데이터
5. 명확한 질문

### 디버깅 요청 템플릿

```markdown
## 문제 설명
[문제를 한 문장으로]

## 증상
- [구체적인 증상 1]
- [구체적인 증상 2]

## 환경
- 하드웨어: pyDrone ESP32-S3
- 펌웨어: [버전]
- 관련 코드: [파일명]

## 재현 방법
1. [단계 1]
2. [단계 2]
3. [결과]

## 시도한 방법
- [시도 1] → [결과]
- [시도 2] → [결과]

## 에러 메시지
```
[에러 메시지 전체 복사]
```

## 관련 코드
```python
[문제가 발생하는 코드]
```

## 로그/데이터
[첨부 파일 또는 복사]

## 질문
[구체적인 질문]
```

---

## 📊 디버깅 체크리스트

비행 전 체크:

```
하드웨어:
□ 배터리 충전 확인 (>50%)
□ 프로펠러 장착 확인 (A, B 구분)
□ 모터 회전 방향 확인
□ 센서 연결 확인

소프트웨어:
□ 센서 캘리브레이션 완료
□ PID 게인 설정 확인
□ 로깅 활성화
□ 안전 기능 활성화 (페일세이프 등)

환경:
□ 충분한 공간 확보 (최소 3x3m)
□ 바람 확인 (<10km/h)
□ 장애물 제거
```

비행 중 모니터링:

```
□ 배터리 전압 (실시간)
□ Roll/Pitch/Yaw 값
□ 고도
□ 모터 출력
□ 제어 루프 시간
```

비행 후 분석:

```
□ 로그 파일 다운로드
□ 그래프로 시각화
□ 이상 값 확인
□ Claude에게 분석 요청
```

---

## 🎓 요약

```
디버깅 레벨:

Level 1 (기본):
✓ print() 디버깅
✓ 센서 값 확인
✓ 모터 테스트

Level 2 (중급):
✓ 메모리 모니터링
✓ 성능 프로파일링
✓ 로깅 시스템

Level 3 (고급):
✓ 예외 처리
✓ 변수 모니터링
✓ 캘리브레이션 검증

항상:
✓ Claude Code에게 도움 요청
✓ 체크리스트 확인
✓ 안전 최우선
```

**문제가 생기면 당황하지 말고, 체계적으로 접근하세요!** 🔍

Claude Code가 항상 함께합니다! 🤖

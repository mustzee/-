"""
pyDrone vs Tello 직접 비교 데모
실제 개발 가능성을 명확하게 보여주는 예제
"""


def pydrone_advanced_flight():
    """
    pyDrone으로 가능한 고급 비행 제어
    ✅ 완전히 가능!
    """
    print("=" * 70)
    print("pyDrone: 고급 비행 제어 (Claude와 함께 개발 가능!)")
    print("=" * 70)

    # pyDrone 코드
    code = '''
from drone import DRONE
from flight_control.pid_controller import AttitudePIDController
from sensors.sensor_fusion import SensorFusion
from navigation.waypoint_navigation import WaypointNavigator

# 1. 드론 초기화
d = DRONE(flightmode=0)
pid = AttitudePIDController()
sensor_fusion = SensorFusion()
navigator = WaypointNavigator(d)

# 2. 센서 캘리브레이션 (pyDrone만 가능!)
sensor_fusion.calibrate_gyro(samples=100)
print("센서 캘리브레이션 완료!")

# 3. PID 게인 튜닝 (pyDrone만 가능!)
pid.roll_pid.set_gains(kp=2.0, ki=0.02, kd=0.6)
pid.pitch_pid.set_gains(kp=2.0, ki=0.02, kd=0.6)
print("PID 게인 조정 완료!")

# 4. 이륙
d.takeoff()

# 5. 실시간 센서 데이터 읽기 (pyDrone만 가능!)
while True:
    # Raw 센서 데이터 획득
    mpu_data = d.get_mpu6050_data()  # 가속도/자이로
    baro_data = d.get_barometer_data()  # 기압
    mag_data = d.get_compass_data()  # 나침반

    # 센서 퓨전으로 정확한 자세 추정
    state = sensor_fusion.process_raw_sensor_data(
        mpu_data, baro_data, mag_data, dt=0.01
    )

    # 목표 자세 설정
    target = {'roll': 0, 'pitch': 10, 'yaw': 0, 'altitude': 150}

    # PID 컨트롤러로 제어값 계산
    control = pid.update(target, state, time_ms())

    # 드론 제어
    d.control(**control)

    # 실시간 로깅 (pyDrone만 가능!)
    print(f"Roll: {state['roll']:.2f}°, Pitch: {state['pitch']:.2f}°, "
          f"Alt: {state['altitude']:.1f}cm")

    if some_condition:
        break

# 6. 착륙
d.landing()
    '''

    print(code)
    print()
    print("✅ pyDrone의 강력한 기능:")
    print("  ✓ Raw 센서 데이터 직접 접근")
    print("  ✓ 센서 캘리브레이션")
    print("  ✓ PID 게인 실시간 튜닝")
    print("  ✓ 커스텀 센서 퓨전 알고리즘")
    print("  ✓ 정밀한 자세 제어")
    print("  ✓ 실시간 데이터 로깅")
    print()


def tello_limited_flight():
    """
    Tello의 제한적인 비행 제어
    ⚠️ 고수준 명령만 가능
    """
    print("=" * 70)
    print("Tello: 제한적인 고수준 명령 (내부 접근 불가)")
    print("=" * 70)

    # Tello 코드
    code = '''
from djitellopy import Tello

# 1. Tello 연결
tello = Tello()
tello.connect()

# 2. 센서 캘리브레이션? ❌ 불가능!
# 내부 센서에 접근할 수 없습니다

# 3. PID 튜닝? ❌ 불가능!
# 내부 PID 컨트롤러를 수정할 수 없습니다

# 4. 이륙
tello.takeoff()

# 5. 고수준 명령만 가능
tello.move_forward(100)  # 1m 전진
tello.move_left(50)      # 50cm 좌측
tello.rotate_clockwise(90)  # 90도 회전

# Raw 센서 데이터? ❌ 불가능!
# 제한적인 상태 정보만 얻을 수 있습니다:
battery = tello.get_battery()
height = tello.get_height()
# 그게 전부입니다...

# 정밀한 제어? ❌ 불가능!
# go 명령으로 대략적인 이동만 가능:
tello.go_xyz_speed(100, 0, 0, 50)

# 6. 착륙
tello.land()
    '''

    print(code)
    print()
    print("❌ Tello의 제한사항:")
    print("  ✗ Raw 센서 데이터 접근 불가")
    print("  ✗ 센서 캘리브레이션 불가")
    print("  ✗ PID 게인 튜닝 불가")
    print("  ✗ 내부 알고리즘 수정 불가")
    print("  ✗ 정밀한 자세 제어 불가")
    print("  ✗ 하드웨어 확장 불가")
    print()


def comparison_table():
    """
    기능별 상세 비교표
    """
    print("=" * 70)
    print("pyDrone vs Tello: 기능별 상세 비교")
    print("=" * 70)
    print()

    features = [
        ("기능", "pyDrone", "Tello", "중요도"),
        ("-" * 20, "-" * 20, "-" * 20, "-" * 10),
        ("센서 Raw 데이터 접근", "✅ 완전히 가능", "❌ 불가능", "⭐⭐⭐⭐⭐"),
        ("PID 게인 튜닝", "✅ 실시간 조정", "❌ 불가능", "⭐⭐⭐⭐⭐"),
        ("센서 캘리브레이션", "✅ 직접 수행", "❌ 불가능", "⭐⭐⭐⭐"),
        ("펌웨어 수정", "✅ 오픈소스", "❌ 클로즈드", "⭐⭐⭐⭐⭐"),
        ("하드웨어 확장", "✅ 가능", "❌ 불가능", "⭐⭐⭐⭐"),
        ("데이터 로깅", "✅ 모든 데이터", "❌ 제한적", "⭐⭐⭐⭐"),
        ("비행 알고리즘 개발", "✅ 완전 자유", "❌ SDK만", "⭐⭐⭐⭐⭐"),
        ("즉시 사용 가능", "⚠️ 조립 필요", "✅ 즉시 사용", "⭐⭐⭐"),
        ("비행 안정성", "⚠️ 튜닝 필요", "✅ 검증됨", "⭐⭐⭐⭐"),
        ("커뮤니티 크기", "⚠️ 작음", "✅ 큼", "⭐⭐⭐"),
        ("교육용", "✅ 탁월함", "✅ 좋음", "⭐⭐⭐⭐"),
        ("연구/개발용", "✅ 최고", "⚠️ 제한적", "⭐⭐⭐⭐⭐"),
        ("가격", "$80-100", "$100-130", "⭐⭐⭐"),
    ]

    for feature in features:
        print(f"{feature[0]:<25} {feature[1]:<20} {feature[2]:<20} {feature[3]:<10}")

    print()


def claude_development_scenarios():
    """
    Claude와 함께 개발 가능한 시나리오
    """
    print("=" * 70)
    print("Claude와 함께 개발 가능한 프로젝트 시나리오")
    print("=" * 70)
    print()

    scenarios = {
        "pyDrone으로만 가능한 프로젝트": [
            "1. 커스텀 PID 컨트롤러 개발 및 자동 튜닝",
            "   - 실시간 센서 데이터로 PID 게인 자동 조정",
            "   - Ziegler-Nichols 방법 구현",
            "   - 비행 데이터 기반 머신러닝 튜닝",
            "",
            "2. 고급 센서 퓨전 알고리즘",
            "   - Extended Kalman Filter (EKF) 구현",
            "   - Madgwick 필터로 자세 추정",
            "   - 센서 오차 보정 알고리즘",
            "",
            "3. 자율 비행 연구",
            "   - SLAM (Simultaneous Localization and Mapping)",
            "   - 장애물 회피 알고리즘",
            "   - 경로 계획 알고리즘 (A*, RRT)",
            "",
            "4. 하드웨어 확장 프로젝트",
            "   - GPS 모듈 추가",
            "   - Lidar 센서 통합",
            "   - FPV 카메라 시스템",
            "",
            "5. 실시간 데이터 분석",
            "   - 비행 중 진동 분석",
            "   - 모터 성능 모니터링",
            "   - 배터리 수명 예측",
        ],
        "Tello와 pyDrone 모두 가능 (pyDrone이 더 유리)": [
            "1. 웨이포인트 네비게이션",
            "   - pyDrone: 정밀한 PID 제어",
            "   - Tello: go 명령으로 대략적 이동",
            "",
            "2. 컴퓨터 비전 애플리케이션",
            "   - pyDrone: 카메라 직접 제어",
            "   - Tello: SDK로 비디오 스트림",
            "",
            "3. 군집 비행 (Swarm)",
            "   - pyDrone: 완전한 제어",
            "   - Tello EDU: SDK 3.0 지원",
        ],
        "Tello가 더 적합한 경우": [
            "1. 빠른 프로토타이핑",
            "   - 즉시 사용 가능",
            "   - 안정적인 비행",
            "",
            "2. 초보자 교육",
            "   - Scratch 프로그래밍",
            "   - 간단한 Python 스크립트",
            "",
            "3. 앱 개발",
            "   - 모바일 앱 연동",
            "   - 간단한 원격 조종",
        ]
    }

    for category, items in scenarios.items():
        print(f"📌 {category}")
        print()
        for item in items:
            print(f"   {item}")
        print()


def final_recommendation():
    """
    최종 추천
    """
    print("=" * 70)
    print("🎯 최종 결론 및 추천")
    print("=" * 70)
    print()

    print("Claude와 함께 드론 개발을 한다면:")
    print()
    print("✅ pyDrone을 선택해야 하는 경우:")
    print("  • 드론 알고리즘을 깊이 있게 배우고 싶다")
    print("  • 센서 데이터와 제어 이론을 실습하고 싶다")
    print("  • 연구/개발 프로젝트를 진행한다")
    print("  • 하드웨어 확장을 계획하고 있다")
    print("  • 완전한 제어권이 필요하다")
    print("  • Claude와 함께 고급 알고리즘을 개발하고 싶다 ⭐")
    print()

    print("✅ Tello를 선택해야 하는 경우:")
    print("  • 즉시 비행을 시작하고 싶다")
    print("  • 안정적이고 검증된 플랫폼이 필요하다")
    print("  • 드론 조립/튜닝에 시간을 쓰고 싶지 않다")
    print("  • 고수준 애플리케이션 개발에만 집중하고 싶다")
    print("  • 미션 패드, 군집 비행 기능이 필요하다 (EDU)")
    print()

    print("💡 Claude의 추천:")
    print()
    print("  Gemini가 Tello를 추천한 이유는 '즉시 사용 가능'하기 때문입니다.")
    print("  하지만 당신이 '제어 모듈 관리'와 '개발'에 관심이 있다면,")
    print("  pyDrone이 훨씬 더 적합합니다!")
    print()
    print("  pyDrone으로 할 수 있는 것:")
    print("  ✓ PID 컨트롤러 직접 개발 및 튜닝")
    print("  ✓ 센서 퓨전 알고리즘 구현")
    print("  ✓ 커스텀 비행 모드 개발")
    print("  ✓ 하드웨어 확장 (GPS, Lidar 등)")
    print("  ✓ 실시간 데이터 분석 및 로깅")
    print()
    print("  이 모든 것을 Claude와 함께 개발할 수 있습니다! 🚀")
    print()

    print("📚 다음 단계:")
    print("  1. pyDrone 구매 및 조립")
    print("  2. MicroPython 펌웨어 설치")
    print("  3. Claude와 함께 PID 컨트롤러 튜닝")
    print("  4. 센서 캘리브레이션 수행")
    print("  5. 고급 비행 모드 개발 시작")
    print()


if __name__ == "__main__":
    print("\n")
    print("🚁" * 35)
    print()
    print("         pyDrone vs Tello: 개발자 관점 완전 비교")
    print()
    print("🚁" * 35)
    print("\n")

    pydrone_advanced_flight()
    print("\n")

    tello_limited_flight()
    print("\n")

    comparison_table()
    print("\n")

    claude_development_scenarios()
    print("\n")

    final_recommendation()

    print("=" * 70)
    print("이 모든 pyDrone 모듈들은 현재 저장소에 있습니다!")
    print("pydrone_modules/ 디렉토리를 확인하세요.")
    print("=" * 70)

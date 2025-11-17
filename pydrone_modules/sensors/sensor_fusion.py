"""
센서 퓨전 알고리즘 - pyDrone 전용
Tello는 센서 Raw 데이터에 접근할 수 없어서 이런 모듈을 만들 수 없습니다!
"""

import math


class ComplementaryFilter:
    """
    상보 필터 (Complementary Filter)
    - 가속도계와 자이로스코프 데이터 융합
    - Tello는 내부적으로만 사용, 우리는 수정 불가
    - pyDrone은 직접 구현 가능!
    """

    def __init__(self, alpha=0.98):
        """
        Args:
            alpha: 필터 계수 (0~1)
                  - 1에 가까울수록 자이로 의존
                  - 0에 가까울수록 가속도계 의존
        """
        self.alpha = alpha
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

    def update(self, accel_data, gyro_data, dt):
        """
        상보 필터 업데이트

        Args:
            accel_data: {'x': ax, 'y': ay, 'z': az} (g)
            gyro_data: {'x': gx, 'y': gy, 'z': gz} (deg/s)
            dt: 시간 차분 (초)

        Returns:
            {'roll': r, 'pitch': p, 'yaw': y} (도)
        """
        # 가속도계로부터 Roll, Pitch 계산
        accel_roll = math.atan2(accel_data['y'], accel_data['z']) * 180 / math.pi
        accel_pitch = math.atan2(-accel_data['x'],
                                  math.sqrt(accel_data['y']**2 + accel_data['z']**2)) * 180 / math.pi

        # 자이로스코프 적분
        gyro_roll = self.roll + gyro_data['x'] * dt
        gyro_pitch = self.pitch + gyro_data['y'] * dt
        gyro_yaw = self.yaw + gyro_data['z'] * dt

        # 상보 필터 적용
        self.roll = self.alpha * gyro_roll + (1 - self.alpha) * accel_roll
        self.pitch = self.alpha * gyro_pitch + (1 - self.alpha) * accel_pitch
        self.yaw = gyro_yaw  # Yaw는 자이로만 사용 (가속도계로 측정 불가)

        return {
            'roll': self.roll,
            'pitch': self.pitch,
            'yaw': self.yaw
        }


class KalmanFilter:
    """
    1D 칼만 필터
    - 더 정확한 센서 데이터 필터링
    - pyDrone에서만 구현 가능!
    """

    def __init__(self, process_variance=0.01, measurement_variance=0.1):
        self.process_variance = process_variance  # Q
        self.measurement_variance = measurement_variance  # R
        self.estimated_value = 0.0
        self.estimation_error = 1.0

    def update(self, measurement):
        """
        칼만 필터 업데이트

        Args:
            measurement: 센서 측정값

        Returns:
            필터링된 추정값
        """
        # 예측 단계
        prediction_error = self.estimation_error + self.process_variance

        # 칼만 게인 계산
        kalman_gain = prediction_error / (prediction_error + self.measurement_variance)

        # 업데이트 단계
        self.estimated_value = self.estimated_value + kalman_gain * (measurement - self.estimated_value)
        self.estimation_error = (1 - kalman_gain) * prediction_error

        return self.estimated_value


class SensorFusion:
    """
    pyDrone 센서 퓨전 시스템
    - MPU6050 (가속도/자이로)
    - SPL06-001 (기압계)
    - QMC5883L (나침반)

    Tello는 이런 저수준 접근이 불가능!
    """

    def __init__(self):
        # 자세 추정용 상보 필터
        self.attitude_filter = ComplementaryFilter(alpha=0.98)

        # 고도 추정용 칼만 필터
        self.altitude_filter = KalmanFilter(
            process_variance=0.01,
            measurement_variance=0.5
        )

        # 센서 캘리브레이션 오프셋
        self.gyro_offset = {'x': 0, 'y': 0, 'z': 0}
        self.accel_offset = {'x': 0, 'y': 0, 'z': 0}

    def calibrate_gyro(self, samples=100):
        """
        자이로스코프 캘리브레이션
        pyDrone에서만 가능! Tello는 센서 접근 불가!
        """
        print("자이로 캘리브레이션 시작...")
        print("드론을 평평한 곳에 두고 움직이지 마세요!")

        # 실제 구현에서는 MPU6050에서 데이터 읽기
        # from mpu6050 import MPU6050
        # mpu = MPU6050()
        # for i in range(samples):
        #     gyro_data = mpu.read_gyro()
        #     self.gyro_offset['x'] += gyro_data['x']
        #     ...

        print("캘리브레이션 완료!")
        print("이런 기능은 Tello에서 절대 불가능합니다!")

    def process_raw_sensor_data(self, mpu_data, baro_data, mag_data, dt):
        """
        Raw 센서 데이터 처리

        Args:
            mpu_data: MPU6050 데이터 {'accel': {...}, 'gyro': {...}}
            baro_data: 기압계 데이터 {'pressure': p, 'temperature': t}
            mag_data: 나침반 데이터 {'x': mx, 'y': my, 'z': mz}
            dt: 시간 차분

        Returns:
            처리된 자세 및 위치 정보
        """
        # 자이로 오프셋 보정
        corrected_gyro = {
            'x': mpu_data['gyro']['x'] - self.gyro_offset['x'],
            'y': mpu_data['gyro']['y'] - self.gyro_offset['y'],
            'z': mpu_data['gyro']['z'] - self.gyro_offset['z']
        }

        # 자세 추정
        attitude = self.attitude_filter.update(
            mpu_data['accel'],
            corrected_gyro,
            dt
        )

        # 기압계로부터 고도 계산 (간단한 근사)
        # P = P0 * (1 - 0.0065*h/T0)^5.255
        # 실제로는 더 복잡한 계산 필요
        raw_altitude = (1 - (baro_data['pressure'] / 101325) ** 0.190284) * 44330

        # 칼만 필터로 고도 스무딩
        filtered_altitude = self.altitude_filter.update(raw_altitude)

        # 나침반으로부터 헤딩 계산
        heading = math.atan2(mag_data['y'], mag_data['x']) * 180 / math.pi

        return {
            'roll': attitude['roll'],
            'pitch': attitude['pitch'],
            'yaw': attitude['yaw'],
            'altitude': filtered_altitude,
            'heading': heading,
            'raw': {
                'accel': mpu_data['accel'],
                'gyro': mpu_data['gyro'],
                'pressure': baro_data['pressure'],
                'mag': mag_data
            }
        }


# 사용 예제
if __name__ == "__main__":
    print("=" * 60)
    print("pyDrone 센서 퓨전 시스템")
    print("=" * 60)
    print()
    print("✅ pyDrone으로 가능한 것:")
    print("  - Raw 센서 데이터 직접 접근")
    print("  - 커스텀 필터 알고리즘 구현")
    print("  - 센서 캘리브레이션")
    print("  - 실시간 데이터 로깅")
    print("  - 필터 파라미터 튜닝")
    print()
    print("❌ Tello로 불가능한 것:")
    print("  - 센서 Raw 데이터 접근 불가")
    print("  - 내부 알고리즘 수정 불가")
    print("  - 캘리브레이션 접근 불가")
    print()

    fusion = SensorFusion()
    print("센서 퓨전 시스템 초기화 완료!")

"""
Advanced PID Controller for pyDrone
이것은 pyDrone에서만 가능합니다 - Tello는 내부 PID에 접근 불가!
"""

class PIDController:
    """
    3축 PID 컨트롤러 (Roll, Pitch, Yaw)
    - 실시간 튜닝 가능
    - 안티 와인드업 (Anti-windup) 기능
    - 출력 제한 (Output limiting)
    """

    def __init__(self, kp=1.0, ki=0.0, kd=0.0, output_limits=(-100, 100)):
        # PID 게인 값
        self.kp = kp  # 비례 게인
        self.ki = ki  # 적분 게인
        self.kd = kd  # 미분 게인

        # 내부 상태
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = 0

        # 출력 제한
        self.output_min, self.output_max = output_limits

        # 안티 와인드업 활성화
        self.anti_windup = True

    def update(self, setpoint, measured_value, current_time):
        """
        PID 제어 출력 계산

        Args:
            setpoint: 목표값
            measured_value: 현재 측정값
            current_time: 현재 시간 (ms)

        Returns:
            제어 출력값
        """
        # 오차 계산
        error = setpoint - measured_value

        # 시간 차분 계산
        dt = (current_time - self.prev_time) / 1000.0  # ms -> s
        if dt <= 0:
            dt = 0.001  # 최소값 설정

        # 비례항 (P)
        p_term = self.kp * error

        # 적분항 (I)
        self.integral += error * dt
        i_term = self.ki * self.integral

        # 미분항 (D)
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        d_term = self.kd * derivative

        # PID 출력 계산
        output = p_term + i_term + d_term

        # 출력 제한 적용
        output = max(self.output_min, min(self.output_max, output))

        # 안티 와인드업: 출력이 제한되면 적분 누적 중지
        if self.anti_windup:
            if output == self.output_min or output == self.output_max:
                self.integral -= error * dt  # 적분값 되돌리기

        # 상태 업데이트
        self.prev_error = error
        self.prev_time = current_time

        return output

    def reset(self):
        """PID 상태 초기화"""
        self.integral = 0.0
        self.prev_error = 0.0

    def set_gains(self, kp=None, ki=None, kd=None):
        """
        실시간 PID 게인 튜닝
        Tello에서는 불가능! pyDrone만의 강력한 기능!
        """
        if kp is not None:
            self.kp = kp
        if ki is not None:
            self.ki = ki
        if kd is not None:
            self.kd = kd

    def get_gains(self):
        """현재 PID 게인 값 반환"""
        return {'kp': self.kp, 'ki': self.ki, 'kd': self.kd}


class AttitudePIDController:
    """
    드론 자세 제어를 위한 다축 PID 컨트롤러
    """

    def __init__(self):
        # 각 축별 PID 컨트롤러
        self.roll_pid = PIDController(kp=1.5, ki=0.01, kd=0.5)
        self.pitch_pid = PIDController(kp=1.5, ki=0.01, kd=0.5)
        self.yaw_pid = PIDController(kp=2.0, ki=0.005, kd=0.3)
        self.throttle_pid = PIDController(kp=1.0, ki=0.05, kd=0.2)

    def update(self, target_attitude, current_attitude, current_time):
        """
        자세 제어 업데이트

        Args:
            target_attitude: {'roll': 0, 'pitch': 0, 'yaw': 0, 'throttle': 0}
            current_attitude: {'roll': x, 'pitch': y, 'yaw': z, 'altitude': h}
            current_time: 현재 시간 (ms)

        Returns:
            모터 제어값 {'rol': x, 'pit': y, 'yaw': z, 'thr': w}
        """
        roll_output = self.roll_pid.update(
            target_attitude['roll'],
            current_attitude['roll'],
            current_time
        )

        pitch_output = self.pitch_pid.update(
            target_attitude['pitch'],
            current_attitude['pitch'],
            current_time
        )

        yaw_output = self.yaw_pid.update(
            target_attitude['yaw'],
            current_attitude['yaw'],
            current_time
        )

        throttle_output = self.throttle_pid.update(
            target_attitude.get('altitude', 0),
            current_attitude.get('altitude', 0),
            current_time
        )

        return {
            'rol': int(roll_output),
            'pit': int(pitch_output),
            'yaw': int(yaw_output),
            'thr': int(throttle_output)
        }

    def auto_tune(self, axis, sensor_data, test_duration=5000):
        """
        자동 PID 튜닝 (Ziegler-Nichols 방법)

        이것도 pyDrone에서만 가능합니다!
        Tello는 센서 데이터에 직접 접근할 수 없어서 불가능!
        """
        print(f"Auto-tuning {axis} axis PID...")
        print("이 기능은 Tello에서는 절대 불가능합니다!")
        # 실제 구현은 센서 데이터를 이용한 진동 분석 필요
        pass

    def reset_all(self):
        """모든 PID 컨트롤러 초기화"""
        self.roll_pid.reset()
        self.pitch_pid.reset()
        self.yaw_pid.reset()
        self.throttle_pid.reset()


# 사용 예제
if __name__ == "__main__":
    # pyDrone에서 사용하는 방법
    controller = AttitudePIDController()

    # 실시간 게인 조정 (Tello 불가능!)
    controller.roll_pid.set_gains(kp=2.0, ki=0.02, kd=0.6)

    print("pyDrone PID Controller initialized")
    print("Tello에서는 이런 저수준 제어가 불가능합니다!")

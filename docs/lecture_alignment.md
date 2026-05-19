# Lecture-Based Project Direction

이 프로젝트는 강의자료의 ROS/Gazebo 흐름을 기준으로 다음 단계로 확장한다.

## 지금 반영한 내용

### ROS_03_Gazebo(part2)

- Gazebo world 안에 공장 환경을 구성했다.
- `W1`, `W2`는 창고, `S1`, `S2`, `S3`는 조립 스테이션으로 모델링했다.
- 로봇 `R1`, `R2`를 Gazebo 모델로 배치했다.
- ROS2 노드가 Gazebo의 entity state를 갱신해서 로봇 위치를 시각화한다.
- 강의자료의 mobile robot 예시처럼 바퀴, caster, laser frame 형태가 보이는 로봇 모델로 변경했다.
- `/R1/cmd_vel`, `/R2/cmd_vel` 토픽을 발행해서 controller 계층의 명령을 확인할 수 있게 했다.

### ROS_02_Robot_Description

- `base_link`, wheel, caster, laser frame에 해당하는 시각 요소를 Gazebo 모델에 반영했다.
- 최종 Nav2 확장을 위해 `base_link -> laser_frame` 구조가 필요하다는 점을 설계 기준으로 둔다.

### ROS_08_Extra

- 프로젝트용 멀티로봇 예제로 구성했다.
- 두 로봇을 같은 world 안에서 동시에 제어한다.
- 이벤트 입력을 별도 ROS2 노드 `event_sender`로 분리했다.

### 7_Trajectory_Generation

- 로봇이 1초마다 순간이동하는 느낌을 줄이기 위해 0.1초 단위 보간을 추가했다.
- 시뮬레이션의 작업 진행은 1초 단위로 유지하고, Gazebo 표시 위치는 smooth time-scaling으로 갱신한다.
- 현재 구현은 발표용 시각화에 적합한 간단한 cubic smoothstep 방식이다.

## 다음에 붙일 내용

### ROS_04_Sensors

- 각 로봇에 LiDAR 또는 카메라 센서를 붙인다.
- `/scan` 같은 센서 토픽을 확인하고, 장애물 감지나 상태 출력에 연결한다.

### ROS_05_SLAM

- 공장 맵을 직접 모르는 설정으로 바꾸면 SLAM으로 map을 생성할 수 있다.
- 현재 프로젝트는 이미 좌표 기반 공장 맵이 있으므로 SLAM은 선택 확장으로 둔다.

### ROS_06_Nav2

- 최종 확장 방향은 스케줄러가 작업을 정하면 각 로봇에게 Nav2 goal을 보내는 구조다.
- 예: `R1`이 `T1`을 받으면 `W1`으로 이동한 뒤 `S1`로 이동한다.
- Nav2를 쓰려면 로봇별 namespace, map, localization, planner/controller 설정이 필요하다.

## 발표에서 설명할 구조

```text
Event Sender
    |
    v
Central Scheduler
    |
    v
Task Assignment / Reassignment
    |
    v
Gazebo Multi-Robot Visualization
```

핵심은 Gazebo 자체가 목표가 아니라, 생산 이벤트가 들어왔을 때 중앙 스케줄러가 작업을 다시 나누고 그 결과가 Gazebo에서 두 로봇의 움직임으로 보인다는 점이다.

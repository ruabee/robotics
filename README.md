# Smart Factory Multi-Robot Scheduling Simulation

ROS2 Humble 기반 스마트 팩토리 멀티로봇 작업 재할당 시뮬레이션입니다.

프로젝트 주제는 생산 시퀀스 변화, 부품 지연, 긴급 오더 삽입 같은 상황에서 중앙 스케줄러가 로봇 2대의 작업을 다시 배정하는 시스템입니다. 현재 버전은 Gazebo/Nav2 없이 먼저 검증할 수 있는 텍스트 기반 ROS2 시뮬레이션입니다.

## 구현 범위

- 로봇 2대: `R1`, `R2`
- 창고 2개: `W1`, `W2`
- 조립 스테이션 3개: `S1`, `S2`, `S3`
- 생산 작업: `V1`, `V2`, `V3`
- 이벤트 입력:
  - `1`: 생산 순서 변경, `V1 -> V2 -> V3`에서 `V1 -> V3 -> V2`
  - `2`: `V2` 부품 지연
  - `3`: 긴급 작업 `X` 삽입
  - `r`: 현재 상태 기준 재스케줄링
- 연속 생산:
  - `V1`, `V2`, `V3` 작업 batch가 끝나면 다음 batch가 자동으로 생성됨
  - 로봇은 작업이 끝나도 사라지지 않고 다음 생산 batch나 이벤트를 기다림
- 비용 기반 작업 할당:
  - 이동 거리
  - 납기 지연 패널티
  - 생산 순서 패널티
  - 긴급 작업 우선순위
- Gazebo 시각화:
  - 바퀴, caster, laser frame이 보이는 모바일 로봇 모델
  - 창고 선반, 팔레트, 컨베이어, 작업 스테이션, 안전 구역이 있는 공장 world
  - `/R1/cmd_vel`, `/R2/cmd_vel` 토픽으로 controller 계층의 명령 확인

강의자료 기반 진행 방향은 [docs/lecture_alignment.md](docs/lecture_alignment.md)에 정리했습니다.

## Ubuntu ROS2 Humble에서 실행

처음 한 번:

```bash
mkdir -p ~/robot_ws/src
cd ~/robot_ws/src
git clone <YOUR_REPOSITORY_URL>
```

이미 clone한 뒤 최신 코드를 받을 때:

```bash
cd ~/robot_ws/src/robotics
git pull
```

빌드:

```bash
cd ~/robot_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select smart_factory_mrs
source install/setup.bash
```

실행:

```bash
ros2 run smart_factory_mrs factory_sim
```

또는 launch 파일로 실행:

```bash
ros2 launch smart_factory_mrs factory_sim.launch.py
```

## Gazebo로 보기

Gazebo 패키지가 없다면 Ubuntu에서 먼저 설치합니다.

```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs
```

빌드 후 Gazebo 시뮬레이션을 실행합니다. 현재 저장소가 `/home/ruabee/Desktop/robotics`에 있다면 아래처럼 실행합니다.

```bash
cd /home/ruabee/Desktop/robotics
source /opt/ros/humble/setup.bash
colcon build --packages-select smart_factory_mrs
source install/setup.bash
ros2 launch smart_factory_mrs gazebo_factory_sim.launch.py
```

Gazebo 화면에서는 다음처럼 보면 됩니다.

- 파란 박스: 부품 창고 `W1`, `W2`
- 초록 박스: 조립 스테이션 `S1`, `S2`, `S3`
- 빨간 바퀴형 모바일 로봇: `R1`
- 노란 바퀴형 모바일 로봇: `R2`
- 갈색 구조물: 창고 선반
- 검은 긴 구조물: 컨베이어
- 노란 선: 로봇 이동 동선

로봇이 멈추는 것은 배정된 작업을 끝냈거나, 새 이벤트를 기다리는 상태입니다. 이벤트는 Gazebo를 켜둔 터미널이 아니라 새 터미널을 하나 더 열어서 넣습니다.

추천 방식:

```bash
source /opt/ros/humble/setup.bash
source /home/ruabee/Desktop/robotics/install/setup.bash
ros2 run smart_factory_mrs event_sender
```

그러면 아래처럼 입력창이 뜹니다.

```text
event>
```

여기에 `1`, `2`, `3`, `r` 중 하나를 입력하고 Enter를 누르면 Gazebo 시뮬레이션으로 이벤트가 전달됩니다.

직접 토픽으로 보낼 수도 있습니다.

```bash
source /opt/ros/humble/setup.bash
source /home/ruabee/Desktop/robotics/install/setup.bash
ros2 topic pub --once /factory_sim/event std_msgs/msg/String "{data: '1'}"
```

컨트롤러 계층에서 어떤 속도 명령이 나가는지 확인하려면 새 터미널에서 봅니다.

```bash
source /opt/ros/humble/setup.bash
source /home/ruabee/Desktop/robotics/install/setup.bash
ros2 topic echo /R1/cmd_vel
```

이벤트 번호는 텍스트 시뮬레이션과 같습니다.

```text
1: 생산 순서 변경
2: V2 부품 지연
3: 긴급 작업 삽입
r: 재스케줄링
```

실행 중 터미널에 숫자를 입력하고 Enter를 누르면 이벤트가 발생합니다.

```text
1 Enter: 생산 순서 변경
2 Enter: V2 부품 지연
3 Enter: 긴급 작업 삽입
r Enter: 재스케줄링
q Enter: 종료
```

상태 메시지는 ROS2 토픽으로도 발행됩니다.

```bash
ros2 topic echo /factory_sim/status
```

## Mac에서 가능한 확인

Mac에는 ROS2가 없어도 순수 Python 로직 테스트는 가능합니다.

```bash
python3 -m pytest tests
```

## 파일 구조

```text
smart_factory_mrs/
  factory_sim_node.py   # ROS2 노드, 키보드 입력, 토픽 출력
  simulation.py         # 시간 진행, 로봇 이동, 이벤트 적용
  scheduler.py          # 비용 기반 작업 할당/재할당
  models.py             # Robot, Task, Location 데이터 모델
  factory_map.py        # 창고/스테이션 좌표와 이동거리
  tasks.py              # 초기 작업과 긴급 작업 정의
launch/
  factory_sim.launch.py
tests/
  test_scheduler.py
```

## 에러가 나면 보내줄 것

Ubuntu에서 문제가 생기면 아래 결과를 그대로 복사해서 Codex에게 보내면 됩니다.

```bash
cd ~/robot_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select smart_factory_mrs
```

그리고 실행 에러:

```bash
source install/setup.bash
ros2 run smart_factory_mrs factory_sim
```

파일 구조 확인:

```bash
find ~/robot_ws/src/robotics -maxdepth 4 -type f
```

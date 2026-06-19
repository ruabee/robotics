# Smart Factory Multi-Robot Scheduling Simulation

## Team

**팀명:** Synaps

**팀원**

* 김채영
* 최준희

---

## Project Description

본 프로젝트는 **ROS2 Humble 기반 스마트 팩토리 멀티로봇 작업 재할당(Multi-Robot Scheduling) 시뮬레이션**입니다.

생산 공장에서는 생산 순서 변경, 부품 지연, 긴급 작업 삽입과 같은 이벤트가 빈번하게 발생합니다. 이러한 상황에서 중앙 스케줄러가 현재 수행 가능한 작업을 다시 선별하고, 이동 거리와 납기 지연, 생산 순서, 긴급 작업 우선순위를 고려한 비용 함수를 이용하여 두 대의 모바일 로봇(R1, R2)에 작업을 재할당하도록 구현하였습니다.

또한 Gazebo 환경에서 공장 레이아웃과 모바일 로봇을 시각화하고, ROS2 토픽을 통해 이동 명령(cmd_vel), LiDAR(scan), 목표 위치(goal_pose)를 확인할 수 있도록 구성하였습니다.

---

## Role Distribution

### 김채영

* ROS2 기반 시뮬레이션 환경 구축
* Gazebo 공장 환경 및 로봇 모델 구성
* ROS2 노드 및 이벤트 처리 구현
* Gazebo 시각화 및 테스트

### 최준희

* 중앙 스케줄러 설계
* 비용 기반 작업 할당 및 재스케줄링 알고리즘 구현
* 생산 이벤트(생산 순서 변경, 부품 지연, 긴급 작업, 장애물) 처리 로직 구현
* 테스트 및 README 작성

---

## AI Usage

본 프로젝트에서는 생성형 AI를 개발 보조 도구로 활용하였습니다.

사용 내용은 다음과 같습니다.

* ROS2 및 Gazebo 관련 코드 구조 개선
* Python 코드 리팩토링 및 디버깅
* README 문서 작성 보조
* 발표 자료 및 설명 문서 작성 보조

AI가 생성한 코드는 프로젝트 목적에 맞게 직접 수정 및 검증한 후 사용하였습니다.

---

## References

### ROS2

* ROS2 Humble Documentation
* Nav2 Documentation
* Gazebo Documentation

### GitHub

* ROS2 Examples
* Navigation2 (Nav2)
* TurtleBot3

### 기타

* ROS2 및 Gazebo 관련 공식 문서
* 강의자료

---

## YouTube

발표 영상

(YouTube 링크 입력)

---

## GitHub (Optional)

(GitHub Repository 링크 입력)

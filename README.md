# Smart Factory Multi-Robot Scheduling Simulation

## Team

**팀명:** Synapse

**팀원**

* 2271021 김채영
* 2376300 최준희

---

# Project Description

본 프로젝트는 **ROS2 Humble 기반 스마트 팩토리 멀티로봇 작업 재할당(Multi-Robot Scheduling) 시뮬레이션**이다.

스마트 팩토리에서는 생산 순서 변경, 부품 지연, 긴급 작업 삽입, 장애물 발생 등 다양한 이벤트가 발생하며, 이러한 변화에 따라 작업을 효율적으로 다시 배정하는 것이 중요하다.

본 시스템은 중앙 스케줄러(Central Scheduler)가 이벤트 발생 시 현재 수행 가능한 작업을 다시 선별하고, 이동 거리, 납기 지연, 생산 순서, 긴급 작업 우선순위 등의 비용을 계산하여 두 대의 모바일 로봇(R1, R2)에 작업을 재할당하도록 구현하였다.

또한 Gazebo 기반 공장 환경을 구축하여 창고, 조립 스테이션, 컨베이어, 장애물 및 모바일 로봇을 시각화하였으며, ROS2 Topic을 이용하여 `/cmd_vel`, `/scan`, `/goal_pose` 등을 확인할 수 있도록 구성하였다.

주요 기능은 다음과 같다.

* 생산 순서 변경(Event 1)
* 부품 지연(Event 2)
* 긴급 작업 삽입(Event 3)
* 장애물 발생 및 해제(Event o / c)
* 비용 기반 작업 재할당(Event r)
* 연속 생산 Batch 생성
* Gazebo 기반 시뮬레이션 및 ROS2 Topic 확인

---

# Role Distribution

| 팀원      | 담당 역할                                                                                             |
| ------- | ------------------------------------------------------------------------------------------------- |
| **김채영** | 작업 데이터 구조 설계, 중앙 스케줄러 구현, 비용 함수 설계, 생산 순서 변경 및 긴급 작업 재할당 알고리즘 구현                                  |
| **최준희** | Gazebo 공장 환경 구축, 모바일 로봇 이동 구현, 장애물 시각화, ROS2 Topic 구성 및 시스템 통합 |

시스템 통합과 테스트는 두 팀원이 함께 진행하였으며, 다양한 이벤트 시나리오에서 스케줄러의 작업 재할당 결과와 Gazebo 시뮬레이션의 로봇 동작이 일치하는지 검증하였다.

---

# AI Usage

본 프로젝트에서는 생성형 AI를 개발 보조 도구로 활용하였다.

### 사용 내용

* ROS2 및 Gazebo 코드 구조 개선
* Python 코드 리팩토링 및 디버깅
* ROS2 Launch 및 Package 설정 보조
* README 문서 작성 보조
* 발표 자료 및 발표 대본 작성 보조

AI가 제안한 코드와 문서는 프로젝트 목적에 맞게 직접 수정하고 테스트한 후 사용하였다.

---

# References

1. ROS2 Documentation
   https://docs.ros.org

2. Gazebo Documentation
   https://gazebosim.org/docs

3. Navigation2 (Nav2) Documentation
   https://docs.nav2.org

4. Intelligent Robotics 강의자료

   * ROS_03_Gazebo
   * ROS_04_Sensors
   * ROS_06_Nav2

---

# YouTube

발표 영상 (Unlisted)

**링크:** https://youtu.be/o_6xLYiB7CU?si=vmG8wPKyfZ4Fsa5u




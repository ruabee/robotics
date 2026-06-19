# 생산 시퀀스 변화에 대응하는 공장 내 멀티로봇 협업 시스템

## 팀명

**Synapse**

---

# 팀원

* 2271021 김채영
* 2376300 최준희

---

# 프로젝트 소개

본 프로젝트는 **ROS2 Humble 기반 스마트 팩토리 멀티로봇 작업 재할당(Multi-Robot Scheduling) 시스템**을 구현한 프로젝트입니다.

스마트 팩토리에서는 생산 순서 변경, 부품 준비 지연, 긴급 작업 삽입 등으로 인해 작업 환경이 지속적으로 변화합니다. 이러한 상황에서는 처음 계획한 작업 순서를 그대로 유지하기보다 현재 공장 상태를 반영하여 작업을 다시 배정하는 것이 중요합니다.

이를 위해 중앙 스케줄러(Central Scheduler)를 중심으로 작업 관리 시스템을 설계하였으며, 이벤트가 발생하면 현재 수행 가능한 작업을 다시 선별한 뒤 이동 거리, 작업량, 완료 지연, 생산 순서, 작업 우선순위 등을 고려한 비용 함수를 계산하여 가장 적합한 로봇에게 작업을 재할당하도록 구현하였습니다.

또한 Gazebo 기반 공장 환경을 구축하여 모바일 로봇, 창고, 작업 스테이션, 박스 등을 시각화하였으며, ROS2 Topic을 이용하여 로봇의 이동 명령, 센서 정보, 목표 위치 등을 확인할 수 있도록 구현하였습니다.

### 주요 기능

* 중앙 스케줄러 기반 작업 관리
* 비용 기반 멀티로봇 작업 할당 및 재스케줄링
* 생산 순서 변경 이벤트 처리
* 부품 지연 이벤트 처리
* 긴급 작업 삽입 및 작업 선점
* 연속 생산(Batch) 처리
* Gazebo 기반 공장 시뮬레이션
* ROS2 Topic 기반 로봇 상태 확인 및 제어
* Pickup / Drop 작업 시각화

---

# 역할 분담

### 김채영

* 중앙 스케줄러 설계 및 구현
* 작업(Task) 데이터 구조 설계
* 비용 함수 설계
* 작업 배정 및 재스케줄링 알고리즘 구현
* 생산 순서 변경, 부품 지연, 긴급 작업, 작업 선점 이벤트 처리

### 최준희

* Gazebo 공장 환경 구축
* Robot Node 및 Navigation 연동
* Pickup / Drop 작업 실행 로직 구현
* Visualization Node 구현
* ROS2 Topic 구성
* 로봇과 박스 상태 동기화 구현

### 공동 수행

* 전체 시스템 구조(System Architecture) 설계
* ROS2 노드 통합 및 기능 연동
* Gazebo 시뮬레이션 테스트 및 디버깅
* 다양한 이벤트 시나리오 검증
* 좌표계(Map, Gazebo, Nav2) 문제 해결
* 프로젝트 통합 테스트
* 최종 발표 자료(PPT) 제작
* 발표 대본 작성 및 발표 준비
* 시연(Demo) 구성
* README 및 프로젝트 문서 작성

---

# AI 사용 여부 및 사용 내용

본 프로젝트에서는 생성형 AI를 개발 보조 도구로 활용하였습니다.

### 사용한 AI

* ChatGPT
* Claude

### 활용 내용

* ROS2 및 Gazebo 관련 코드 구조 개선
* Python 코드 리팩토링 및 디버깅
* ROS2 Launch 및 Package 설정 보조
* 작업 재할당 알고리즘 구현 아이디어 검토
* README 문서 작성 보조
* 발표 자료(PPT) 구성 보조
* 발표 대본 작성 및 수정
* 프로젝트 문서 정리

AI가 생성한 코드와 문서는 프로젝트 목적에 맞게 팀원이 직접 수정하고 테스트한 후 최종 프로젝트에 적용하였습니다.

---

# 참고 자료

### 공식 문서

* ROS2 Documentation
  https://docs.ros.org

* Gazebo Documentation
  https://gazebosim.org/docs

* Navigation2 (Nav2) Documentation
  https://docs.nav2.org

---

### GitHub

* Navigation2 (Nav2)
* TurtleBot4
* ROS2 Examples

---

### 강의 자료

* Intelligent Robotics 강의자료

  * ROS_03_Gazebo
  * ROS_04_Sensors
  * ROS_06_Nav2

---

# YouTube

발표 영상

**링크:** https://youtu.be/o_6xLYiB7CU?si=vmG8wPKyfZ4Fsa5u




# Psychrochart for CNU [![Travis Status](https://travis-ci.org/azogue/psychrochart.svg?branch=master)](https://github.com/Hongildude/Psychrochart-for-CNU) 


안녕하세요 전남대학교 기계공학부 학생들을 위한 습공기선도 프로그램입니다. 다운로드 링크 :  **[Psychrometric charts for CNU](https://github.com/Hongildude/Psychrochart-for-CNU)** 

Psychrochart for CNU를 이용해주셔서 감사합니다.

Psychrochart for CNU는 전남대학교 기계공학부 2022년 3학년 2학기 캡스톤디자인1의 주제로 양홍일, 한현흠, 조선우가 제작을 하였습니다.

사용된 라이브러리 

(1) [`PsychroLib`](https://github.com/psychrometrics/psychrolib)

(2) `Matplotlib`

(3) `CoolProp`

(4) `Tkinter`

◈ 설치 및 사용상 궁금한 점이 있으시면 아래의 메일로 연락해주시기 바랍니다.

◈ 프로그램에서 오류가 발견되면 아래의 메일로 연락해주시기 바랍니다

`Email` : hongildude@gmail.com

## 0. 설치

```Bash
pip install Psychrolib
pip install Matplotlib
pip install Coolprop
```

## 1. 메뉴바

(1) 파일: 파일의 입출력을 위한 메뉴입니다

(2) 도구: 문자열 작성 및 작도 조건을 설정하는 옵션으로 구성되어있습니다.

(3) 도움말 : 본 프로그램의 정보 및 매뉴얼을 확인할 수 있습니다.

## 2. 도구 - 옵션

(1) 상단의 메뉴바에서 도구 - 옵션을 클릭합니다.

(2) 해발, 건구온도, 비습도

습공기선도의 작도 환경(해발, 건구온도, 절대습도)을 설정합니다.

해발은 0부터 4000m까지 입력 가능합니다.

건구온도는 -10도부터 50도까지 입력가능합니다.

비습도는 0부터 60g/kg dry air까지 입력가능합니다.

(3) 선도 표시 항목을 지정합니다.

나열된 항목 중에서 습공기선도에 표시하고자 하는 항목에 대해 클릭하여 체크를 합니다.

체크된 항목을 다시 한 번 체크하면 선택이 해제됩니다.

(4) 상태점 표시 항목을 선택합니다.

상태량 박스에 건구온도, 상대습도, 비습도, 엔탈피중 추가할 상태량을 선택합니다.

## 3. 습공기선도

(1) 상태량 계산 

상태량 계산을 위해 2개의 입력값이 필요합니다. 

체크박스를 클릭해 2개의 입력값을 받으면 자동으로 나머지 상태량들이 계산이 됩니다.

- 계산된 상태값은 소수점이하 절삭을 하여 오차가 발생할 수 있습니다.

(2) 상태점, 선 추가 

상태량 계산을 한 후 점을 추가할 수 있으며 점과 점을 잇는 선을 추가할 수 있습니다.

## 4. 인쇄

(1) 도구 - 인쇄 기능을 이용하여 .png파일로 저장할 수 있습니다.

- 저장된 파일은 .py이 있는곳에 자동으로 저장이 됩니다.

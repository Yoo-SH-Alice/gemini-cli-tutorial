# gemini-cli-tutorial

## Introduction
생성형 AI Gemini-CLI를 사용하여 여러가지 프로젝트를 생성하여 AI와 페어 프로그래밍을 통해 Python과 PyQt를 경험해 봅니다


## Environment
Pythoncn 3.13.3
PyQT5
Gemini-CLI



## Programs

### Notepad
```
todolist/
├── main.py             # 애플리케이션의 진입점
└── notepad_app.py     # PyQt UI 및 주요 로직
```

**메뉴바 구성**
- 메뉴 '파일','편집','보기'
- 파일에 하위 메뉴 : 새탭, 새창, 열기, 저장, 다른 이름으로 저장,모두 저장, 닫기
- 편집에 하위 메뉴 : 실행취소, 잘라내기, 복사, 붙여넣기, 삭제
- 보기에 하위 메뉴 : 확대,축소,자동줄바꿈


### Todolsit
```
todolist/
├── main.py             # 애플리케이션의 진입점
├── todo_app.py         # PyQt UI 및 주요 로직
└── data_manager.py     # 할 일 데이터 저장 및 로드 (JSON 파일 사용)
```

**주요 기능**
메인 윈도우: 애플리케이션의 기본 창.
할 일 입력 필드: 새로운 할 일을 입력하는 곳.
할 일 추가 버튼: 입력된 할 일을 목록에 추가.
할 일 목록: 현재 할 일들을 표시. 각 항목은 체크박스를 포함할 수 있습니다.
할 일 삭제 버튼: 비해선택된 할 일을 목록에서 제거.
레이아웃: 위젯들을 정렬하고 배치.
# gemini-cli-tutorial



## Introduction
생성형 AI Gemini-CLI를 사용하여 여러가지 프로젝트를 생성하여 AI와 페어 프로그래밍을 통해 Python과 PyQt를 경험해 봅니다


## Environment
- Pythoncn 3.13.3
- PyQT5
- Gemini-CLI



## Programs

### Notepad
**파일구조**

![Image](https://github.com/user-attachments/assets/b6bc1731-d0f0-4761-adf7-90f385d8ef52)


```
notepad/
├── main.py             # 애플리케이션의 진입점
└── notepad_app.py     # PyQt UI 및 주요 로직
```


**주요 기능**
- 메뉴 구성 '파일','편집','보기'
- 파일 : 새탭, 새창, 열기, 저장, 다른 이름으로 저장,모두 저장, 닫기
- 편집 : 실행취소, 잘라내기, 복사, 붙여넣기, 삭제
- 보기 : 확대,축소,자동줄바꿈


### Todolsit


![Image](https://github.com/user-attachments/assets/1444de4f-5ab1-42c3-a0d0-2e12fc4e536e)


**파일구조**
```
todolist/
├── main.py             # 애플리케이션의 진입점
├── todo_app.py         # UI 및 주요 로직
├── data_manager.py     # 할 일 데이터 저장 및 로드 (JSON 파일 사용)
└──todos.json           # 할 일 데이터 파일
```

**주요 기능**
- 새로운 할 일 입력: 새로운 할 일의 내용과 시작,끝 시간을 입력.  
- 할 일 추가 버튼: 클릭 시 입력된 할 일을 목록에 추가.  
- 할 일 목록 표시: 체크박스로 현재 할 일들을 표시.  
- 할 일 삭제 버튼: 선택된 할 일을 목록에서 제거.




### Image Gallery


![Image](https://github.com/user-attachments/assets/a295e07d-c366-425e-967c-535a4feda6cf)


**파일구조**
```
gallery/
└── main.py             # 주요로직
```
**주요 기능**


### YOLO Object Detection


![Image](https://github.com/user-attachments/assets/e43a5dd9-8bdf-464e-93cd-7904ac33c4f9)


**파일구조**
```
object_detection_app.py # UI 및 주요로직
```

- 이미지 파일 선택 후 화면에 로드
- 로드된 이미지를 


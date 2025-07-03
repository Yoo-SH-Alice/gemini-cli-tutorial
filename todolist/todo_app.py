from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime
from data_manager import load_todos, save_todos

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List App")
        self.setGeometry(100, 100, 550, 400)

        self.todos = [] # Internal list to store todo data
        self.selected_todo_index = -1 # -1 means no item is selected for editing
        self.init_ui()
        self.load_initial_todos()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Input and Add/Update Button
        input_layout = QVBoxLayout()

        # Todo Text Input
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Add a new todo...")
        input_layout.addWidget(self.todo_input)

        # Date/Time Inputs
        datetime_layout = QHBoxLayout()
        self.start_datetime_input = QDateTimeEdit(self)
        self.start_datetime_input.setCalendarPopup(True)
        self.start_datetime_input.setDateTime(QDateTime.currentDateTime())
        self.start_datetime_input.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.end_datetime_input = QDateTimeEdit(self)
        self.end_datetime_input.setCalendarPopup(True)
        self.end_datetime_input.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.end_datetime_input.setDisplayFormat("yyyy-MM-dd HH:mm")

        datetime_layout.addWidget(self.start_datetime_input)
        datetime_layout.addWidget(self.end_datetime_input)
        input_layout.addLayout(datetime_layout)

        # Add/Update Button
        self.add_update_button = QPushButton("Add Todo")
        self.add_update_button.clicked.connect(self.add_or_update_todo)
        input_layout.addWidget(self.add_update_button)

        # Todo List
        self.todo_list_widget = QListWidget()
        self.todo_list_widget.itemChanged.connect(self.toggle_todo_state)
        self.todo_list_widget.itemClicked.connect(self.on_todo_item_clicked)

        # Delete Button
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_todo)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.todo_list_widget)
        main_layout.addWidget(self.delete_button)

        self.setLayout(main_layout)

    def load_initial_todos(self):
        self.todos = load_todos()
        for todo in self.todos:
            self._add_todo_item_to_list_widget(todo)

    def _add_todo_item_to_list_widget(self, todo_data):
        start_dt_str = todo_data.get('start_datetime')
        end_dt_str = todo_data.get('end_datetime')

        formatted_start_datetime = 'N/A'
        if start_dt_str:
            start_dt = QDateTime.fromString(start_dt_str, Qt.ISODate)
            if start_dt.isValid():
                formatted_start_datetime = start_dt.toString("yyyy-MM-dd HH:mm")

        formatted_end_datetime = 'N/A'
        if end_dt_str:
            end_dt = QDateTime.fromString(end_dt_str, Qt.ISODate)
            if end_dt.isValid():
                formatted_end_datetime = end_dt.toString("yyyy-MM-dd HH:mm")

        item_text = f"{todo_data['text']} (시작: {formatted_start_datetime}, 끝: {formatted_end_datetime})"
        item = QListWidgetItem(item_text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked if todo_data['completed'] else Qt.Unchecked)
        if todo_data['completed']:
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
        self.todo_list_widget.addItem(item)

    def add_or_update_todo(self):
        todo_text = self.todo_input.text().strip()
        if not todo_text:
            return

        start_dt_obj = self.start_datetime_input.dateTime()
        end_dt_obj = self.end_datetime_input.dateTime()

        start_dt_str = start_dt_obj.toString(Qt.ISODate)
        end_dt_str = end_dt_obj.toString(Qt.ISODate)

        if self.selected_todo_index != -1:
            # Update existing todo
            self.todos[self.selected_todo_index]['text'] = todo_text
            self.todos[self.selected_todo_index]['start_datetime'] = start_dt_str
            self.todos[self.selected_todo_index]['end_datetime'] = end_dt_str
            
            # Update the QListWidgetItem text
            item = self.todo_list_widget.item(self.selected_todo_index)
            formatted_start_datetime = start_dt_obj.toString("yyyy-MM-dd HH:mm")
            formatted_end_datetime = end_dt_obj.toString("yyyy-MM-dd HH:mm")
            item_text = f"{todo_text} (시작: {formatted_start_datetime}, 끝: {formatted_end_datetime})"
            item.setText(item_text)

            self.selected_todo_index = -1 # Deselect after update
            self.add_update_button.setText("Add Todo")
        else:
            # Add new todo
            new_todo = {
                'text': todo_text,
                'completed': False,
                'start_datetime': start_dt_str,
                'end_datetime': end_dt_str
            }
            self.todos.append(new_todo)
            self._add_todo_item_to_list_widget(new_todo)

        self.todo_input.clear()
        self.start_datetime_input.setDateTime(QDateTime.currentDateTime())
        self.end_datetime_input.setDateTime(QDateTime.currentDateTime().addDays(1))
        save_todos(self.todos)

    def delete_todo(self):
        selected_rows = sorted([item.row() for item in self.todo_list_widget.selectedItems()], reverse=True)
        if not selected_rows:
            return
        
        for row in selected_rows:
            self.todo_list_widget.takeItem(row)
            del self.todos[row]
            
        save_todos(self.todos)
        self.selected_todo_index = -1 # Deselect if deleted
        self.add_update_button.setText("Add Todo")
        self.todo_input.clear()
        self.start_datetime_input.setDateTime(QDateTime.currentDateTime())
        self.end_datetime_input.setDateTime(QDateTime.currentDateTime().addDays(1))

    def toggle_todo_state(self, item):
        # Disconnect to prevent recursive calls during text update
        self.todo_list_widget.itemChanged.disconnect(self.toggle_todo_state)

        row = self.todo_list_widget.row(item)
        if 0 <= row < len(self.todos):
            is_completed = item.checkState() == Qt.Checked
            self.todos[row]['completed'] = is_completed
            
            font = item.font()
            font.setStrikeOut(is_completed)
            item.setFont(font)
            
            # Update the displayed text to reflect completion status if needed
            # (already handled by font strike-out, but good to keep in mind for more complex displays)

            save_todos(self.todos)
        
        # Reconnect after changes
        self.todo_list_widget.itemChanged.connect(self.toggle_todo_state)

    def on_todo_item_clicked(self, item):
        self.selected_todo_index = self.todo_list_widget.row(item)
        selected_todo_data = self.todos[self.selected_todo_index]

        self.todo_input.setText(selected_todo_data['text'])
        self.start_datetime_input.setDateTime(QDateTime.fromString(selected_todo_data.get('start_datetime', QDateTime.currentDateTime().toString(Qt.ISODate)), Qt.ISODate))
        self.end_datetime_input.setDateTime(QDateTime.fromString(selected_todo_data.get('end_datetime', QDateTime.currentDateTime().addDays(1).toString(Qt.ISODate)), Qt.ISODate))
        self.add_update_button.setText("Update Todo")

    def closeEvent(self, event):
        save_todos(self.todos)
        event.accept()

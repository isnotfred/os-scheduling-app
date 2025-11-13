import sys
from scheduling.process import Process
from scheduling.algorithms import highest_response_ratio_next, preemptive_priority, calculate_averages
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidget,
    QTableWidgetItem, QLineEdit, QPushButton, QLabel, QScrollArea, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SchedulingTab(QWidget):
    def __init__(self, scheduling_algo, with_priority=False):
        super().__init__()
        self.processes = []
        self.pid = 0
        self.scheduling_algo = scheduling_algo
        self.with_priority = with_priority

        self.tab_layout = QHBoxLayout()
        self.input_section = QVBoxLayout()
        self.output_section = QVBoxLayout()
        
        form_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        # Input field styling
        input_field_style = """
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """

        if self.with_priority:
            self.at_input_field = QLineEdit()
            self.at_input_field.setPlaceholderText("Enter arrival time")
            self.at_input_field.setStyleSheet(input_field_style)
            
            self.bt_input_field = QLineEdit()
            self.bt_input_field.setPlaceholderText("Enter burst time")
            self.bt_input_field.setStyleSheet(input_field_style)
            
            self.priority_input_field = QLineEdit()
            self.priority_input_field.setPlaceholderText("Enter priority")
            self.priority_input_field.setStyleSheet(input_field_style)
        else:
            self.at_input_field = QLineEdit()
            self.at_input_field.setPlaceholderText("Enter arrival time")
            self.at_input_field.setStyleSheet(input_field_style)
            
            self.bt_input_field = QLineEdit()
            self.bt_input_field.setPlaceholderText("Enter burst time")
            self.bt_input_field.setStyleSheet(input_field_style)

        submit_button = QPushButton("Add Process")
        if self.with_priority:
            submit_button.setFixedSize(90, self.at_input_field.sizeHint().height() * 3 + 15)
        else:
            submit_button.setFixedSize(90, self.at_input_field.sizeHint().height() * 2 + 10)
        submit_button.clicked.connect(self.add_item)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

        input_layout.addWidget(self.at_input_field)
        input_layout.addWidget(self.bt_input_field)
        if self.with_priority:
            input_layout.addWidget(self.priority_input_field)
        form_layout.addLayout(input_layout)
        form_layout.addWidget(submit_button)

        # Table styling
        table_style = """
            QTableWidget {
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
        """

        if self.with_priority:
            self.input_table_widget = QTableWidget()
            self.input_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
            self.input_table_widget.setColumnCount(4)
            self.input_table_widget.setHorizontalHeaderLabels(["Process", "Arrival Time", "Burst Time", "Priority Level"])
            self.input_table_widget.horizontalHeader().setStretchLastSection(True)
            self.input_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.input_table_widget.setStyleSheet(table_style)
        else:
            self.input_table_widget = QTableWidget()
            self.input_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
            self.input_table_widget.setColumnCount(3)
            self.input_table_widget.setHorizontalHeaderLabels(["Process", "Arrival Time", "Burst Time"])
            self.input_table_widget.horizontalHeader().setStretchLastSection(True)
            self.input_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.input_table_widget.setStyleSheet(table_style)
        
        clear_input_button = QPushButton("Clear")
        clear_input_button.setFixedHeight(40)
        clear_input_button.clicked.connect(self.clear_all)
        clear_input_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c41408;
            }
        """)
        
        schedule_button = QPushButton("Schedule")
        schedule_button.setFixedHeight(40)
        schedule_button.clicked.connect(self.schedule_input)
        schedule_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6ebd;
            }
        """)

        buttons_layout.addWidget(clear_input_button)
        buttons_layout.addWidget(schedule_button)

        self.input_section.addLayout(form_layout)
        self.input_section.addWidget(self.input_table_widget)
        self.input_section.addLayout(buttons_layout)

        self.processes_label = QLabel()
        self.processes_label.setStyleSheet("""
            QLabel {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
                color: #333;
                background-color: #e3f2fd;
                padding: 5px;
            }
        """)
        
        self.times_label = QLabel()
        self.times_label.setStyleSheet("""
            QLabel {
                font-family: 'Courier New', monospace;
                font-size: 13px;
                color: #333;
                background-color: #f5f5f5;
                padding: 5px;
            }
        """)
        
        gantt_chart_widget = QWidget()
        gantt_chart_layout = QVBoxLayout(gantt_chart_widget)
        gantt_chart_layout.addWidget(self.processes_label)
        gantt_chart_layout.addWidget(self.times_label)

        scroll_area = QScrollArea()
        scroll_area.setFixedHeight(100)
        scroll_area.setWidget(gantt_chart_widget)       
        scroll_area.setWidgetResizable(True)            
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
        """)

        self.output_table_widget = QTableWidget()
        self.output_table_widget.setFixedHeight(590)
        self.output_table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.output_table_widget.setColumnCount(8)
        self.output_table_widget.setHorizontalHeaderLabels(["PID", "AT", "BT", "ST", "CT", "TAT", "WT", "RT"])
        self.output_table_widget.horizontalHeader().setStretchLastSection(True)
        self.output_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.output_table_widget.setStyleSheet(table_style)

        self.averages_label = QLabel()
        self.averages_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                background-color: #fff3e0;
                padding: 10px;
                border: 2px solid #ff9800;
                border-radius: 5px;
            }
        """)

        self.output_section.addWidget(scroll_area)
        self.output_section.addWidget(self.output_table_widget)
        self.output_section.addWidget(self.averages_label)

        self.tab_layout.addLayout(self.input_section, 4)
        self.tab_layout.addLayout(self.output_section, 8)
        self.setLayout(self.tab_layout)

    def add_item(self):
        try: 
            arrival_time = int(self.at_input_field.text().strip())
            burst_time = int(self.bt_input_field.text().strip())
            if self.with_priority:
                priority_level = int(self.priority_input_field.text().strip())
        except ValueError:
            self.at_input_field.clear()
            self.bt_input_field.clear()
            if self.with_priority:
                self.priority_input_field.clear()
            return
        
        self.pid += 1
        row_position = self.input_table_widget.rowCount()
        self.input_table_widget.insertRow(row_position)
        self.input_table_widget.setItem(row_position, 0, QTableWidgetItem(f"P{self.pid}"))
        self.input_table_widget.setItem(row_position, 1, QTableWidgetItem(f"{arrival_time}"))
        self.input_table_widget.setItem(row_position, 2, QTableWidgetItem(f"{burst_time}"))
        if self.with_priority:
            self.input_table_widget.setItem(row_position, 3, QTableWidgetItem(f"{priority_level}"))
            self.processes.append(Process(self.pid, arrival_time, burst_time, priority_level))
        else:
            self.processes.append(Process(self.pid, arrival_time, burst_time))
        self.at_input_field.clear()
        self.bt_input_field.clear()
        if self.with_priority:
            self.priority_input_field.clear()

    def clear_all(self):
        self.input_table_widget.setRowCount(0)
        self.processes.clear()
        self.pid = 0
        self.output_table_widget.setRowCount(0)
        self.processes_label.clear()
        self.times_label.clear()
        self.averages_label.clear()

    def schedule_input(self):
        if not self.processes:
            return
        
        gantt_chart = self.scheduling_algo(self.processes, len(self.processes))
        averages = calculate_averages(self.processes, len(self.processes))

        processes_id_str = ""
        times_str = ""
        for time, process_id in gantt_chart:
            if process_id is not None:
                processes_id_str += f"{process_id:^10}"
            times_str += f"{time:<10}"

        self.processes_label.setText(processes_id_str)
        self.times_label.setText(times_str)

        for process in self.processes:
            row_position = self.output_table_widget.rowCount()
            self.output_table_widget.insertRow(row_position)
            self.output_table_widget.setItem(row_position, 0, QTableWidgetItem(f"P{process.pid}"))
            self.output_table_widget.setItem(row_position, 1, QTableWidgetItem(f"{process.arrival_time}"))
            self.output_table_widget.setItem(row_position, 2, QTableWidgetItem(f"{process.burst_time}"))
            self.output_table_widget.setItem(row_position, 3, QTableWidgetItem(f"{process.starting_time}"))
            self.output_table_widget.setItem(row_position, 4, QTableWidgetItem(f"{process.completion_time}"))
            self.output_table_widget.setItem(row_position, 5, QTableWidgetItem(f"{process.turnaround_time}"))
            self.output_table_widget.setItem(row_position, 6, QTableWidgetItem(f"{process.waiting_time}"))
            self.output_table_widget.setItem(row_position, 7, QTableWidgetItem(f"{process.response_time}"))

        self.averages_label.setText(f"TAT: {round(averages["turnaround_time_avg"], 2):<10.2f}"
                                    f"WT: {round(averages["waiting_time_avg"], 2):<10.2f}"
                                    f"RT: {round(averages["response_time_avg"], 2):<10.2f}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1560, 850)
        self.setWindowTitle("Scheduling Algorithms")
        
        # Main window styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
            }
        """)

        self.tabs = QTabWidget()
        
        # Tab widget styling
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #cccccc;
                border-radius: 5px;
                background-color: #f5f5f5;
                top: -2px;
            }
            
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333333;
                padding: 12px 25px;
                margin-right: 2px;
                border: 2px solid #cccccc;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
                border-color: #4CAF50;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #d0d0d0;
            }
        """)
        
        self.tabs.addTab(SchedulingTab(highest_response_ratio_next), "HRRN")
        self.tabs.addTab(SchedulingTab(preemptive_priority, with_priority=True), "Preemptive Priority")
    
        self.setCentralWidget(self.tabs)

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
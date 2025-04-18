from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
import sys
from memory_manager import MemoryManager
from visualization import visualize_memory
import threading

class MemoryTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = MemoryManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Real-Time Memory Tracker")
        self.setGeometry(100, 100, 700, 500)
        
        layout = QVBoxLayout()

        self.status_label = QLabel("🖥 Memory Status: Ready", self)
        layout.addWidget(self.status_label)

        self.input_process = QLineEdit(self)
        self.input_process.setPlaceholderText("Enter Process ID")
        layout.addWidget(self.input_process)

        self.input_pages = QLineEdit(self)
        self.input_pages.setPlaceholderText("Enter Number of Pages")
        layout.addWidget(self.input_pages)

        self.btn_allocate = QPushButton("Allocate Memory", self)
        self.btn_allocate.clicked.connect(self.allocate_memory)
        layout.addWidget(self.btn_allocate)

        self.btn_deallocate = QPushButton("Deallocate Memory", self)
        self.btn_deallocate.clicked.connect(self.deallocate_memory)
        layout.addWidget(self.btn_deallocate)

        self.btn_visualize = QPushButton("Show Memory Visualization", self)
        self.btn_visualize.clicked.connect(self.show_visualization)
        layout.addWidget(self.btn_visualize)

        self.memory_table = QTableWidget()
        self.memory_table.setColumnCount(2)
        self.memory_table.setHorizontalHeaderLabels(["Process ID", "Allocated Pages"])
        layout.addWidget(self.memory_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_notification(self, message, title="Notification"):
        """Displays a pop-up message."""
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def update_memory_display(self):
        """Updates the table with current memory allocation."""
        self.memory_table.setRowCount(len(self.manager.processes))
        for i, (pid, pages) in enumerate(self.manager.processes.items()):
            self.memory_table.setItem(i, 0, QTableWidgetItem(str(pid)))
            self.memory_table.setItem(i, 1, QTableWidgetItem(str(len(pages))))

    def allocate_memory(self):
        """Handles memory allocation and notifies the user."""
        process_id = self.input_process.text().strip()
        num_pages = self.input_pages.text().strip()
        
        if not process_id or not num_pages.isdigit():
            self.show_notification("⚠ Please enter valid Process ID and Page Number!", "Error")
            return
        
        message = self.manager.allocate_memory(process_id, int(num_pages))
        self.status_label.setText(f"🖥 {message}")
        self.show_notification(message)
        self.update_memory_display()

    def deallocate_memory(self):
        """Handles memory deallocation and notifies the user."""
        process_id = self.input_process.text().strip()
        if not process_id:
            self.show_notification("⚠ Please enter a valid Process ID!", "Error")
            return
        
        message = self.manager.deallocate_memory(process_id)
        self.status_label.setText(f"🖥 {message}")
        self.show_notification(message)
        self.update_memory_display()
        
    def show_visualization(self):
        """Opens the memory visualization directly on the main thread."""
        self.show_notification("📊 Opening Memory Visualization...")
        visualize_memory(self.manager)  # Direct call (no threading)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemoryTrackerApp()
    window.show()
    sys.exit(app.exec_())

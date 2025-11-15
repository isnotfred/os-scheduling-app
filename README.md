# Scheduling Algorithms GUI

A PyQt5-based graphical user interface application for visualizing CPU scheduling algorithms including Highest Response Ratio Next (HRRN) and Preemptive Priority scheduling.

## Features

* **HRRN (Highest Response Ratio Next)** - Non-preemptive scheduling algorithm
* **Preemptive Priority Scheduling** - Priority-based preemptive algorithm
* Visual Gantt chart representation
* Detailed process metrics (Turnaround Time, Waiting Time, Response Time)
* Modern, styled UI with intuitive controls

## Prerequisites

Before running this application, ensure you have the following installed:

* Python 3.7 or higher
* pip (Python package installer)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/isnotfred/os-scheduling-app.git
cd os-scheduling-app
```

### 2. Install Required Dependencies

`requirements.txt` is already provided so you can install all dependencies at once:

```bash
pip install -r requirements.txt
```

### 3. Project Structure

Ensure your project has the following structure:

```
os-scheduling-app/
│
├── main.py                 # Main GUI application file
├── scheduling/
│   ├── __init__.py
│   ├── process.py          # Process class definition
│   └── algorithms.py       # Scheduling algorithms implementation
├── requirements.txt        # Project dependencies
└── README.md
```

## Running the Application

### Option 1: Run directly with Python

```bash
python main.py
```

### Option 2: Make it executable (Linux/Mac)

```bash
chmod +x main.py
./main.py
```

### Option 3: Run as a module

```bash
python -m main
```

## How to Use

1. **Enter Process Details:** Arrival Time, Burst Time, Priority Level (if any)
2. **Add Process:** Click the "Add Process" button
3. **Schedule:** Click "Schedule" to run the selected algorithm and view results
4. **View Results:** Gantt Chart, Output Table, and average metrics (TAT, WT, RT)
5. **Clear:** Remove all processes and reset

## Output Metrics Explained

* **PID:** Process ID
* **AT:** Arrival Time
* **BT:** Burst Time
* **ST:** Start Time (first time the process gets CPU)
* **CT:** Completion Time
* **TAT:** Turnaround Time (CT - AT)
* **WT:** Waiting Time (TAT - BT)
* **RT:** Response Time (ST - AT)

## Troubleshooting

### PyQt5 Installation Issues

**Windows:**

```bash
pip install PyQt5 --user
```

**Linux:**

```bash
sudo apt-get install python3-pyqt5
```

**Mac:**

```bash
brew install pyqt5
pip install PyQt5
```

### Module Not Found Error

If you get a "Module not found" error for `scheduling`:

1. Ensure the `scheduling` folder exists with `__init__.py`
2. Run the script from the correct directory
3. Check that `process.py` and `algorithms.py` are in the `scheduling` folder

### Display Issues

If the GUI doesn't display correctly:

* Ensure you have a compatible display/desktop environment
* On Linux, try running with a different Qt platform plugin:

```bash
export QT_QPA_PLATFORM=xcb
python main.py
```

## Dependencies

* **PyQt5** - GUI framework
* **Python Standard Library** - sys module

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

MIT License

## Author

Frederick Orlain

## Version

1.0.0

---

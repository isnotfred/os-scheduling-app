# Scheduling Algorithms GUI

A comprehensive PyQt5-based graphical user interface application for visualizing and comparing CPU scheduling algorithms.

## Features

### Supported Scheduling Algorithms

#### Non-Preemptive Algorithms
* **FCFS (First Come First Serve)** - Processes are executed in order of arrival time
* **SJF (Shortest Job First)** - Processes with shortest burst time are executed first
* **Non-Preemptive Priority** - Processes with highest priority (lowest priority number) are executed first
* **HRRN (Highest Response Ratio Next)** - Balances between short jobs and long-waiting jobs using response ratio

#### Preemptive Algorithms
* **SRTF (Shortest Remaining Time First)** - Preemptive version of SJF, switches to process with shortest remaining time
* **Preemptive Priority** - Switches to higher priority process when it arrives
* **Round Robin (RR)** - Each process gets a fixed time quantum in circular order

### Application Features
* Interactive visual Gantt chart representation
* Detailed process metrics table (AT, BT, ST, CT, TAT, WT, RT)
* Average performance metrics calculation
* Configurable time quantum for Round Robin
* Modern, styled UI with intuitive controls
* Color-coded process visualization
* Real-time process addition and management

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

Alternatively, install PyQt5 directly:

```bash
pip install PyQt5
```

### 3. Project Structure

Ensure your project has the following structure:

```
os-scheduling-app/
│
├── main.py                 # Main GUI application file
├── scheduling/
│   ├── __init__.py        # Package initializer
│   ├── process.py         # Process class definition
│   └── algorithms.py      # All 7 scheduling algorithms
├── requirements.txt       # Project dependencies
└── README.md             # This file
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

### Basic Workflow

1. **Select Algorithm:** Choose from the tab menu (FCFS, SJF, Priority, HRRN, SRTF, Preemptive Priority, or Round Robin)
2. **Enter Process Details:**
   - **Arrival Time:** When the process arrives in the ready queue
   - **Burst Time:** CPU time required by the process
   - **Priority:** Priority level (lower number = higher priority)
   - **Time Quantum:** For Round Robin only (e.g., 2, 4)
3. **Add Process:** Click "Add Process" to add the process to the queue
4. **Schedule:** Click "Schedule" button to execute the algorithm
5. **View Results:**
   - Gantt Chart shows process execution timeline
   - Output Table displays detailed metrics for each process
   - Average metrics (TAT, WT, RT) shown at the bottom
6. **Clear:** Click "Clear" to remove all processes and start over

### Input Validation

- Arrival Time: Must be non-negative integer
- Burst Time: Must be positive integer
- Priority: Required for Priority-based algorithms (lower number = higher priority)
- Time Quantum: Required for Round Robin (must be positive integer)

## Output Metrics Explained

* **PID** - Process ID (automatically assigned)
* **AT** - Arrival Time (when process enters ready queue)
* **BT** - Burst Time (total CPU time required)
* **Priority** - Priority level (if applicable)
* **ST** - Start Time (first time the process gets CPU)
* **CT** - Completion Time (when process finishes execution)
* **TAT** - Turnaround Time (CT - AT) - total time from arrival to completion
* **WT** - Waiting Time (TAT - BT) - time spent waiting in ready queue
* **RT** - Response Time (ST - AT) - time from arrival to first CPU allocation

### Performance Metrics

The application calculates and displays:
- **Average Turnaround Time (Avg TAT)**
- **Average Waiting Time (Avg WT)**
- **Average Response Time (Avg RT)**

These metrics help compare the efficiency of different scheduling algorithms.

## Algorithm Details

### Tie-Breaking Rules

When multiple processes have the same priority/burst time/arrival time:

1. **FCFS:** Earlier arrival time, then lower PID
2. **SJF:** Shorter burst time, then earlier arrival time, then lower PID
3. **Priority (Non-Preemptive):** Higher priority, then earlier arrival time, then shorter burst time, then lower PID
4. **HRRN:** Higher response ratio, then earlier arrival time, then shorter burst time, then lower PID
5. **SRTF:** Shorter remaining time, then earlier arrival time, then lower PID
6. **Preemptive Priority:** Higher priority, then earlier arrival time, then shorter burst time, then lower PID
7. **Round Robin:** Order of arrival in ready queue

## Example Usage

### Example 1: FCFS Scheduling

```
Process 1: AT=0, BT=4
Process 2: AT=1, BT=3
Process 3: AT=2, BT=1
```

Result: P1 → P2 → P3

### Example 2: Round Robin (Time Quantum = 2)

```
Process 1: AT=0, BT=5
Process 2: AT=1, BT=3
Process 3: AT=2, BT=1
```

Result: P1(2) → P2(2) → P3(1) → P1(2) → P2(1) → P1(1)

## Troubleshooting

### PyQt5 Installation Issues

**Windows:**
```bash
pip install PyQt5 --user
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-pyqt5
```

**Linux (Fedora):**
```bash
sudo dnf install python3-qt5
```

**Mac:**
```bash
brew install pyqt5
pip install PyQt5
```

### Module Not Found Error

If you get a "Module not found" error for `scheduling`:

1. Ensure the `scheduling` folder exists with `__init__.py`
2. Run the script from the project root directory
3. Verify `process.py` and `algorithms.py` are in the `scheduling` folder
4. Check Python path: `export PYTHONPATH="${PYTHONPATH}:${PWD}"`

### Display Issues

If the GUI doesn't display correctly:

**Linux:**
```bash
export QT_QPA_PLATFORM=xcb
python main.py
```

**Wayland users:**
```bash
export QT_QPA_PLATFORM=wayland
python main.py
```

**Missing display:**
```bash
export DISPLAY=:0
python main.py
```

### Permission Denied

**Linux/Mac:**
```bash
chmod +x main.py
```

## Dependencies

* **PyQt5** (>=5.15.0) - GUI framework
* **Python Standard Library**
  - sys - System-specific parameters
  - copy - Deep copy functionality for process objects

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Frederick Orlain**
- GitHub: [@isnotfred](https://github.com/isnotfred)

## Acknowledgments

- Built with PyQt5 framework
- Inspired by operating systems course materials
- CPU scheduling algorithms based on standard OS textbooks

## Version

* **1.1.0**
  - Completed all 7 scheduling algorithms
  - Improved error handling and tie-breaking conditions

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: fredorlain5@gmail.com

---
# Operating System Multi-Subsystem Scheduler

A comprehensive multi-subsystem task scheduler implementing different scheduling algorithms with resource management.

## System Architecture

The project consists of four main subsystems:
1. Weighted Round Robin (3 processors)
2. Shortest Remaining Time First (2 processors) 
3. Rate Monotonic for real-time tasks (1 processor)
4. Dependency-based scheduling (2 processors)

### Directory Structure
```
OS__final_prj/
├── Main_system/
│   ├── main_subsystem.py     # Core system coordinator
│   └── get_input.py         # Input handler
├── SubSystems/
│   ├── subsystem1/          # Weighted Round Robin
│   ├── subsystem2/          # SRTF
│   ├── subsystem3/          # Rate Monotonic
│   └── subsystem4/          # Dependency-based
├── Reports/
│   └── execution_tracker.py # Performance monitoring
├── app.py                   # Entry point
└── readme.md
```

## Installation

1. Ensure Python 3.7+ is installed
2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd OS__final_prj
   ```

## Input Format

The program expects input in the following format:

```
[subsystem1_r1] [subsystem1_r2]     # Resource units for subsystem 1
[subsystem2_r1] [subsystem2_r2]     # Resource units for subsystem 2
[subsystem3_r1] [subsystem3_r2]     # Resource units for subsystem 3
[subsystem4_r1] [subsystem4_r2]     # Resource units for subsystem 4
# Subsystem 1 Tasks (WRR)
[name] [execution_time] [r1_usage] [r2_usage] [arrival_time] [processor_number]
$
# Subsystem 2 Tasks (SRTF)
[name] [execution_time] [r1_usage] [r2_usage] [arrival_time]
$
# Subsystem 3 Tasks (RM)
[name] [execution_time] [r1_usage] [r2_usage] [arrival_time] [period] [repetitions]
$
# Subsystem 4 Tasks (Dependency)
[name] [execution_time] [r1_usage] [r2_usage] [arrival_time] [prerequisite_task]
$
```

## Running the Program

1. Execute the main program:
   ```bash
   python app.py
   ```

2. Enter the input as per the format above. Example:
   ```
   2 2
   2 2
   2 2
   2 2
   T1 4 1 1 0 1
   T2 3 1 1 2 2
   $
   T3 5 1 1 0
   T4 4 1 1 1
   $
   T5 3 1 1 0 5 2
   T6 2 1 1 1 4 3
   $
   T7 4 1 1 0 -
   T8 3 1 1 2 T7
   $
   ```

## Implementation Details

### 1. Resource Management
- Each subsystem has dedicated R1 and R2 resources
- Thread-safe resource allocation using locks
- Resource tracking and deadlock prevention
- Dynamic resource reallocation for real-time tasks

### 2. Scheduling Algorithms

#### Subsystem 1 (WRR)
- Three processors with weighted round-robin
- Dynamic quantum calculation
- Load balancing among processors
- Priority-based task distribution

#### Subsystem 2 (SRTF)
- Two processors with preemptive SRTF
- Remaining time tracking
- Dynamic task preemption
- Resource-aware scheduling

#### Subsystem 3 (RM)
- Single processor for real-time tasks
- Period and deadline management
- Admission control
- Resource speedup capability

#### Subsystem 4 (Dependency)
- Two processors with dependency resolution
- Prerequisite task tracking
- Dynamic task ordering
- Resource-aware execution

### 3. Monitoring and Reporting

The system generates a detailed execution report (execution_report.json) containing:
- Task completion times
- Resource utilization
- Waiting times
- Core allocation details
- System performance metrics

## Performance Optimization

1. Resource Utilization
   - Dynamic resource reallocation
   - Efficient lock management
   - Smart task distribution

2. Scheduling Efficiency
   - Load balancing
   - Priority adjustment
   - Deadline management

## Support

For additional support or questions:
1. Check the execution report
2. Review system logs

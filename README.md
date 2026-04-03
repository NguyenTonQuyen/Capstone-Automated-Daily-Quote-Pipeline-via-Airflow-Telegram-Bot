**1. High-Level Architecture:**

- Layer 1 (Infrastructure): Docker Compose (Orchestrating containers including Airflow Webserver, Scheduler, and Worker).
- Layer 2 (Orchestration): Apache Airflow (Managed within Docker; responsible for scheduling, monitoring, and error handling).
- Layer 3 (Logic): Python Script (welcome_dag_v2.py) (Defining the Directed Acyclic Graph (DAG), task dependencies, and API integration logic).

**2. Data Pipeline Processing:**

**Step 1: Trigger (Initialization):**
- Event: Scheduled at 23:00 (Asia/Ho_Chi_Minh) daily or initiated via Manual Trigger (UI Play button).
- Component: Airflow Scheduler parses the DAG file and instantiates a DagRun.

**Step 2: Task 1 - print_welcome:**
- Action: Executes a Python function to verify the environment.
- Output: Logs "Welcome to Airflow!" to the Task Instance logs.

**Step 3: Task 3 - print_date:**
- Action: Retrieves system time using the datetime library.
- Output: Logs the current date (YYYY-MM-DD).

**Step 4: Task 3 - print_random_quote (Data Collection)**
- Action: Sends an asynchronous GET request to the ZenQuotes API.
- Logic: Validates HTTP Status (200 OK) => Parses JSON response => Extracts quote and author.
- Output: Pushes the formatted string to XComs (Airflow's internal cross-communication storage).

**Step 5: Task 4 - send_to_telegram (Integration)**
**Action: **
    1.  Pull: Retrieves the Quote string from XComs.
    2.  Authenticate: Uses the encrypted Bot Token and Chat ID.
    3.  Transmit: Sends a POST request to the Telegram Bot API.

**Endpoint: api.telegram.org/bot<token>/sendMessage.**

**Step 6: Finish (Completion)**
- Result: The user receives a push notification on the Telegram mobile/desktop app.
- Status: Task is marked as Success (Green) in the Airflow Grid/Graph View.

<div align="center">

# CampusCore — College Management System

**A relational academic administration system featuring student admissions, faculty allocations, course offerings, fee ledger tracking, and an interactive SQL query inspection engine.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26.svg?logo=html5&logoColor=white)](https://html.spec.whatwg.org/)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6.svg?logo=css3&logoColor=white)](https://www.w3.org/Style/CSS/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E.svg?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### 🔗 Live: [college-management-system-nc5t.onrender.com](https://college-management-system-nc5t.onrender.com/)

</div>

---

## What it is

CampusCore is a full-stack college management and database administration platform built to replace cluttered academic portals with a high-performance, single-screen workspace. It combines day-to-day administrative operations (admissions, faculty allocation, timetable scheduling, tuition fee ledgering) with a live database engine that allows administrators and educators to inspect table schemas, execute pre-compiled relational SQL queries with sub-millisecond execution telemetry, and manage institutional records with strict relational integrity.

---

## Features

**Student Admissions & Records** — Register students with validated registration numbers, contact information, date of birth, semester tracking, and departmental assignments. Includes live status monitoring across Active, Graduated, Suspended, and Withdrawn states.

**Faculty & Department Administration** — Manage institutional schools and departments alongside annual operating budgets and building assignments. Maintain faculty profiles with designations, salary ledgers, hire dates, and direct department associations.

**Curriculum & Course Scheduling** — Structure academic offerings by course code, title, credits, and level. Schedule term offerings across designated classrooms with real-time seat capacity tracking, preventing over-enrollment.

**Tuition Fee Ledger & Dues Lookup** — Record fee transactions across multiple payment channels (UPI, Net Banking, Credit/Debit Card, Demand Draft). An instant dues lookup engine computes paid versus outstanding balances per student in real time.

**Academic Audit & Performance** — Compute cumulative GPAs, record course examination results, and review automated academic standing classifications including Dean's List and First Class honors.

**Live SQL Query Engine & Schema Explorer** — Explore all relational tables, schema column specifications, foreign key mappings, and primary keys. Execute 16 categorized SQL queries covering multi-table INNER JOINs, GROUP BY aggregations, HAVING filters, correlated subqueries, and set operations with execution timers.

---

## Stack

| Layer | Tech |
|---|---|
| Frontend | Semantic HTML5, Vanilla JavaScript (ES6+), Custom Design System (CSS3) |
| Backend | Python 3, Flask, Werkzeug, Gunicorn |
| Database | SQLite3 (ACID-compliant, Foreign Key Enforcement, Strict Checks) |
| Typography | Plus Jakarta Sans, Outfit, JetBrains Mono |
| Deployment | Render |

---

## Project structure

```text
College-Management-System/
├── application/
│   ├── templates/
│   │   └── index.html       # Single-screen dashboard UI
│   ├── app.py               # CLI administration interface
│   ├── db_manager.py        # SQLite connection, DDL/DML, stored logic
│   ├── demo_runner.py       # End-to-end transaction test suite
│   ├── query_runner.py      # Pre-compiled SQL queries with ASCII tables
│   └── server.py            # Flask REST API server and route handlers
├── database/
│   ├── 01_create_tables.sql # Relational schema DDL with constraints
│   ├── 02_insert_data.sql   # Seed records
│   ├── 03_queries.sql       # Complex analytical SQL queries
│   ├── 04_procedures.sql    # Transaction procedures
│   ├── 05_functions.sql     # Database functions
│   ├── 06_cursor.sql        # Cursor logic
│   ├── 07_triggers.sql      # Integrity triggers
│   ├── 08_demo_transactions.sql # Sample transaction sequence
│   └── college_cms.db       # Active SQLite database file
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

---

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/stats` | Fetch institution summary metrics (students, faculty, courses, departments) |
| `GET` | `/api/meta` | Retrieve all entity collections for dropdowns and directory views |
| `GET` | `/api/tables/<table_name>` | Fetch all rows and column headers from a specific table |
| `POST` | `/api/students/add` | Register a new student into a department |
| `POST` | `/api/faculty/add` | Appoint a new faculty member with designation and salary |
| `POST` | `/api/courses/add` | Add a new course to the curriculum |
| `POST` | `/api/departments/add` | Create an academic department with allocated budget |
| `POST` | `/api/offerings/add` | Schedule a course offering section in a classroom with capacity |
| `POST` | `/api/enroll` | Enroll a student in an offering (capacity and prerequisite checks) |
| `POST` | `/api/exam/record` | Record examination score and automatically compute letter grade |
| `POST` | `/api/fees/pay` | Record a tuition fee payment transaction |
| `GET` | `/api/students/<student_id>/gpa_fees` | Compute GPA, credits earned, total paid fees, and pending dues |
| `GET` | `/api/cursor/audit` | Run academic performance audit cursor and GPA distribution |
| `GET` | `/api/queries` | List all 16 pre-compiled SQL analytical queries |
| `GET` | `/api/queries/<query_id>` | Execute a specific pre-compiled SQL query with live telemetry |
| `POST` | `/api/execute_raw_sql` | Execute a custom SELECT query from the query console |
| `GET` | `/api/telemetry` | Stream live backend transaction telemetry and execution timings |
| `POST` | `/api/reset_db` | Reset and re-seed the SQLite database to factory state |

---

<div align="center">
<sub>Built by <a href="https://github.com/ahlawatansh">Ansh Ahlawat</a> · CSE undergrad, VIT Vellore</sub>
</div>

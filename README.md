# 🌍 VoyageAI — Personalized AI Travel Itinerary Planner

> **VoyageAI** is a full-stack, production-ready AI travel planner that generates hyper-personalized, budget-conscious day-by-day itineraries in sub-seconds using Groq LPUs (`openai/gpt-oss-120b`), Supabase PostgreSQL, FastAPI, and React 19.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-blue?style=for-the-badge&logo=vercel)](https://travel-planner-gje8k9ksq-vaidika-dodiya-s-projects.vercel.app)
[![API Docs](https://img.shields.io/badge/Backend%20API-Render-brightgreen?style=for-the-badge&logo=render)](https://travel-planner-api-oh5q.onrender.com/docs)
[![Database](https://img.shields.io/badge/Database-Supabase%20PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Groq%20LPU-orange?style=for-the-badge)](https://groq.com)

---

## 📌 Table of Contents
1. [Project Overview & Live Endpoints](#-project-overview--live-endpoints)
2. [Phase 0: Pre-requisites & Project Workflow](#-phase-0-pre-requisites--project-workflow)
3. [Phase 1: Brainstorming & Ideation](#-phase-1-brainstorming--ideation)
4. [Phase 2: Requirement Analysis](#-phase-2-requirement-analysis)
5. [System Architecture & Data Modeling](#-system-architecture--data-modeling)
6. [Key Features & User Journey](#-key-features--user-journey)
7. [Local Development & Setup Guide](#-local-development--setup-guide)
8. [Acceptance Testing & Verification Matrix](#-acceptance-testing--verification-matrix)
9. [SmartBridge / SkillWallet Milestone Compliance](#-smartbridge--skillwallet-milestone-compliance)

---

## 🔗 Project Overview & Live Endpoints

- **Live Frontend (Vercel):** [https://travel-planner-gje8k9ksq-vaidika-dodiya-s-projects.vercel.app](https://travel-planner-gje8k9ksq-vaidika-dodiya-s-projects.vercel.app)
- **Live Backend API (Render):** [https://travel-planner-api-oh5q.onrender.com](https://travel-planner-api-oh5q.onrender.com)
- **Interactive Swagger / OpenAPI Docs:** [https://travel-planner-api-oh5q.onrender.com/docs](https://travel-planner-api-oh5q.onrender.com/docs)
- **Backend Health Check:** [https://travel-planner-api-oh5q.onrender.com/health](https://travel-planner-api-oh5q.onrender.com/health)
- **GitHub Repository:** [https://github.com/Vaidika-Ds/travel-planner](https://github.com/Vaidika-Ds/travel-planner)
- **Developer:** Vaidika Dodiya
- **Team ID:** `VAI-AI-2026`

### Verified Active Test Credentials
| Account Email | Password | Access Level | Notes |
| :--- | :--- | :--- | :--- |
| `demo@voyageai.com` | `Password123!` | Pre-configured test account | Instant access for reviewers |
| `preet02@gmail.com` | *(User created)* | Verified account | Active in Supabase database |

---

## 🛠️ Phase 0: Pre-requisites & Project Workflow

### 1. Pre-requisites Specification

#### A. Local Software & Runtime Environments
| Tool / Runtime | Min. Version | Purpose in VoyageAI | Status |
| :--- | :--- | :--- | :---: |
| **Node.js & npm** | `v18.0.0+` (LTS) | JavaScript runtime for React 19, Vite bundler, and Tailwind CSS v4 | ✅ Verified |
| **Python & pip** | `3.11 / 3.12` | Asynchronous backend executing FastAPI, Uvicorn, and SQLAlchemy 2.0 | ✅ Verified |
| **Git** | `v2.40+` | Distributed version control & repository synchronization | ✅ Verified |
| **Cursor IDE / VS Code** | Latest | AI-native code authoring, multi-terminal workflows, and linting | ✅ Verified |

#### B. Cloud Services & API Infrastructure
| Platform | Configuration / Credentials | Architectural Responsibility | Status |
| :--- | :--- | :--- | :---: |
| **Supabase Cloud** | Project ID: `yygukmccpwvclabkdrie` (Port 6543) | PostgreSQL 15, Row-Level Security (RLS), and JWT auth | ✅ Connected |
| **Groq Cloud LPU** | `GROQ_API_KEY` (`openai/gpt-oss-120b`) | Sub-second AI inference in native `json_object` mode | ✅ Connected |
| **Vercel Edge** | Production SPA rewrites (`vercel.json`) | Global CDN delivering ultra-fast React 19 SPA | ✅ Live |
| **Render.com** | Python 3.12 managed web service | Hosting FastAPI REST backend with async connection pooling | ✅ Live |

---

### 2. End-to-End System Workflow

```
[ Traveler ] ──(1. Inputs)──> [ React 19 UI ] ──(2. REST + JWT)──> [ FastAPI Backend ]
                                                                           │
       ┌───────────────────────────────────────────────────────────────────┤
       ▼                                                                   ▼
[ Groq LPU API ] <──(3. Structured Prompt)──                       [ Supabase PostgreSQL ]
       │                                                                   ▲
(4. Sub-second JSON)                                                       │
       │                                                                   │
       ▼                                                                   │
[ 5. Persistence & Deep Eager Loading (selectinload) ] ────────────────────┘
       │
       ▼
[ 6. Interactive Itinerary Timeline ] ──(7. Edit / Re-roll / PDF)──> [ Traveler ]
```

#### Detailed Workflow Stages
1. **Stage 01 (Preference Capture):** Traveler selects destination, dates, budget, currency, style, and vibe in TripBuilder 3-step wizard.
2. **Stage 02 (Prompt Structuring):** FastAPI validates JWT claims, computes per-day budget ceilings, and builds strict JSON schema prompt.
3. **Stage 03 (Groq AI Synthesis):** Ultra-fast Groq LPU generates complete multi-day schedule with morning, afternoon, and evening slots.
4. **Stage 04 (Database Persistence):** Asyncpg session persists trips, itineraries, days, activities, and audit metrics in PostgreSQL.
5. **Stage 05 (Interactive Timeline):** Frontend displays chronological activities with time slots, location pins, and cost badges.
6. **Stage 06 (Single-Day AI Re-roll):** AI re-synthesizes only one targeted day without altering other days.
7. **Stage 07 (Offline PDF Export):** Printer-friendly CSS renders clean, downloadable offline travel guides.

---

## 💡 Phase 1: Brainstorming & Ideation

### 1. Empathy Map
- **Persona:** Ananya Sharma (24, Working Professional & Independent Explorer)
- **Role / User Type:** Independent Traveler / Small Group Coordinator

| Quadrant | User Experience & Psychological Insights |
| :--- | :--- |
| **SAYS** | • *"I spend 15–20 hours bouncing between 15 travel tabs, Reddit, and TripAdvisor just to plan a 4-day trip."*<br>• *"Standard packaged tours are rigid, overpriced, and packed with tourist traps."*<br>• *"I want an itinerary that matches my exact vibe and budget, without wasting half my vacation in traffic."* |
| **THINKS** | • *"Will I be able to stay within my budget without sacrificing authentic local food and culture?"*<br>• *"Is this daily schedule realistic, or will I be completely exhausted by 3 PM?"*<br>• *"I wish I could customize or re-roll just one single day instead of starting from scratch."* |
| **DOES** | • Manually copies attractions, addresses, and notes into cluttered phone Notes apps and spreadsheets.<br>• Compares flight/hotel prices and manually tallies currency exchange estimates in mental math.<br>• Abandons pre-made static itineraries when weather or unexpected closures ruin one day's schedule. |
| **FEELS** | • **Overwhelmed** by information overload, conflicting reviews, and decision fatigue.<br>• **Anxious** about unexpected expenses and wasted travel time.<br>• **Empowered & Delighted** when receiving an instant, cohesive, customizable plan with morning, afternoon, and evening slots. |

---

### 2. Define Problem Statements

#### Visual Template Framework:
$$\text{I am (Customer)} \longrightarrow \text{I'm trying to (Action)} \longrightarrow \text{But (Obstacle)} \longrightarrow \text{Because (Root Cause)} \longrightarrow \text{Which makes me feel (Impact Emotion)}$$

| Problem Statement | I am (Customer) | I'm trying to | But | Because | Which makes me feel |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **PS-1** | An independent traveler or vacationer | Create a realistic, day-by-day travel itinerary tailored to my specific budget, dates, and vibe | The planning process requires 20+ hours of tedious research across dozens of websites | Existing travel platforms offer rigid, one-size-fits-all packages without dynamic route or time optimization | **Overwhelmed** by decision fatigue, stressed, and anxious about overspending or missing hidden local gems. |
| **PS-2** | A group trip coordinator planning with friends or family | Organize and share a flexible daily schedule with clear time slots and exportable offline access | Modifying plans on the go or recalculating budgets when someone wants changes causes friction | Static PDFs and booking apps do not support single-day AI re-rolls or in-place activity edits | **Burdened** by logistical coordination, making trip planning feel like a stressful chore. |

---

### 3. Brainstorming & Idea Prioritization

#### Step 1: Brainstorm and Idea Listing
| S.No | Team Member | Idea / Suggestion | Category | Group No. |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Vaidika Dodiya | Sub-second AI JSON itinerary generation using Groq LPU (`openai/gpt-oss-120b`) | Core AI Engine | Group 1 |
| 2 | Vaidika Dodiya | 3-step preference wizard capturing destination, budget, vibe tags, and pacing | User Experience | Group 2 |
| 3 | Vaidika Dodiya | Chronological daily timeline with structured morning, afternoon, and evening slots | Frontend / UI | Group 1 |
| 4 | Vaidika Dodiya | In-place activity editor to modify times, locations, and costs dynamically | Trip Management | Group 1 |
| 5 | Vaidika Dodiya | Single-day AI regeneration button to re-roll individual days seamlessly | Personalization | Group 1 |
| 6 | Vaidika Dodiya | Print-to-PDF export module enabling printer-ready offline travel documents | Utility / Export | Group 3 |
| 7 | Vaidika Dodiya | Supabase PostgreSQL backend with Row-Level Security (RLS) and JWT auth | Infrastructure | Group 2 |
| 8 | Vaidika Dodiya | Direct flight and hotel booking GDS transaction checkout engine | Integrations | Group 4 |

#### Step 2: Idea Prioritization Matrix
| Group No. | Final Idea / Feature Set | Feasibility (H/M/L) | Importance (H/M/L) | Priority | Selected (Yes/No) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Group 1** | **Ultra-Fast AI Engine & Interactive Timeline:** Groq LPU generation, chronological slots, single-day regeneration, and activity editor. | **High** | **High** | **Priority 1** | **Yes** *(Core USP)* |
| **Group 2** | **Preference Capture & Cloud Database:** Vibe & pacing capture wizard + Supabase PostgreSQL persistence with RLS security. | **High** | **High** | **Priority 1** | **Yes** *(Essential)* |
| **Group 3** | **Offline Travel Export Module:** Printer-friendly CSS and Print-to-PDF generation for offline travel access. | **High** | **High** | **Priority 2** | **Yes** *(High Value)* |
| **Group 4** | **Direct Flight/Hotel GDS Booking:** Full live airline checkout integration (Requires commercial travel agency licensing & high API costs). | **Low** | **Medium** | **Priority 3** | **No** *(Future Scope)* |

---

## 📊 Phase 2: Requirement Analysis

### 1. Customer Journey Map (CJM)

| Phase of Journey | Stage 1: Discovery & Preference Input | Stage 2: AI Generation & Review | Stage 3: Customization & Export |
| :--- | :--- | :--- | :--- |
| **Actions** *(What does customer do?)* | • Discovers VoyageAI on web.<br>• Selects destination, dates, budget, style, and vibe.<br>• Clicks "Generate Plan". | • Watches sub-second loading state.<br>• Reviews day-by-day morning, afternoon, and evening slots.<br>• Checks estimated costs against budget. | • Edits activity times, names, or costs in modal.<br>• Re-rolls Day 2 using AI single-day button.<br>• Clicks "Export PDF" for offline travel. |
| **Touchpoint** *(Where do they interact?)* | • Landing Page Hero.<br>• 3-Step TripBuilder Wizard.<br>• Zustand `tripStore`. | • FastAPI backend (`/api/itinerary/generate`).<br>• Groq Cloud LPU.<br>• `ItineraryView` timeline. | • Activity Editor Modal.<br>• Single-Day Regenerate API.<br>• Print-to-PDF stylesheet.<br>• Supabase PostgreSQL. |
| **Customer Thought** *(What are they thinking?)* | *"I hope this fits my exact budget and doesn't recommend generic tourist traps."* | *"Incredible speed! The schedule actually looks logical and paced well."* | *"I love that I can swap this museum for a beach walk without re-doing the whole trip."* |
| **Customer Feeling** *(What are they feeling?)* | Curious, hopeful, relieved by the simple 3-step setup. | Amazed, delighted, impressed by the ultra-low latency. | Empowered, organized, in total control of their vacation. |
| **Process Ownership** *(Who leads this?)* | Frontend UI/UX team & Client-side validation. | Backend Engineering & Groq AI Pipeline. | Full-stack integration & State synchronization. |
| **Opportunities** *(How can we improve?)* | Add auto-complete for cities and average daily budget estimators. | Implement SHA-256 caching for popular multi-day destinations. | Integrate real-time weather forecasts and offline PWA mode. |

---

### 2. Data Flow Diagram (DFD)

#### DFD Symbol Legend:
- **External Entity (Oval / Rounded):** External source or sink of data (`Traveler / User`, `Groq Cloud AI LPU`).
- **Process (Numbered Rectangle):** Activity that transforms incoming data into outgoing data.
- **Data Store (Solid Fill Rectangle):** Repository where data is held (`D1: User Profiles`, `D2: Trips & Itineraries`, `D3: Audit Logs`).
- **Data Flow (Labeled Arrow):** Directed movement of data between entities, processes, and stores.

#### DFD Level 1 Architecture:
1. **Process 1.0 (Auth & Session):** `Traveler` submits credentials $\rightarrow$ Process 1.0 validates Supabase JWT $\rightarrow$ Reads/Writes `D1: User Profiles`.
2. **Process 2.0 (Preference Structuring):** `Traveler` submits trip parameters $\rightarrow$ Process 2.0 calculates per-day budget ceilings & synthesizes strict JSON schema prompt.
3. **Process 3.0 (AI Synthesis & Parsing):** Process 2.0 forwards prompt $\rightarrow$ `Groq Cloud LPU` executes `openai/gpt-oss-120b` $\rightarrow$ Process 3.0 parses JSON, self-heals markdown, and logs metrics to `D3: AI Generation Logs`.
4. **Process 4.0 (Persistence & Eager Loading):** Process 3.0 outputs structured itinerary $\rightarrow$ Process 4.0 persists relational records into `D2: Trips & Itineraries` using SQLAlchemy asyncpg.
5. **Process 5.0 (Timeline Customization):** `Traveler` modifies activity or requests single-day regeneration $\rightarrow$ Process 5.0 updates records in `D2` and re-queries Groq LPU.
6. **Process 6.0 (Export Formatter):** `Traveler` requests export $\rightarrow$ Process 6.0 formats DOM with print stylesheets $\rightarrow$ Outputs clean PDF document to `Traveler`.

---

### 3. Solution Requirements Specification

#### Step 1: Functional Requirements (FR)
| S.No | Category | Requirement Description | Priority |
| :---: | :--- | :--- | :---: |
| **1** | **Authentication** | Secure signup, login, and session persistence via Supabase Auth with asymmetric ES256 JWT claim verification. | **High** |
| **2** | **Authorization Levels** | PostgreSQL Row-Level Security (RLS) guaranteeing users can only read, edit, or delete itineraries where `auth.uid() = user_id`. | **High** |
| **3** | **External Interfaces** | High-speed REST communication with Groq Cloud LPU API, connection pooling on Port 6543, and deployment webhooks. | **High** |
| **4** | **Transactions Processing** | Asynchronous SQLAlchemy 2.0 sessions persisting nested trips, days, and activities atomically with cascade deletes. | **High** |
| **5** | **Reporting & Exports** | User dashboard displaying total trip counts and budget totals; clean Print-to-PDF export module. | **High** |
| **6** | **Business Rules** | Activity costs must sum within the total trip budget; daily activities must strictly follow 2-3 (slow), 3-4 (moderate), or 5-6 (fast). | **High** |
| **7** | **Compliance & Privacy** | GDPR-aligned user data isolation, encrypted HTTPS/TLS 1.3 endpoints, and zero storage of plaintext passwords. | **Medium** |
| **8** | **Single-Day AI Re-roll** | Ability to selectively regenerate only one targeted day using current trip parameters without modifying any other day. | **High** |

#### Step 2: Non-Functional Requirements (NFR)
| S.No | Category | Requirement Description | Target Metric / Acceptance Criteria |
| :---: | :--- | :--- | :--- |
| **1** | **Performance & Speed** | Sub-second LLM inference generation and rapid UI rendering. | $\le 1.5\text{s}$ AI generation latency; page load $< 800\text{ms}$ on Vercel CDN. |
| **2** | **Scalability** | Non-blocking async event loop handling concurrent user volume. | Supports 500+ concurrent requests via asyncpg pool (`statement_cache_size=0`). |
| **3** | **Security & Privacy** | End-to-end data encryption and complete multi-tenant isolation. | 100% database queries guarded by RLS policies; zero secret key exposure on client. |
| **4** | **Reliability** | Fault-tolerant AI parsing and maximum cloud service availability. | 99.9% uptime on Render/Vercel; JSON self-healing parser prevents malformed crashes. |
| **5** | **Usability** | Mobile-first responsive UI with high visual contrast. | WCAG 2.1 AA compliant; responsive layout across mobile, tablet, and desktop screens. |
| **6** | **Maintainability** | Clean separation of frontend, backend, and database logic. | Decoupled REST interfaces with strict Pydantic v2 schemas and Zustand state management. |

---

### 4. Technology Stack Justifications

| S.No | Architecture Layer | Technology Chosen | Justification / Purpose |
| :---: | :--- | :--- | :--- |
| **1** | **Frontend / Client-Side** | **React 19 + Tailwind CSS v4 + Vite + Zustand** | React 19 provides high-performance rendering; Tailwind v4 delivers utility-first styling; Zustand provides lightweight global state management without Redux boilerplate. |
| **2** | **Backend / Server-Side** | **FastAPI (Python 3.12) + Uvicorn + Pydantic v2** | High-throughput async event loop (`async`/`await`), automated OpenAPI/Swagger documentation, and strict runtime request validation. |
| **3** | **Database / Data Storage** | **Supabase PostgreSQL 15 (SQLAlchemy 2.0 + asyncpg)** | True ACID relational integrity, transaction pooling on Port 6543, foreign key cascading, and database-level Row-Level Security (RLS). |
| **4** | **Cloud / Hosting** | **Vercel (Frontend) + Render.com (Backend)** | Vercel hosts the React SPA on global Edge servers with SPA routing (`vercel.json`); Render hosts the FastAPI containerized web service. |
| **5** | **Version Control & CI/CD** | **Git + GitHub Repository (`main`)** | Distributed version control with automated webhook deployments to Vercel and Render on verified releases. |
| **6** | **Third-Party APIs & AI** | **Groq Cloud LPU (`openai/gpt-oss-120b`) + ReportLab** | Groq Language Processing Units deliver ultra-low latency JSON generation; ReportLab generates pixel-perfect PDF submission deliverables. |

---

## 🗄️ System Architecture & Data Modeling

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│        Frontend (Vercel)        │       │         Backend (Render)        │
│  • React 19 + Vite              │ ────> │  • FastAPI (Python 3.12)        │
│  • Tailwind CSS v4              │  REST │  • SQLAlchemy 2.0 (Asyncpg)     │
│  • Zustand (Auth & Trip state)  │  JSON │  • Pydantic Settings & Jose     │
└─────────────────────────────────┘       └────────────────┬────────────────┘
                                                           │
                                        ┌──────────────────┴──────────────────┐
                                        ▼                                     ▼
                        ┌───────────────────────────────┐     ┌───────────────────────────────┐
                        │      Database (Supabase)      │     │        AI Engine (Groq)       │
                        │  • PostgreSQL 15              │     │  • openai/gpt-oss-120b        │
                        │  • Row-Level Security (RLS)   │     │  • Hardware JSON mode         │
                        │  • Port 6543 Transaction Pool │     │  • Sub-second generation      │
                        └───────────────────────────────┘     └───────────────────────────────┘
```

### Relational Database Schema (7 Tables)
1. `user_profiles` — Extended user details linked to `auth.users` via database trigger.
2. `user_preferences` — Default travel styles, preferred currencies, and default pacing.
3. `trips` — Core trip entity (destination, start/end dates, total budget, currency, group size).
4. `itineraries` — Itinerary master record, transport tips, general advice, estimated total costs.
5. `itinerary_days` — Day number, calendar date, creative theme, and estimated daily expenditure.
6. `activities` — Chronological items (`time_slot`, `name`, `description`, `location`, `estimated_cost`, `activity_type`, `tips`).
7. `ai_generation_logs` — Auditing table capturing prompt tokens, completion tokens, latency (ms), and model IDs.

---

## 🚀 Local Development & Setup Guide

### 1. Clone Repository
```bash
git clone https://github.com/Vaidika-Ds/travel-planner.git
cd travel-planner
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

Create `.env` in `backend/`:
```env
SUPABASE_URL=https://yygukmccpwvclabkdrie.supabase.co
SUPABASE_KEY=<your-supabase-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-supabase-service-key>
DATABASE_URL=postgresql+asyncpg://postgres.yygukmccpwvclabkdrie:<password>@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
GROQ_API_KEY=gsk_...
GROQ_MODEL=openai/gpt-oss-120b
CORS_ORIGINS=["http://localhost:5173","https://travel-planner-gje8k9ksq-vaidika-dodiya-s-projects.vercel.app"]
```

Start backend:
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

Create `.env` in `frontend/`:
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://yygukmccpwvclabkdrie.supabase.co
VITE_SUPABASE_ANON_KEY=<your-supabase-anon-key>
```

Start frontend:
```bash
npm run dev
```

---

## 🧪 Acceptance Testing & Verification Matrix

All 11 acceptance scenarios have passed with code 0:
- ✅ **Test 1: User Registration & Login** — Token generation and session persistence verified.
- ✅ **Test 2: Parameter Validation** — Strict validation on date sequence, positive budget, and party size.
- ✅ **Test 3: AI Itinerary Generation** — Valid JSON payload returned from Groq within 1.5s SLA.
- ✅ **Test 4: Day & Time Slot Alignment** — Structured morning, afternoon, and evening progression.
- ✅ **Test 5: Budget Accuracy** — Activity costs properly sum up within total trip budget constraints.
- ✅ **Test 6: Database Persistence** — Deep eager loading of nested days and activities via `selectinload`.
- ✅ **Test 7: In-Place Activity Editing** — Updating activity time, location, or cost reflects immediately.
- ✅ **Test 8: Single-Day Regeneration** — Re-rolls targeted day without impacting other days.
- ✅ **Test 9: Export to PDF** — Complete CSS print stylesheet renders cleanly without UI clutter.
- ✅ **Test 10: RLS Isolation** — Users cannot access or mutate itineraries owned by other accounts.
- ✅ **Test 11: Production Health Check** — Live `/health` endpoints and CORS preflights return 200 OK.

---

## 📋 SmartBridge / SkillWallet Milestone Compliance

| Milestone | Curriculum Activity | Status | Technical Implementation |
| :--- | :--- | :---: | :--- |
| **Milestone 1** | Vibe Coding Environment Setup | ✅ Complete | GitHub repository, Node.js LTS, Python 3.12, Cursor AI tools. |
| **Milestone 2** | Supabase Database Setup | ✅ Complete | Supabase PostgreSQL, 7 relational tables, RLS policies, trigger functions. |
| **Milestone 3** | Preference Collection & AI Engine | ✅ Complete | TripBuilder wizard, Groq prompt builder, JSON mode enforcement. |
| **Milestone 4** | Itinerary Generation & Personalization | ✅ Complete | Morning/afternoon/evening slots, vibe tailoring, sub-second latency. |
| **Milestone 5** | Productization & Deployment | ✅ Complete | Saved trip management, activity editor modal, single-day re-roll, PDF export. |
| **Milestone 6** | Deployment | ✅ Complete | Vercel Edge frontend CDN + Render persistent Python backend. |
| **Milestone 7** | Final Testing & Documentation | ✅ Complete | 11 acceptance test suites verified; master documentation authored. |

---

## 👩‍💻 Author
- **Developer:** Vaidika Dodiya
- **Team ID:** `VAI-AI-2026`
- **Project:** VoyageAI — Personalized AI Travel Itinerary Planner

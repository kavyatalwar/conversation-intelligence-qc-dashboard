# 🎙️ Conversational Intelligence Platform
### *Leveraging 7 QC Frameworks for Advanced Automated Quality Assurance Audits*

📥 **Live Cloud Application:** [conversation-intelligence-qc-dashboard.streamlit.app](https://conversation-intelligence-qc-dashboard.streamlit.app/)

---

## 📑 Project Genesis & Overview

In operational management, receiving targeted feedback about system performance or analytical gaps is a critical driver for engineering iterations. This project was born out of a challenge to turn classical text processing capabilities—such as isolated sentiment metrics—into a full-scale, interactive, and production-grade software application. 

Instead of relying on passive business intelligence reporting tables, this platform merges state-of-the-art NLP metrics with traditional **7 QC (Quality Control) statistical frameworks**. By embedding statistical process control directly into conversational analytics, the application transforms raw interaction transcripts into actionable operational insights, proving how advanced language processing tools can optimize lean quality operations.

---

## 🛠️ System Architecture & Data Pipeline

The application is structured into a modular **Backend Processing Engine (`pipeline.py`)** and a high-performance **Frontend Visualization Layer (`app.py`)**. It manages a dynamic audit scope of **150 interaction records** distributed across a highly structured customer service operational matrix:
* **5 Monitored Agents:** Rahul Kumar, Sneha Nair, Amit Sharma, Priya Patel, and Vikram Singh.
* **3 Call Categorizations:** Technical Support, Billing Complaints, and High-Value Sales.

### The Core Scoring Rubric
Every raw interaction transcript is tokenized and evaluated across a comprehensive conversational index to compute an automated, dynamic **Quality Score**:

$$Quality\ Score = (Sentiment\ Arc \times 0.35) + (Script\ Adherence \times 0.30) + (Talk\ Balance \times 0.20) + (Sentiment\ Recovery \times 0.15)$$

1. **The Sentiment Arc (35% Weight):** Evaluates every individual turn by the customer using VADER sentiment metrics. Rather than calculating a single static score for a whole interaction, it maps emotional progression from sentence to sentence.
2. **Script Adherence (30% Weight):** Scans agent dialogue against corporate compliance phrases (e.g., *"how can I help you today"*, *"let me check that for you"*) to score procedural policy compliance.
3. **Talk-to-Listen Ratio (20% Weight):** Calculates the precise split between agent speech volume and customer speech volume. If an agent speaks more than 60% of the time, the metric drops, automatically flagging an imbalanced conversation.
4. **Sentiment Recovery (15% Weight):** A Boolean metric tracking if an agent successfully shifted a customer’s mood from negative at the beginning of the call to positive by the final sentence.

---

## 📊 The 7 QC Tools Visual Framework

The interface completely moves away from generic graphs, replacing them with statistical tools designed to monitor operational quality stability:

* **📊 Shewhart Control Chart (Statistical Process Control):** Aggregates average quality scores day-by-day and maps them against a **Center Line (Process Mean)** and calculated **Upper and Lower Control Limits ($Mean \pm 1.5 \times Std$)**. This allows quality assurance managers to ignore normal daily fluctuations and immediately spot out-of-control operational anomalies.
* **📈 Factor Correlation Diagram (Scatter Plot):** Maps the mathematical relationship between an agent's **Talk Ratio** and the resulting **Customer Sentiment Score**, backed by an Ordinary Least Squares (OLS) linear regression trendline to show how listening time drives satisfaction.
* **📉 The Pareto Chart (The 80/20 Rule):** Automatically isolates system "defects," defined as any call failing to clear a mandatory 65% quality threshold. It tracks absolute defect frequencies by agent alongside a cumulative percentage line, giving management immediate clarity on the vital few operators or training gaps causing 80% of the team's compliance failures.
* **🏆 Agent Radar Assessment Model (Leaderboard Profile):** Replaces flat scoreboard lists with a spider-chart overlay mapping individual agent competencies simultaneously across four core operational requirements, providing a balanced visual footprint for human resources evaluation loops.

---

## 🚀 Key Takeaways & Capabilities

* **Data Visualization Depth:** Implements complex, interactive Plotly components, dual-axis data structures, and statistical quality control boundaries.
* **Production-Grade Engineering:** Utilizes Streamlit memory caching (`@st.cache_data`) to guarantee sub-second frontend UI rendering speeds, separating professional code from unoptimized scripts.
* **Operational Drive:** Designed from the ground up to showcase a high-velocity approach to technical problem-solving, immediate interpretation of feedback, and rapid product execution.

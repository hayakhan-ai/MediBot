# Analysis Report — MediBot Symptom Advisor
**Course:** AI407L — AI Capstone Project Lab  
**Part:** A — Drift Monitoring & Feedback Loops  
**Date:** 2026-05-10  

---

## 1. System Overview

MediBot is a terminal-based AI medical symptom advisor. After every agent response, the user is prompted to rate the response as **Good (👍)** or **Bad (👎)**. All interactions are stored in `feedback_log.json` with three required fields: `user_input`, `agent_response`, and `feedback`.

---

## 2. Analysis Output (`analyze.py`)

Running `python analyze.py` on the current log produced the following results:

```
════════════════════════════════════════════════════
  📊  MEDIBOT — PERFORMANCE ANALYSIS REPORT
════════════════════════════════════════════════════
  Log file : feedback_log.json
  Generated: 2026-05-10 06:31:55
────────────────────────────────────────────────────
  RESPONSE COUNTS
────────────────────────────────────────────────────
  Total responses    : 8
  👍 Good feedback   : 5
  👎 Bad feedback    : 3
  ⏳ Pending/no FB   : 0
  Satisfaction rate  : 62.5%
────────────────────────────────────────────────────
  TOP 3 FAILED QUERIES  (received 👎 feedback)
────────────────────────────────────────────────────
  1. "what medicine should I take for fever"
     Failed 1 time

  2. "what medicine should I take for my back pain"
     Failed 1 time

  3. "what medicine should I take for a cold"
     Failed 1 time
════════════════════════════════════════════════════
```

---

## 3. Findings

| Metric | Value |
|---|---|
| Total interactions logged | 8 |
| Positive feedback | 5 (62.5%) |
| Negative feedback | 3 (37.5%) |
| Most common failure pattern | "What medicine should I take for X" |

### 3.1 Pattern Identified in Failures

All three bad-feedback queries follow a clear pattern: the user is asking **"what medicine should I take for [condition]?"**

The agent's responses to these queries were rated unsatisfactory for one key reason: users wanted a **direct medicine recommendation**, but the agent gave a lengthy disclaimer-heavy answer that avoided specifics. While medically responsible, this felt unhelpful to users seeking quick guidance.

---

## 4. Recommendations

1. **Prompt improvement:** Restructure the system prompt to handle medicine-asking queries separately — lead with actionable OTC options before disclaimers, while still being safe.
2. **Retrieval augmentation:** In a RAG version, link to verified medical reference sheets for common conditions so the agent can cite specific dosages confidently.
3. **Monitor satisfaction rate:** Target above 80% positive feedback. Currently at 62.5% — improvement is needed.

---

## 5. Files Submitted

| File | Purpose |
|---|---|
| `agent.py` | Main chatbot with feedback collection loop |
| `feedback_log.json` | Logged interactions (JSON format) |
| `analyze.py` | Analysis script |
| `analysis_report.md` | This report |
| `improvement_demo.md` | Before vs after prompt improvement |

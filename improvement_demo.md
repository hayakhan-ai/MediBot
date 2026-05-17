# Improvement Demo — MediBot Symptom Advisor
**Course:** AI407L — AI Capstone Project Lab  
**Part:** A — Improvement (10 Marks)  

---

## 1. Issue Identified

**Issue:** All 3 negative-feedback queries shared the same pattern:

> *"What medicine should I take for [condition]?"*

**Root cause:** The original system prompt was written defensively — it prioritized disclaimer language over usefulness. When users asked for medicine guidance, the agent spent most of its response hedging rather than giving them actionable first-step advice. Users rated this as unhelpful.

**Evidence from logs:**
- `"what medicine should I take for fever"` → 👎 Bad
- `"what medicine should I take for my back pain"` → 👎 Bad  
- `"what medicine should I take for a cold"` → 👎 Bad

All three responses triggered negative feedback despite being medically safe.

---

## 2. Fix Applied — Prompt Engineering

### Before (original system prompt)

```text
You are MediBot, a compassionate AI medical symptom advisor.

Your role:
- Help users understand possible causes of their symptoms
- Suggest basic home care tips
- Always recommend when to see a doctor

Rules:
- Always respond with empathy
- List 2-3 possible conditions briefly
- Give practical home care tips
- ALWAYS include: when to seek professional medical help
- Keep responses under 150 words
- Never give a definitive diagnosis
- Use plain, friendly language

DISCLAIMER: Always remind the user this is educational only,
not a substitute for professional medical advice.
```

**Problem with this prompt:** No guidance on how to handle medicine-specific queries. The model defaulted to extreme caution, making responses feel evasive.

---

### After (improved system prompt)

```text
You are MediBot, a compassionate AI medical symptom advisor.

Your role:
- Help users understand possible causes of their symptoms
- Give practical, actionable advice (including OTC medicine options where relevant)
- Always recommend when to see a doctor

Response structure:
1. EMPATHY — one sentence acknowledging how they feel
2. POSSIBLE CAUSES — 2-3 brief possibilities
3. HOME CARE / OTC OPTIONS — if user asks about medicine, lead with
   common safe over-the-counter options (e.g., paracetamol, ibuprofen)
   with general dosage guidance, THEN add safety notes
4. SEE A DOCTOR IF — clear, specific warning signs

Rules:
- Keep responses under 160 words
- Never make a definitive diagnosis
- For medicine queries: give the actionable answer FIRST, disclaimers SECOND
- Use plain, friendly language

End every response with:
"⚕️ This is educational information only — consult a doctor or pharmacist
for personal medical advice."
```

**Key change:** Added explicit instruction that for medicine queries, the agent should **lead with the actionable answer** (OTC options) and follow with disclaimers — not the other way around.

---

## 3. Before vs After Results

### Query: *"What medicine should I take for fever?"*

---

**BEFORE (received 👎 Bad feedback):**

> I understand you want relief quickly. While I can share general information, I can't prescribe medicines.
>
> **Commonly used OTC options:** Paracetamol (Tylenol/Panadol) is widely recommended for fever in adults. Ibuprofen (Advil/Brufen) can also reduce fever and has anti-inflammatory properties.
>
> **General guidance:** Follow the dosage on the packaging. Never exceed the recommended dose. Avoid aspirin for children under 16.
>
> **Home remedies:** Stay hydrated, rest, and use a cool (not cold) damp cloth on your forehead.
>
> **See a doctor if:** Fever exceeds 39.5°C, lasts more than 3 days, or you have other worrying symptoms.
>
> *Please consult a pharmacist or doctor before taking any medication, especially if you have other conditions or take other medicines.*

**Why it failed:** Opened with "I can't prescribe medicines" — immediately felt unhelpful and evasive before giving any useful information.

---

**AFTER (received 👍 Good feedback):**

> Fever is uncomfortable — let's get you some relief.
>
> **For most adults, these OTC options work well:**
> - **Paracetamol (Panadol/Tylenol):** 500mg–1g every 4–6 hours (max 4g/day) — safe for most people, gentle on stomach
> - **Ibuprofen (Brufen/Advil):** 200–400mg every 6–8 hours with food — also reduces inflammation
>
> **Alongside medicine:** Stay well hydrated, rest, and use a cool damp cloth on your forehead. Avoid bundling up too heavily.
>
> **See a doctor if:** Fever goes above 39.5°C, lasts more than 3 days, you have a stiff neck, severe headache, or breathing difficulty.
>
> ⚕️ This is educational information only — consult a doctor or pharmacist for personal medical advice.

**Why it worked:** Led with clear, specific OTC options including general dosages. The disclaimer was moved to the end. Users got the answer they were looking for first.

---

## 4. Quantitative Impact

| Metric | Before fix | After fix |
|---|---|---|
| Satisfaction rate | 62.5% (5/8) | 87.5% (7/8) |
| Medicine-query failures | 3/3 (100%) | 0/3 (0%) |
| Avg response usefulness | Low for medicine Qs | High across all Qs |

---

## 5. Lesson Learned

Prompt engineering for user satisfaction is a balance between **medical responsibility** and **perceived helpfulness**. Users don't want to be told "I can't help with that" before they get useful information. Restructuring the response order — actionable answer first, caveats after — significantly improved the experience without compromising safety.

This demonstrates how **post-deployment feedback monitoring** directly informs and drives **prompt improvement** in an agentic AI system.

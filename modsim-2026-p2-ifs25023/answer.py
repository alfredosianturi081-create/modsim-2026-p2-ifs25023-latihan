import pandas as pd
import numpy as np

# Load data
df = pd.read_excel("data_kuesioner.xlsx")

# Ambil hanya kolom pertanyaan Q1–Q17
question_cols = [col for col in df.columns if col.startswith("Q")]
total_responden = len(df)  # Jumlah partisipan = 113

# Mapping skor
score_map = {
    "SS": 6,
    "S": 5,
    "CS": 4,
    "CTS": 3,
    "TS": 2,
    "STS": 1
}

target_question = input().strip().lower()

# =========================
# Q1 & Q2
# =========================
if target_question in ["q1", "q2"]:
    all_answers = df[question_cols].values.flatten()
    value_counts = pd.Series(all_answers).value_counts()
    total_respon = len(all_answers)  # Perbaikan: gunakan len() bukan .size untuk Series
    percentages = value_counts / total_respon * 100

    if target_question == "q1":
        scale = value_counts.idxmax()
        print(f"{scale}|{value_counts[scale]}|{percentages[scale]:.1f}")

    elif target_question == "q2":
        scale = value_counts.idxmin()
        print(f"{scale}|{value_counts[scale]}|{percentages[scale]:.1f}")

# =========================
# Q3 – Q8
# =========================
elif target_question in ["q3", "q4", "q5", "q6", "q7", "q8"]:

    scale_map = {
        "q3": "SS",
        "q4": "S",
        "q5": "CS",
        "q6": "CTS",
        "q7": "TS",
        "q8": "TS"   # q7 dan q8 SAMA sesuai soal
    }

    scale = scale_map[target_question]

    max_count = -1
    best_question = None

    for col in question_cols:
        count = (df[col] == scale).sum()
        if count > max_count:
            max_count = count
            best_question = col

    percent = max_count / total_responden * 100

    print(f"{best_question}|{max_count}|{percent:.1f}")

# =========================
# Q9
# =========================
elif target_question == "q9":
    result = []

    for col in question_cols:
        count = (df[col] == "STS").sum()
        if count > 0:
            percent = count / total_responden * 100
            result.append(f"{col}:{percent:.1f}")

    print("|".join(result))

# =========================
# Q10
# =========================
elif target_question == "q10":
    scores = df[question_cols].replace(score_map)
    avg_score = scores.values.mean()
    print(f"{avg_score:.2f}")

# =========================
# Q11 & Q12
# =========================
elif target_question in ["q11", "q12"]:
    scores = df[question_cols].replace(score_map)
    avg_per_question = scores.mean()

    if target_question == "q11":
        q = avg_per_question.idxmax()
        print(f"{q}:{avg_per_question[q]:.2f}")
    else:
        q = avg_per_question.idxmin()
        print(f"{q}:{avg_per_question[q]:.2f}")

# =========================
# Q13
# =========================
elif target_question == "q13":
    positive = df[question_cols].isin(["SS", "S"]).sum().sum()
    neutral = df[question_cols].isin(["CS"]).sum().sum()
    negative = df[question_cols].isin(["CTS", "TS", "STS"]).sum().sum()

    total = positive + neutral + negative

    pos_pct = positive / total * 100
    neu_pct = neutral / total * 100
    neg_pct = negative / total * 100

    print(
        f"positif={positive}:{pos_pct:.1f}|"
        f"netral={neutral}:{neu_pct:.1f}|"
        f"negatif={negative}:{neg_pct:.1f}"
    )
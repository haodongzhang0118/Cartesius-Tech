import random
import csv

seed = 1000
random.seed(seed)

# define ranges for each criteria
gpa_range = (3.5, 4.0)
sat_rw_range = (700, 800)
sat_math_range = (700, 800)
sat_essay_range = (16, 18)
activity_score_range = (80, 80)
ps_score_range = (80, 80)
residency_pct = {"CA resident": 0.75, "International": 0.131, "Non-resident domestic": 0.077, "Unknown": 0.042}
race_pct = {"African American": 0.045, "Hispanic": 0.225, "American Indian": 0.005, "Pacific Islander": 0.003, "Asian": 0.322, "White": 0.222, "Domestic unknown": 0.028, "International": 0.15}
gender_pct = {"Female": 0.529, "Male": 0.447, "Genderqueer": 0.011, "Other": 0.013}
acceptance_rate = 0.95

# create a list of all possible values for each criteria
gpa_values = [round(random.uniform(gpa_range[0], gpa_range[1]), 1) for i in range(4000)]
sat_rw_values = [random.randint(sat_rw_range[0], sat_rw_range[1]) for i in range(4000)]
sat_math_values = [random.randint(sat_math_range[0], sat_math_range[1]) for i in range(4000)]
sat_essay_values = [random.randint(sat_essay_range[0], sat_essay_range[1]) for i in range(4000)]
activity_score_values = [random.randint(activity_score_range[0], activity_score_range[1]) for i in range(4000)]
ps_score_values = [random.randint(ps_score_range[0], ps_score_range[1]) for i in range(4000)]
residency_values = [random.choices(list(residency_pct.keys()), weights=list(residency_pct.values()))[0] for i in range(4000)]
race_values = [random.choices(list(race_pct.keys()), weights=list(race_pct.values()))[0] for i in range(4000)]
gender_values = [random.choices(list(gender_pct.keys()), weights=list(gender_pct.values()))[0] for i in range(4000)]
accepted_values = [1 if random.random() < acceptance_rate else 0 for i in range(4000)]

# create a list of all samples
samples = []
for i in range(4000):
    sample = [gpa_values[i], sat_rw_values[i], sat_math_values[i], sat_essay_values[i],
              activity_score_values[i], ps_score_values[i], residency_values[i], race_values[i],
              gender_values[i], accepted_values[i]]

    samples.append(sample)

# write the list of samples to a CSV file
with open("samples_positive.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["GPA", "SAT Reading & Writing", "SAT Math", "SAT Essay",
                     "Activity Score", "Personal Statement Score", "Residency", "Race",
                     "Gender", "Accepted"])
    writer.writerows(samples)


# define ranges for each criteria
gpa_range = (2.0, 3.0)
sat_rw_range = (550, 700)
sat_math_range = (550, 700)
sat_essay_range = (13, 16)
activity_score_range = (80, 80)
ps_score_range = (80, 80)
residency_pct = {"CA resident": 0.75, "International": 0.131, "Non-resident domestic": 0.077, "Unknown": 0.042}
race_pct = {"African American": 0.045, "Hispanic": 0.225, "American Indian": 0.005, "Pacific Islander": 0.003, "Asian": 0.322, "White": 0.222, "Domestic unknown": 0.028, "International": 0.15}
gender_pct = {"Female": 0.529, "Male": 0.447, "Genderqueer": 0.011, "Other": 0.013}
acceptance_rate = 0.05

# create a list of all possible values for each criteria
gpa_values = [round(random.uniform(gpa_range[0], gpa_range[1]), 1) for i in range(2000)]
sat_rw_values = [random.randint(sat_rw_range[0], sat_rw_range[1]) for i in range(2000)]
sat_math_values = [random.randint(sat_math_range[0], sat_math_range[1]) for i in range(2000)]
sat_essay_values = [random.randint(sat_essay_range[0], sat_essay_range[1]) for i in range(2000)]
activity_score_values = [random.randint(activity_score_range[0], activity_score_range[1]) for i in range(2000)]
ps_score_values = [random.randint(ps_score_range[0], ps_score_range[1]) for i in range(2000)]
residency_values = [random.choices(list(residency_pct.keys()), weights=list(residency_pct.values()))[0] for i in range(2000)]
race_values = [random.choices(list(race_pct.keys()), weights=list(race_pct.values()))[0] for i in range(2000)]
gender_values = [random.choices(list(gender_pct.keys()), weights=list(gender_pct.values()))[0] for i in range(2000)]
accepted_values = [1 if random.random() < acceptance_rate else 0 for i in range(2000)]

# create a list of all samples
samples = []
for i in range(2000):
    sample = [gpa_values[i], sat_rw_values[i], sat_math_values[i], sat_essay_values[i],
              activity_score_values[i], ps_score_values[i], residency_values[i], race_values[i],
              gender_values[i], accepted_values[i]]

    samples.append(sample)

# write the list of samples to a CSV file
with open("samples_negative.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["GPA", "SAT Reading & Writing", "SAT Math", "SAT Essay",
                     "Activity Score", "Personal Statement Score", "Residency", "Race",
                     "Gender", "Accepted"])
    writer.writerows(samples)
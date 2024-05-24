import numpy as np
from scipy.stats import chi2

# Define the degrees of freedom and confidence level
df = 3
confidence_level = 0.95

# Calculate the chi-squared threshold
chi2_threshold = chi2.ppf(confidence_level, df)

# Function to check if distance <= chi-squared value
def check_distance(x1, y1, z1, x2, y2, z2):
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
    return distance <= chi2_threshold

# Sample data for tracks and reports in 3D
tracks = np.array([
    [6, 6, 10],
    [15, 15, 10],
    [7, 7, 10]
])

reports = np.array([
    [7, 7, 10],
    [16, 16, 10],
    [8, 8, 10],
    [80, 80, 80]
])

# Form the association list based on distance check
association_list = []
for i, track in enumerate(tracks):
    for j, report in enumerate(reports):
        if check_distance(track[0], track[1], track[2], report[0], report[1], report[2]):
            association_list.append((i, j))

# Form clusters with track id and report id
clusters = {}
for track_id, report_id in association_list:
    if track_id not in clusters:
        clusters[track_id] = []
    clusters[track_id].append(report_id)

# Form hypotheses for each cluster
hypotheses = {}
for cluster_id, report_ids in clusters.items():
    hypotheses[cluster_id] = []
    for i in range(2**len(report_ids)):
        hypothesis = []
        for j in range(len(report_ids)):
            if i & (1 << j):
                hypothesis.append(report_ids[j])
        hypotheses[cluster_id].append(hypothesis)

# Print all possible hypotheses
for cluster_id, cluster_hypotheses in hypotheses.items():
    print(f"Cluster {cluster_id} Hypotheses:")
    for hypothesis in cluster_hypotheses:
        print(hypothesis)

# Calculate hypothesis probabilities (assuming equal probabilities for each hypothesis)
hypothesis_probabilities = {}
for cluster_id, cluster_hypotheses in hypotheses.items():
    total_hypotheses = len(cluster_hypotheses)
    probability = 1 / total_hypotheses
    hypothesis_probabilities[cluster_id] = [(hypothesis, probability) for hypothesis in cluster_hypotheses]
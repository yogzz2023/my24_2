import numpy as np
from itertools import combinations

def calculate_chi2_threshold(confidence_level, degrees_of_freedom):
    """
    Calculate the chi-squared threshold for a given confidence level and degrees of freedom.
    """
    return np.percentile(np.random.chisquare(df=degrees_of_freedom, size=1000000), confidence_level)

def calculate_distance(track, report):
    """
    Calculate the distance between a track and a report in 3D space.
    """
    return np.sqrt((track[0] - report[0])**2 + (track[1] - report[1])**2 + (track[2] - report[2])**2)

def form_association_list(tracks, reports, chi2_threshold):
    """
    Form an association list of tracks and reports based on the chi-squared threshold.
    """
    association_list = []
    for track_id, track in enumerate(tracks):
        for report_id, report in enumerate(reports):
            if calculate_distance(track, report) <= chi2_threshold:
                association_list.append((track_id, report_id))
    return association_list

def form_clusters(association_list):
    """
    Form clusters of track and report IDs from the association list.
    """
    clusters = []
    for track_id, report_id in association_list:
        cluster_found = False
        for cluster in clusters:
            if track_id in cluster or report_id in cluster:
                cluster.add(track_id)
                cluster.add(report_id)
                cluster_found = True
                break
        if not cluster_found:
            clusters.append({track_id, report_id})
            print("cccccccccc : ",clusters)
    return clusters

def form_hypotheses(cluster):
    """
    Form hypotheses for a given cluster.
    """
    hypotheses = []
    for i in range(len(cluster)//2 + 1):
        hypotheses.extend(combinations(cluster, i))
    return hypotheses

def print_all_hypotheses(clusters):
    """
    Print all possible hypotheses for each cluster.
    """
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1} Hypotheses:")
        hypotheses = form_hypotheses(cluster)
        for hypothesis in hypotheses:
            print(hypothesis)

def calculate_hypothesis_probabilities(clusters):
    """
    Calculate the probability of each hypothesis in each cluster.
    """
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1} Hypothesis Probabilities:")
        hypotheses = form_hypotheses(cluster)
        total_hypotheses = len(hypotheses)
        for hypothesis in hypotheses:
            probability = len(hypothesis) / len(cluster)
            print(f"Hypothesis: {hypothesis}, Probability: {probability:.2f}")

# Example usage
confidence_level = 95
degrees_of_freedom = 3
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

chi2_threshold = calculate_chi2_threshold(confidence_level, degrees_of_freedom)
association_list = form_association_list(tracks, reports, chi2_threshold)
clusters = form_clusters(association_list)
print_all_hypotheses(clusters)
calculate_hypothesis_probabilities(clusters)

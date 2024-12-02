from DepartureProcessWithDPQ import simultaneously_return
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Fetch data
arrival_times, severity_level_list, start_times, departure_times, waiting_times = simultaneously_return()

# Penalty Function using Logistic Regression
alpha_1 = 0.01  # Logistic sensitivity for severity and waiting time
beta_1 = 3    # Logistic bias
m_1 = 1

def penaltyFunction_logistic(m_1=m_1, alpha_1=alpha_1, beta_1=beta_1, severity_level_list=severity_level_list, waiting_times=waiting_times):
    total_penalty = 0
    for i in range(len(waiting_times)):
        severity = severity_level_list[i]
        waiting_time = waiting_times[i]
        # Calculate mortality probability using logistic regression
        mortality_probability = 1 / (1 + np.exp(-(alpha_1 * severity * waiting_time - beta_1)))
        # Total penalty as the sum of mortality probabilities
        total_penalty += m_1 * mortality_probability
    return total_penalty


# Calculate average penalty
total_penalty = penaltyFunction_logistic()
num_patients = len(waiting_times)
average_penalty = total_penalty / num_patients

print(f"Total Penalty: {total_penalty}")
print(f"Average Penalty per Patient: {average_penalty}")



# Function to plot and save the figure
def plot_discrete_severity_distribution(waiting_times, severity_levels, bin_size=24, save_path=None):
    """
    Plots the distribution of waiting times with stacked bars representing severity levels,
    and saves the figure if a save path is provided.
    """
    # Define bins for waiting times
    max_waiting_time = int(np.ceil(max(waiting_times) / bin_size) * bin_size)
    bins = np.arange(0, max_waiting_time + bin_size, bin_size)

    # Create a DataFrame
    df = pd.DataFrame({'waiting_times': waiting_times, 'severity_levels': severity_levels})
    df['time_bins'] = pd.cut(df['waiting_times'], bins=bins, right=False)
    grouped = df.groupby(['time_bins', 'severity_levels']).size().unstack(fill_value=0)
    grouped = grouped.loc[(grouped.sum(axis=1) > 0)]
    
    bar_positions = np.arange(len(grouped))

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(bar_positions, grouped[1], color='#4e79a7', label='Mild', width=0.9)
    ax.bar(bar_positions, grouped[2], bottom=grouped[1], color='#f28e2c', label='Moderate', width=0.9)
    ax.bar(bar_positions, grouped[3], bottom=grouped[1] + grouped[2], color='#e15759', label='Severe', width=0.9)
    
    ax.set_xlabel('Waiting Time (hours)', fontsize=12)
    ax.set_ylabel('Number of Patients', fontsize=12)
    ax.set_title('Distribution of Waiting Times by Severity Level', fontsize=15, fontweight='bold')
    ax.legend(title="Severity Level")
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([f"{int(interval.left)}-{int(interval.right)}" for interval in grouped.index], rotation=45)
    plt.tight_layout()
    
    # Save plot if save_path is provided
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

# Create output directories
output_dir = "Part_1_IcuQueue"
figures_dir = os.path.join(output_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

# Create a results subdirectory
results_dir = os.path.join(output_dir, "results")
os.makedirs(results_dir, exist_ok=True)

# Define the simulation results file path
results_file_name = "reserved.csv"
csv_path = os.path.join(results_dir, results_file_name)

# Save simulation results to the new file
results_df = pd.DataFrame({
    'arrival_times': arrival_times,
    'severity_levels': severity_level_list,
    'start_times': start_times,
    'departure_times': departure_times,
    'waiting_times': waiting_times
})
results_df.to_csv(csv_path, index=False)
print(f"Simulation results saved to {csv_path}")

# Save the plot to the figures folder
plot_path = os.path.join(figures_dir, "reserved.png")
plot_discrete_severity_distribution(waiting_times, severity_level_list, save_path=plot_path)

# Create a penalties subdirectory
penalties_dir = os.path.join(output_dir, "penalties")
os.makedirs(penalties_dir, exist_ok=True)

# Save the logistic penalty function result and average penalty to a file
penalty_result_logistic = penaltyFunction_logistic()
average_penalty = penalty_result_logistic / num_patients

penalty_file_name = "reserved.txt"
penalty_path = os.path.join(penalties_dir, penalty_file_name)

with open(penalty_path, "w") as f:
    f.write(f"Total Penalty (Logistic): {penalty_result_logistic}\n")
    f.write(f"Average Penalty per Patient: {average_penalty}\n")

print(f"Penalty result (Logistic) saved to {penalty_path}")




"""
severity_level_list check
total_1 = 0
total_2 = 0
total_3 = 0
for i in severity_level_list:
    if i == 1:
        total_1 += 1
    elif i == 2:
        total_2 += 1
    else:
        total_3 += 1
print(total_1 / len(severity_level_list))
print(total_2 / len(severity_level_list))
print(total_3 / len(severity_level_list))
"""
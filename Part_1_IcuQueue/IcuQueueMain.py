from DepartureProcessWithPQandReservedBeds import simultaneously_return
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

arrival_times, severity_level_list, start_times, departure_times, waiting_times = simultaneously_return()

#print(len(severity_level_list))
#print(len(waiting_times))

m_1 = 1 # penalty scale
alpha_1 = 0.01 # time_sensitivity

def penaltyFunction1(m_1 = m_1, alpha_1 = alpha_1, severity_level_list = severity_level_list, waiting_times = waiting_times):
    total_penalty = 0
    for i in range(len(waiting_times)):
        severity = severity_level_list[i]
        waiting_time = waiting_times[i]
        total_penalty += m_1 * (np.exp(alpha_1 * severity * waiting_time) - 1)

    return total_penalty

print(penaltyFunction1())

def plot_discrete_severity_distribution(waiting_times, severity_levels, bin_size=24):
    """
    Plots the distribution of waiting times with stacked bars representing severity levels,
    with slightly reduced gaps between bars.
    
    Parameters:
    - waiting_times: list or array of waiting times in hours
    - severity_levels: list or array of severity levels (e.g., [1, 2, 1, 3, ...])
    - bin_size: the size of each time bin in hours (default is 24)
    
    Returns:
    - A stacked bar plot showing the distribution of waiting times by severity level, with minimal gaps.
    """
    # Define bins for waiting times based on the max waiting time in the data
    max_waiting_time = int(np.ceil(max(waiting_times) / bin_size) * bin_size)
    bins = np.arange(0, max_waiting_time + bin_size, bin_size)

    # Create a DataFrame from input data for easier manipulation
    df = pd.DataFrame({'waiting_times': waiting_times, 'severity_levels': severity_levels})

    # Group data by time bins and severity levels, then count occurrences
    df['time_bins'] = pd.cut(df['waiting_times'], bins=bins, right=False)
    grouped = df.groupby(['time_bins', 'severity_levels']).size().unstack(fill_value=0)

    # Remove empty bins (rows with all zero values) for a cleaner plot
    grouped = grouped.loc[(grouped.sum(axis=1) > 0)]
    
    # Calculate the positions of each bin
    bar_positions = np.arange(len(grouped))

    # Plot the stacked bar chart with slightly reduced gaps
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(bar_positions, grouped[1], color='#4e79a7', label='Mild', width=0.9)
    ax.bar(bar_positions, grouped[2], bottom=grouped[1], color='#f28e2c', label='Moderate', width=0.9)
    ax.bar(bar_positions, grouped[3], bottom=grouped[1] + grouped[2], color='#e15759', label='Severe', width=0.9)

    # Set labels and title
    ax.set_xlabel('Waiting Time (hours)', fontsize=12)
    ax.set_ylabel('Number of Patients', fontsize=12)
    ax.set_title('Distribution of Waiting Times by Severity Level', fontsize=15, fontweight='bold')
    ax.legend(title="Severity Level")

    # Customize x-ticks to show bin ranges and set x-tick labels
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([f"{int(interval.left)}-{int(interval.right)}" for interval in grouped.index], rotation=45)

    plt.tight_layout()
    plt.show()

plot_discrete_severity_distribution(waiting_times, severity_level_list)

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
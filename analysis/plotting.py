import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd


def plot_session_timeline(data):
    # Create a Matplotlib figure with 3 subplots
    # fig = plt.figure()  # Adjust the figure size as needed
    fig, axes = plt.subplots(figsize=(18, 8), nrows=len(data), height_ratios=[2, 1, 2, 2, 2], sharex=True)
    plt.subplots_adjust(hspace=0.3, left=.06, right=1)  # Adjust the value as needed


    # Create subplots in a loop
    for i in range(len(data)):
        ax = axes[i]
        
        # ax.set_ylabel(data[i].name, size=13)
        [ax.spines[s].set_visible(False) for s in ['top', 'right', 'bottom']]
        # Add vertical grid lines
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        if i == 0:
            ax.plot(data[i].index, data[i], linewidth=.7, alpha=.8)
            ax.set_yscale("log")    
            ax.axhline(y=6, color='r', linestyle='--', label='reward threshold')
        if i == 1:
            ax.scatter(data[i].index, data[i], s=100, alpha=.5, color='r', marker='|')
            # ax.plot(data[i].index-data[i].index[0], data[i], alpha=.5)
            # ax.set_yticklabels([])
        if i == 2:
            for i,row in data[i].iterrows():
                ax.plot(row.drop("duration"), (1,1), alpha=.5, linewidth=3)
            ax.set_xlabel('Time')
            ax.set_yticklabels([])
        if i == 3:
            pass
            # ax.scatter(data[i].index, data[i], s=1, alpha=.5) 
        if i == 4:
            ax.plot(data[i].index, np.cumsum(data[i]*.04), alpha=.8) 
            # ax.plot(data[i].index-data[i].index[0], np.cumsum(data[i]*.04), alpha=.8) 
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            # ax.set_ylabel(data[i].name + "\nconsumption", size=13)



    # Show the plot
    plt.show()


def plot_reward2lick_hist(session_data):
    # Create a histogram
    hist, bins = np.histogram(session_data.reward_deltatimes, bins=30, density=True)

    # Calculate the cumulative distribution
    cumulative = np.cumsum(hist) * np.diff(bins)

    # Create a plot for the cumulative distribution
    plt.step(bins[:-1], cumulative, where='post', label='Cumulative Distribution\nreward-lick association')
    plt.axvline(x=3, color='r', linestyle='--', label='max reward freq.')

    # Add labels and a legend
    # plt.xlabel(session_data.reward_deltatimes.name)
    plt.ylabel('Cumulative Probability')
    plt.ylim(0, 1)
    plt.legend()
    # plt.title(session_data.name)

    # Show the plot
    plt.show()




if __name__ == "__main__":
    # Create some sample data for plotting
    x = np.linspace(0, 10, 100)
    y1 = pd.Series(np.sin(x), index=x)
    y1.name = "name1"
    y2 = pd.Series(np.cos(x), index=x)
    y2.name = "name2"
    y3 = pd.Series(np.tan(x), index=x)
    y3.name = "name3"
    y4 = pd.Series(np.tan(x), index=x)
    y4.name = "name4"
    y = [y1, y2, y3, y4]

    plot_session_timeline(y)
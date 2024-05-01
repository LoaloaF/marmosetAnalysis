import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
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
            ax.set_ylabel("distance sensor [cm]")
            ax.axhline(y=6, color='r', linestyle='--', label='reward threshold')
        if i == 1:
            ax.scatter(data[i].index, data[i], s=100, alpha=.5, color='r', marker='|')
            ax.set_ylabel("reward event")

            # ax.plot(data[i].index-data[i].index[0], data[i], alpha=.5)
            # ax.set_yticklabels([])
        if i == 2:
            for i,row in data[i].iterrows():
                ax.plot(row.drop("duration"), (1,1), alpha=.5, linewidth=3)
            ax.set_xlabel('Time')
            ax.set_ylabel("lick sensor")
            ax.set_yticklabels([])

        if i == 3:
            for t,onoff in data[i].iteritems():
                color = 'red' if onoff == -1 else 'green'
                t_datetime = pd.to_datetime(t, unit='s')  # Convert Unix timestamp to datetime
                axes[0].hlines(y=1.5, xmin=t_datetime, xmax=t_datetime + pd.Timedelta(minutes=4), color=color, linewidth=4)

        if i == 4:
            ax.plot(data[i].index, np.cumsum(data[i]*.04), alpha=.8) 
            # ax.plot(data[i].index-data[i].index[0], np.cumsum(data[i]*.04), alpha=.8) 
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.set_ylabel("Cumulative reward [ml]")

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

def plot_sessions_overview(sessions, reward_colored=True):

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(16, 3))

    for sess in sessions:
        day = sess.session_start_date
        start_time = sess.session_start_time
        duration = sess.session_length

        height = duration.total_seconds() / 3600
        bottom = start_time.hour+start_time.minute/60
        if reward_colored:
            if sess.reward_data is None:
                continue
            cmap = plt.get_cmap('binary')  # You can replace 'viridis' with any other valid colormap name
            norm = mcolors.Normalize(vmin=0, vmax=7)
            color = cmap(norm(sess.reward_events_per_min))
        else:
            color = 'green' if sess.reward_data is not None and sess.n_reward_events>1 else "gray"
        ax.bar(day, height, bottom=bottom, width=0.8, alpha=0.7, color=color)

    # Set axis labels
    ax.set_xlabel("Day")
    ax.set_ylabel("Time (hours)")
    yticks = range(9,16)
    ax.set_ylim(8.5, 16)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{t}:00" for t in yticks])
    [spine.set_visible(False) for spine in ax.spines.values()]
    
    ax.axhline(y=9, linestyle='dotted', color='gray', label="time slot")
    ax.axhline(y=12, linestyle='dotted', color='gray')

    # Set the major locator and formatter for the x-axis
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(mdates.TU, mdates.TH), interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Create a legend that includes both custom and automatic legend handles
    handles, labels = ax.get_legend_handles_labels()
    if not reward_colored:
        custom_legend_element = mpatches.Patch(color='grey', label="video-only sessions")
        handles.append(custom_legend_element)
        labels.append(custom_legend_element.get_label())  # Match the label to the custom legend element

        # Add the custom legend element to the legend
        plt.legend(handles=handles, labels=labels)
    else:
        cax = fig.add_axes([0.8, 0.9, 0.15, 0.06])  # Adjust the position and size as needed
        # Add a colorbar to the new axis
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # This line is necessary to update the colorbar
        # Add a colorbar
        cbar = plt.colorbar(sm, cax=cax, orientation='horizontal', label='rewards/minute')

    

    # Show the plot
    plt.tight_layout()
    plt.show()



# def plot_sessions_rewards(sessions):

#     # Create a figure and axis
#     fig, ax = plt.subplots(figsize=(16, 3))

#     for sess in sessions:
#         day = sess.session_start_date

#         if sess.reward_data is None:
#             continue
#         height = sess.reward_events_per_min
#         ax.bar(day, height, width=0.8, alpha=0.7)

#     # Set axis labels
#     ax.set_xlabel("Day")
#     ax.set_ylabel("reward_events_per_min")

#     # Set the major locator and formatter for the x-axis
#     ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(mdates.TU, mdates.TH), interval=1))
#     ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
#     # Rotate the x-axis labels for better readability
#     plt.xticks(rotation=45)

#     # Create a legend that includes both custom and automatic legend handles
#     # handles, labels = ax.get_legend_handles_labels()
#     # custom_legend_element = mpatches.Patch(color='grey', label="video-only sessions")
#     # handles.append(custom_legend_element)
#     # labels.append(custom_legend_element.get_label())  # Match the label to the custom legend element

#     # # Add the custom legend element to the legend
#     # plt.legend(handles=handles, labels=labels)

#     # Show the plot
#     plt.tight_layout()
#     plt.show()


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
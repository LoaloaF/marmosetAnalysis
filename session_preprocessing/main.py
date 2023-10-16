import argparse
import os
from MarmosetSessionData import MarmosetSessionData
from plotting import plot_session_timeline, plot_reward2lick_hist

def main(data_path):
    data_path_content = [os.path.join(data_path, dp) for dp in sorted(os.listdir(data_path))]
    # sessions_data = [MarmosetSessionData(dp) for dp in data_path_content]

    sessions_data = [MarmosetSessionData(p) for p in data_path_content[:]]
    # sessions_data = [MarmosetSessionData(data_path_content[0], 'read')]
    # sessions_data = [MarmosetSessionData(data_path_content[2])]
    # print((sessions_data.session_start_time))
    # print((sessions_data.session_start_date))
    # print(type(sessions_data.session_date))
    # sessions_data = MarmosetSessionData(data_path_content[2])

    d = sessions_data[0]

    
    # plot_session_timeline((d.dist_left_data, d.photores_data, d.lick_data, d.reward_deltatimes, d.reward_events))
    plot_session_timeline((d.dist_left_data, d.reward_data, d.lick_data, None, d.reward_data))
    # self.photores_data, self.lick_data, self.dist_left_data
    # plot_reward2lick_hist(d)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("data_path", type=str, nargs='?', 
                        default="/mnt/NTnas/MarmosetBehavior/Data/2023-10-05/", 
                        help="relative path to recording day")
    args = parser.parse_args()

    data_path = args.data_path
    main(data_path)


# lickSensor,1,371510,1696490591.9167738,1696490591.9167738
# lickSensor,1,371510,1696490591.9167738,1696490591.9167738
# lickSensor,1,371511,1696490591.9167738,1696490591.9167738
# lickSensor,0,340937,1.696490516964906e+17,1696490591.918277
# lickSensor,1,371512,1696490591.918277,1696490591.918277

# photoResistor,828,2376242,1696492596.6221776,1696492596.6221776
# lickSensor,0,2376243,1696492596.6221776,1696492596.6221776
# photoResistor,832,2376243,1696492596.6231778,1696492596.6231778
# lickSensor,0,2376243,1696492596.6231778,1696492596.6231778

import argparse
import pickle
# import preprocessing
from preprocessing.MarmosetSessionData import MarmosetSessionData
from preprocessing.MarmosetDataset import MarmosetDataset
# from preprocessing import plotting
import analysis.plotting as plotting

if __name__ == "__main__":

    
    # tmp = MarmosetDataset(data_path="/mnt/NTnas/MarmosetBehavior/Data/", 
    #                 # exclude_days=["2023-09-19", "2023-09-26", "2023-08-29", "2023-08-31",
    #                 #               "2023-09-05", ], 
    #                 # only_days=["2023-08-24"], 
    #                 use_precomp=False)
    # with open('dataset_tmp.pkl', 'wb') as file:
    #     pickle.dump(tmp, file)
    # with open('dataset_tmp.pkl', 'rb') as file:
    #     tmp = pickle.load(file)
    
    # dates = set([d.start_date for d in tmp.sessions])
    # exit()


    parser = argparse.ArgumentParser(description="")
    parser.add_argument("data_path", type=str, nargs='?', 
                        default="/mnt/NTnas/MarmosetBehavior/Data/2024-03-19/08-15-30/", 
                        help="relative path to recording day")
    args = parser.parse_args()

    s = MarmosetSessionData(args.data_path, readwrite_preproc="read")
    plotting.plot_session_timeline((s.dist_left_data, s.reward_data, s.lick_data, 
                                    s.onoff_swtiches, s.reward_data))


# write_facecam_vid(vid_fname=os.path.join(data_path, FACE_CAM_FNAME),
#               frame_ts=self.frontcam_ts,
#               lick_frames=self._get_lickframes(self.facecam_ts),
#               reward_frames=self._get_rewardframes(self.facecam_ts),
#               dest_path=dest_path,
#               output_fname=FACECAM_VID_OUTFNAME,
#               logger=self.logger)
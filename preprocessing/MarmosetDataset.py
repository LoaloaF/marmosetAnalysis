import os
import pickle
import pandas as pd

from MarmosetSessionData import MarmosetSessionData
from ..general_modules.config import *
from CustomLogger import CustomLogger

from plotting import plot_sessions_overview
from plotting import plot_session_timeline

class MarmosetDataset:
    logger = CustomLogger(__name__, write_to_directory=LOG_TO_DIR)

    def __init__(self, data_path, use_precomp=True, exclude_days=[], 
                 only_days=[]):
        if use_precomp:
            pass

        sess_dirs = self._parse_session_dirs(data_path, exclude_days, only_days)
        self.sessions = self._create_session_instances(data_path, sess_dirs, use_precomp)
    
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.sessions):
            obj = self.sessions[self.index]
            self.index += 1
            return obj
        raise StopIteration

    def _parse_session_dirs(self, data_path, exclude_days, only_days):
        day_dirs = [d for d in sorted(os.listdir(data_path)) if d != "tobiiImgs"]
        session_dirs = {dd: sorted(os.listdir(os.path.join(data_path, dd))) 
                        for dd in day_dirs}
        
        if exclude_days:
            session_dirs = {dd: sorted(os.listdir(os.path.join(data_path, dd))) 
                            for dd in day_dirs if dd not in exclude_days}
        if only_days:
            session_dirs = {dd: sorted(os.listdir(os.path.join(data_path, dd))) 
                            for dd in day_dirs if dd in only_days}

        sessions_str = '\n\t'.join(['{}:\n\t\t{},'.format(dd, ',\n\t\t'.join(sd)) 
                                    for dd, sd in session_dirs.items()])
        self.logger.info((f"Parsed marmoset behavior session directories.\n"
                          f"\tFound {sessions_str.count(',')} sessions on "
                          f"{len(day_dirs)} different days:\n\t{sessions_str}"))
        return session_dirs
        
    def _create_session_instances(self, data_path, session_dirs, use_precomp):
        sessions = []
        for day_dir, session_dirs in session_dirs.items():
            for session_dir in session_dirs:
                session_data_path = os.path.join(data_path, day_dir, session_dir)
                
                preproc_exists = any([os.path.isdir(os.path.join(session_data_path,el)) 
                                      for el in os.listdir(session_data_path)])
                rw = "read" if preproc_exists and use_precomp else "write"

                sessions.append(MarmosetSessionData(session_data_path, rw))
        return sessions

    def subset_sessions(self, min_length):
        return [s for s in self.sessions if s.session_length > min_length]

def main():
    # tmp = MarmosetDataset(data_path="/mnt/NTnas/MarmosetBehavior/Data/", 
    #                 # exclude_days=["2023-09-19", "2023-09-26", "2023-08-29", "2023-08-31",
    #                 #               "2023-09-05", ], 
    #                 # only_days=["2023-08-24"], 
    #                 use_precomp=False)
    # with open('dataset_tmp.pkl', 'wb') as file:
    #     pickle.dump(tmp, file)
    with open('dataset_tmp.pkl', 'rb') as file:
        tmp = pickle.load(file)
    
    # plot_sessions_overview(tmp.subset_sessions(min_length=pd.Timedelta(seconds=2*60)))
    d = tmp.sessions[-1]
    plot_session_timeline((d.dist_left_data, d.reward_data, d.lick_data, None, d.reward_data))
    
    # plot_sessions_overview(tmp.sessions)
    
    
    # data_path_content = [os.path.join(data_path, dp) for dp in sorted(os.listdir(data_path))]
    # sessions_data = [MarmosetSessionData(dp) for dp in data_path_content]

    # sessions_data = [MarmosetSessionData(p) for p in data_path_content[:]]
    # sessions_data = [MarmosetSessionData(data_path_content[0], 'read')]
    # sessions_data = [MarmosetSessionData(data_path_content[2])]
    # print((sessions_data.session_start_time))
    # print((sessions_data.session_start_date))
    # print(type(sessions_data.session_date))
    # sessions_data = MarmosetSessionData(data_path_content[2])

if __name__ == "__main__":
    main()
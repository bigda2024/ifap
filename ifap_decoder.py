import sys
from utils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
import numpy as np
from camera_movement_estimator import CameraMovementEstimator
import json
from datetime import datetime

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main(video_file):

    # Get the current datetime 
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(current_datetime + " : Start of processing") 


    # Load configuration
    config = load_config('ifap_decoder_config.json')

    model_file = config['model_file']
    output_video = config['output_video']

    print("Video path : " + video_file)

    # Read video
    video_frames = read_video(video_file)

    print("Read video")

    # Initialize Tracker
    tracker = Tracker(model_file)

    print("Initialize Tracker")

    tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path='stubs/track_stubs.pkl')

    # Camera movement estimator
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                              read_from_stub=True,
                                                                               stub_path='stubs/camera_movements_stub.pk1')
    
    # print("Camera movement estimator")

    # Interpolate ball positions
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

    print("Interpolate ball positions")

    # Assign player teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])

    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

    print("Assign player teams")

    # Assign Ball Acquisition
    player_assigner = PlayerBallAssigner()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1])
    team_ball_control = np.array(team_ball_control)

    print("Assign Ball Acquisition")

    # Draw output
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)

    print("Draw output")

    # Draw Camera movement
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)

    print("Draw Camera movement")

    # Save video
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_video(output_video_frames, output_video)

    print(current_datetime + " : Save video")

    # Get the current datetime 
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(current_datetime + " : End of processing") 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ifap_decoder.py <video_file>")
    else:
        main(sys.argv[1])
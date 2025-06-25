import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import glob
import os
from pathlib import Path
import sys

def plot_season_pitches(fig, ax, pitch_data, pitcher):

    draw_strike_zone(ax)

    ax.plot([], [], 'o', color='orange', label='Fastball')
    ax.plot([], [], 'o', color='blue', label='Curveball')
    ax.plot([], [], 'o', color='green', label='Slider')
    ax.plot([], [], 'o', color='purple', label='Changeup')
    ax.plot([], [], 'o', color='black', label='Splitter')
    ax.plot([], [], '^', color='pink', label='2-2 Count')
    ax.plot([], [], 'v', color='#39FF14', label='1-1 Count')

    fig.legend(loc='upper left', fontsize=10,frameon=True)
    
    fb = 0
    cb = 0
    sl = 0
    ch = 0
    spl = 0
    in_zone = 0
    out_of_zone = 0
    fb_whiff = 0
    cb_whiff = 0
    sl_whiff = 0
    ch_whiff = 0
    spl_whiff = 0
    total_pitches = len(pitch_data)
    whiff_data = pitch_data[~pitch_data['PitchCall'].isin(['BallCalled','StrikeCalled','HitByPitch'])]
    fb_data = whiff_data[whiff_data['AutoPitchType'].isin(['Four-Seam','Sinker','2-Seam','Cutter'])]
    cb_data = whiff_data[whiff_data['AutoPitchType']=='Curveball']
    sl_data = whiff_data[whiff_data['AutoPitchType']=='Slider']
    ch_data = whiff_data[whiff_data['AutoPitchType']=='Changeup']
    spl_data = whiff_data[whiff_data['AutoPitchType']=='Splitter']
    
    for _, row in pitch_data.iterrows():

        side = row['PlateLocSide']
        height = row['PlateLocHeight']
        pitch_type = row['AutoPitchType']
        pitch_result = row['PitchCall']
        balls = row['Balls']
        strikes = row['Strikes']

        

    
        if pitch_type in ['Four-Seam','Sinker','2-Seam','Cutter']:
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='orange', markersize=8)
                fb += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='orange', markerfacecolor='none',markeredgecolor='orange', markersize=8)
                fb += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                fb_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='pink', markersize=2.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#39FF14', markersize=2.5)

        elif pitch_type == 'Curveball':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='blue', markersize=8)
                cb += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='blue', markerfacecolor='none',markeredgecolor='blue', markersize=8)
                cb += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                cb_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='pink', markersize=2.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#39FF14', markersize=2.5)

        elif pitch_type == 'Slider':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='green', markersize=8)
                sl += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='green', markerfacecolor='none',markeredgecolor='green', markersize=8)
                sl += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                sl_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='pink', markersize=2.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#39FF14', markersize=2.5)

        elif pitch_type == 'Changeup':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='purple', markersize=8)
                ch += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='purple', markerfacecolor='none',markeredgecolor='purple', markersize=8)
                ch += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                ch_whiff += 1
            
            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='pink', markersize=2.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#39FF14', markersize=2.5)

        elif pitch_type == 'Splitter':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='black', markersize=8)
                spl += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='black', markerfacecolor='none',markeredgecolor='black', markersize=8)
                spl += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                spl_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='pink', markersize=2.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#39FF14', markersize=2.5)

    #calculate percentages
    fb_per = round((fb/total_pitches)*100,2)
    cb_per = round((cb/total_pitches)*100,2)
    sl_per = round((sl/total_pitches)*100,2)
    ch_per = round((ch/total_pitches)*100,2)
    spl_per = round((spl/total_pitches)*100,2)
    in_zone_per = round((in_zone/total_pitches)*100,2)
    out_of_zone_per = round((out_of_zone/total_pitches)*100,2)
    try:
        fb_whiff_per = round((fb_whiff/len(fb_data))*100,2)
    except:
        fb_whiff_per = 0

    try:
        cb_whiff_per = round((cb_whiff/len(cb_data))*100,2)
    except:
        cb_whiff_per = 0
    
    try:
        sl_whiff_per = round((sl_whiff/len(sl_data))*100,2)
    except:
        sl_whiff_per = 0

    try:
        ch_whiff_per = round((ch_whiff/len(ch_data))*100,2)
    except:
        ch_whiff_per = 0
    
    try:
        spl_whiff_per = round((spl_whiff/len(spl_data))*100,2)
    except:
        spl_whiff_per = 0

    fig.text(0.02,.60,
        f"Pitch Usage:\nFB: {fb_per}%\nCB: {cb_per}%\nSL: {sl_per}%\nCH: {ch_per}%\nSPL: {spl_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.02,0.02,
        f"In-Zone: {in_zone_per}%\nOut-Of-Zone: {out_of_zone_per}%",
        va='bottom',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.98,0.02,
        f"From Pitchers View",
        va='bottom',
        ha='right',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')

    fig.text(0.02,0.30,
        f"Whiff %:\nFB: {fb_whiff_per}%\nCB: {cb_whiff_per}%\nSL: {sl_whiff_per}%\nCH: {ch_whiff_per}%\nSPL: {spl_whiff_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    first, last = pitcher.split(" ")
    pitcher = f"{first}{last}"
    plt.savefig(f"{pitcher}_SeasonNumbers.pdf")

    plt.close(fig)

def plot_game_pitches(fig, ax, pitch_data, pitcher,yesterday_month, today_month, yesterdays_opponent):


    draw_strike_zone(ax)

    ax.plot([], [], 'o', color='orange', label='Fastball')
    ax.plot([], [], 'o', color='blue', label='Curveball')
    ax.plot([], [], 'o', color='green', label='Slider')
    ax.plot([], [], 'o', color='purple', label='Changeup')
    ax.plot([], [], 'o', color='black', label='Splitter')
    ax.plot([], [], '^', color='#FF6EC7', label='2-2 Count')
    ax.plot([], [], 'v', color='#00FFFF', label='1-1 Count')

    fig.legend(loc='upper left', fontsize=10,frameon=True)
    
    fb = 0
    cb = 0
    sl = 0
    ch = 0
    spl = 0
    in_zone = 0
    out_of_zone = 0
    fb_whiff = 0
    cb_whiff = 0
    sl_whiff = 0
    ch_whiff = 0
    spl_whiff = 0
    total_pitches = len(pitch_data)
    whiff_data = pitch_data[~pitch_data['PitchCall'].isin(['BallCalled','StrikeCalled','HitByPitch'])]
    fb_data = whiff_data[whiff_data['AutoPitchType'].isin(['Four-Seam','Sinker','2-Seam','Cutter'])]
    cb_data = whiff_data[whiff_data['AutoPitchType']=='Curveball']
    sl_data = whiff_data[whiff_data['AutoPitchType']=='Slider']
    ch_data = whiff_data[whiff_data['AutoPitchType']=='Changeup']
    spl_data = whiff_data[whiff_data['AutoPitchType']=='Splitter']
    
    for _, row in pitch_data.iterrows():

        side = row['PlateLocSide']
        height = row['PlateLocHeight']
        pitch_type = row['AutoPitchType']
        pitch_result = row['PitchCall']
        balls = row['Balls']
        strikes = row['Strikes']

    
        if pitch_type in ['Four-Seam','Sinker','2-Seam','Cutter']:
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='orange', markersize=11)
                fb += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='orange', markerfacecolor='none',markeredgecolor='orange', markersize=11)
                fb += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                fb_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='#FF6EC7', markersize=5.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#00FFFF', markersize=5.5)

        elif pitch_type == 'Curveball':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='blue', markersize=11)
                cb += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='blue', markerfacecolor='none',markeredgecolor='blue', markersize=11)
                cb += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                cb_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='#FF6EC7', markersize=5.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#00FFFF', markersize=5.5)

        elif pitch_type == 'Slider':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='green', markersize=11)
                sl += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='green', markerfacecolor='none',markeredgecolor='green', markersize=11)
                sl += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                sl_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='#FF6EC7', markersize=5.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#00FFFF', markersize=5.5)

        elif pitch_type == 'Changeup':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='purple', markersize=11)
                ch += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='purple', markerfacecolor='none',markeredgecolor='purple', markersize=11)
                ch += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                ch_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='#FF6EC7', markersize=5.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#00FFFF', markersize=5.5)

        elif pitch_type == 'Splitter':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                ax.plot(side, height, 'o', color='black', markersize=11)
                spl += 1
                in_zone += 1
            else:
                ax.plot(side, height, 'o', color='black', markerfacecolor='none',markeredgecolor='black', markersize=11)
                spl += 1
                out_of_zone += 1
            if pitch_result == 'StrikeSwinging':
                spl_whiff += 1

            if balls == 2 and strikes == 2:
                ax.plot(side, height, '^', color='#FF6EC7', markersize=5.5)
            if balls == 1 and strikes == 1:
                ax.plot(side, height, 'v', color='#00FFFF', markersize=5.5)

    #calculate percentages
    fb_per = round((fb/total_pitches)*100,2)
    cb_per = round((cb/total_pitches)*100,2)
    sl_per = round((sl/total_pitches)*100,2)
    ch_per = round((ch/total_pitches)*100,2)
    spl_per = round((spl/total_pitches)*100,2)
    in_zone_per = round((in_zone/total_pitches)*100,2)
    out_of_zone_per = round((out_of_zone/total_pitches)*100,2)
    try:
        fb_whiff_per = round((fb_whiff/len(fb_data))*100,2)
    except:
        fb_whiff_per = 0

    try:
        cb_whiff_per = round((cb_whiff/len(cb_data))*100,2)
    except:
        cb_whiff_per = 0
    
    try:
        sl_whiff_per = round((sl_whiff/len(sl_data))*100,2)
    except:
        sl_whiff_per = 0

    try:
        ch_whiff_per = round((ch_whiff/len(ch_data))*100,2)
    except:
        ch_whiff_per = 0
    
    try:
        spl_whiff_per = round((spl_whiff/len(spl_data))*100,2)
    except:
        spl_whiff_per = 0

    fig.text(0.02,.60,
        f"Pitch Usage:\nFB: {fb_per}%\nCB: {cb_per}%\nSL: {sl_per}%\nCH: {ch_per}%\nSPL: {spl_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.02,0.02,
        f"In-Zone: {in_zone_per}%\nOut-Of-Zone: {out_of_zone_per}%",
        va='bottom',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.98,0.02,
        f"From Pitchers View",
        va='bottom',
        ha='right',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')

    fig.text(0.02,0.30,
        f"Whiff %:\nFB: {fb_whiff_per}%\nCB: {cb_whiff_per}%\nSL: {sl_whiff_per}%\nCH: {ch_whiff_per}%\nSPL: {spl_whiff_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    print(pitcher)
    try:
        first, last = pitcher.split(" ")
        pitcher = f"{first}{last}"
    except:
        first, last = pitcher.split("  ")
        pitcher = f"{first}{last}"
    dir = Path(f"/Users/dannycoleman/desktop/valleycats/pitcher_plots/{pitcher}/{yesterday_month}_{yesterdays_opponent}")
    try:
        plt.savefig(f"{dir}/{pitcher}_vs_{yesterdays_opponent}.pdf")
    except:
        dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{dir}/{pitcher}_vs_{yesterdays_opponent}.pdf")

    plt.close(fig)

def plot_fb(fig, ax, pitch_data, pitcher, yesterday_month, today_month, yesterdays_opponent):

    draw_strike_zone(ax)

    ax.plot([], [], 'D', color='red', label='Whiff')
    ax.plot([], [], 'o', color='black', label='Non-Whiff')
    ax.plot([], [], 'o', markerfacecolor='none', markeredgecolor='#39FF14', label='No Strikes')
    ax.plot([], [], '<', color='#FF6EC7', label='1 Strike')
    ax.plot([], [], '>', color='#1F51FF', label='2 Strikes')

    fig.legend(loc='upper left', fontsize=10,frameon=True)
    
    in_zone = 0
    out_of_zone = 0
    fb_whiff = 0
    whiff_data = pitch_data[~pitch_data['PitchCall'].isin(['BallCalled','StrikeCalled','HitByPitch'])]
    fb_data = whiff_data[whiff_data['AutoPitchType'].isin(['Four-Seam','Sinker','2-Seam','Cutter'])]
    if fb_data.empty:
        return
    print("Loading FB....")
    for _, row in fb_data.iterrows():

        side = row['PlateLocSide']
        height = row['PlateLocHeight']
        pitch_type = row['AutoPitchType']
        pitch_result = row['PitchCall']
        strikes = row['Strikes']
    
        if pitch_type in ['Four-Seam','Sinker','2-Seam','Cutter']:
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                in_zone += 1
            else:
                out_of_zone += 1

            if pitch_result == 'StrikeSwinging':
                ax.plot(side, height, 'D', color='red', markersize=11)
                fb_whiff += 1
            else:
                ax.plot(side, height, 'o', color='black', markersize=11)

            if strikes == 2:
                ax.plot(side, height, '>', color='#1F51FF', markersize=5.5)
            elif strikes == 1:
                ax.plot(side, height, '<', color='#FF6EC7', markersize=5.5)
            elif strikes == 0:
                ax.plot(side, height, 'o', markerfacecolor='none', markeredgecolor='#39FF14', markersize=5.5)
        
    #calculate percentages
    try:
        fb_whiff_per = round((fb_whiff/len(fb_data))*100,2)
    except:
        fb_whiff_per = 0

    try:
        in_zone_per = round((in_zone/len(fb_data))*100,2)
    except:
        in_zone_per = 0

    out_of_zone_per = 100 - in_zone_per
    
    fig.text(0.02,0.02,
        f"In-Zone: {in_zone_per}%\nOut-Of-Zone: {out_of_zone_per}%",
        va='bottom',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.98,0.02,
        f"From Pitchers View",
        va='bottom',
        ha='right',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')

    fig.text(0.02,0.50,
        f"Whiff %:\nFB: {fb_whiff_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    try:
        first, last = pitcher.split(" ")
        pitcher = f"{first}{last}"
    except:
        first, last = pitcher.split("  ")
        pitcher = f"{first}{last}"
    dir = Path(f"/Users/dannycoleman/desktop/valleycats/pitcher_plots/{pitcher}/{yesterday_month}_{yesterdays_opponent}")
    try:
        plt.savefig(f"{dir}/{pitcher}_FB_Whiff.pdf")
    except:
        dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{dir}/{pitcher}_FB_Whiff.pdf")
    
    plt.close(fig)

def plot_cb(fig, ax, pitch_data, pitcher, yesterday_month, today_month, yesterdays_opponent):

    draw_strike_zone(ax)

    ax.plot([], [], 'D', color='red', label='Whiff')
    ax.plot([], [], 'o', color='black', label='Non-Whiff')
    ax.plot([], [], 'o', markerfacecolor='none', markeredgecolor='#39FF14', label='No Strikes')
    ax.plot([], [], '<', color='#FF6EC7', label='1 Strike')
    ax.plot([], [], '>', color='#1F51FF', label='2 Strikes')

    fig.legend(loc='upper left', fontsize=10,frameon=True)
    
    in_zone = 0
    out_of_zone = 0
    cb_whiff = 0
    whiff_data = pitch_data[~pitch_data['PitchCall'].isin(['BallCalled','StrikeCalled','HitByPitch'])]
    cb_data = whiff_data[whiff_data['AutoPitchType']=='Curveball']
    if cb_data.empty:
        return
    print("Loading CB....")
    for _, row in cb_data.iterrows():

        side = row['PlateLocSide']
        height = row['PlateLocHeight']
        pitch_type = row['AutoPitchType']
        pitch_result = row['PitchCall']
        strikes = row['Strikes']
    
        if pitch_type == 'Curveball':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                in_zone += 1
            else:
                out_of_zone += 1

            if pitch_result == 'StrikeSwinging':
                ax.plot(side, height, 'D', color='red', markersize=11)
                cb_whiff += 1
            else:
                ax.plot(side, height, 'o', color='black', markersize=11)

            if strikes == 2:
                ax.plot(side, height, '>', color='#1F51FF', markersize=5.5)
            elif strikes == 1:
                ax.plot(side, height, '<', color='#FF6EC7', markersize=5.5)
            elif strikes == 0:
                ax.plot(side, height, 'o', markerfacecolor='none', markeredgecolor='#39FF14', markersize=5.5)

    #calculate percentages
    try:
        cb_whiff_per = round((cb_whiff/len(cb_data))*100,2)
    except:
        cb_whiff_per = 0

    try:
        in_zone_per = round((in_zone/len(cb_data))*100,2)
    except:
        in_zone_per = 0

    out_of_zone_per = 100 - in_zone_per
    
    fig.text(0.02,0.02,
        f"In-Zone: {in_zone_per}%\nOut-Of-Zone: {out_of_zone_per}%",
        va='bottom',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.98,0.02,
        f"From Pitchers View",
        va='bottom',
        ha='right',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')

    fig.text(0.02,0.50,
        f"Whiff %:\nCB: {cb_whiff_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    try:
        first, last = pitcher.split(" ")
        pitcher = f"{first}{last}"
    except:
        first, last = pitcher.split("  ")
        pitcher = f"{first}{last}"

    dir = Path(f"/Users/dannycoleman/desktop/valleycats/pitcher_plots/{pitcher}/{yesterday_month}_{yesterdays_opponent}")
    try:
        plt.savefig(f"{dir}/{pitcher}_CB_Whiff.pdf")
    except:
        dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{dir}/{pitcher}_CB_Whiff.pdf")
    
    plt.close(fig)

def plot_sl(fig, ax, pitch_data, pitcher, yesterday_month, today_month, yesterdays_opponent):

    draw_strike_zone(ax)

    ax.plot([], [], 'D', color='red', label='Whiff')
    ax.plot([], [], 'o', color='black', label='Non-Whiff')
    ax.plot([], [], 'o', markerfacecolor='none', markeredgecolor='#39FF14', label='No Strikes')
    ax.plot([], [], '<', color='#FF6EC7', label='1 Strike')
    ax.plot([], [], '>', color='#1F51FF', label='2 Strikes')

    fig.legend(loc='upper left', fontsize=10,frameon=True)
    
    in_zone = 0
    out_of_zone = 0
    sl_whiff = 0
    whiff_data = pitch_data[~pitch_data['PitchCall'].isin(['BallCalled','StrikeCalled','HitByPitch'])]
    sl_data = whiff_data[whiff_data['AutoPitchType']=='Slider']
    if sl_data.empty:
        return
    print("Loading SL....")
    for _, row in sl_data.iterrows():

        side = row['PlateLocSide']
        height = row['PlateLocHeight']
        pitch_type = row['AutoPitchType']
        pitch_result = row['PitchCall']
        strikes = row['Strikes']
    
        if pitch_type == 'Slider':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                in_zone += 1
            else:
                out_of_zone += 1

            if pitch_result == 'StrikeSwinging':
                ax.plot(side, height, 'D', color='red', markersize=11)
                sl_whiff += 1
            else:
                ax.plot(side, height, 'o', color='black', markersize=11)

            if strikes == 2:
                ax.plot(side, height, '>', color='#1F51FF', markersize=5.5)
            elif strikes == 1:
                ax.plot(side, height, '<', color='#FF6EC7', markersize=5.5)
            elif strikes == 0:
                ax.plot(side, height, 'o', markerfacecolor='none', markeredgecolor='#39FF14', markersize=5.5)

    #calculate percentages
    try:
        sl_whiff_per = round((sl_whiff/len(sl_data))*100,2)
    except:
        sl_whiff_per = 0

    try:
        in_zone_per = round((in_zone/len(sl_data))*100,2)
    except:
        in_zone_per = 0

    out_of_zone_per = 100 - in_zone_per
    
    fig.text(0.02,0.02,
        f"In-Zone: {in_zone_per}%\nOut-Of-Zone: {out_of_zone_per}%",
        va='bottom',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.98,0.02,
        f"From Pitchers View",
        va='bottom',
        ha='right',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')

    fig.text(0.02,0.50,
        f"Whiff %:\nSL: {sl_whiff_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    try:
        first, last = pitcher.split(" ")
        pitcher = f"{first}{last}"
    except:
        first, last = pitcher.split("  ")
        pitcher = f"{first}{last}"

    dir = Path(f"/Users/dannycoleman/desktop/valleycats/pitcher_plots/{pitcher}/{yesterday_month}_{yesterdays_opponent}")
    try:
        plt.savefig(f"{dir}/{pitcher}_SL_Whiff.pdf")
    except:
        dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{dir}/{pitcher}_SL_Whiff.pdf")

    plt.close(fig)

def plot_ch(fig, ax, pitch_data, pitcher, yesterday_month, today_month, yesterdays_opponent):

    draw_strike_zone(ax)

    ax.plot([], [], 'D', color='red', label='Whiff')
    ax.plot([], [], 'o', color='black', label='Non-Whiff')
    ax.plot([], [], 'o', markerfacecolor='none', markeredgecolor='#39FF14', label='No Strikes')
    ax.plot([], [], '<', color='#FF6EC7', label='1 Strike')
    ax.plot([], [], '>', color='#1F51FF', label='2 Strikes')

    fig.legend(loc='upper left', fontsize=10,frameon=True)
    
    in_zone = 0
    out_of_zone = 0
    ch_whiff = 0
    whiff_data = pitch_data[~pitch_data['PitchCall'].isin(['BallCalled','StrikeCalled','HitByPitch'])]
    ch_data = whiff_data[whiff_data['AutoPitchType']=='Changeup']
    if ch_data.empty:
        return
    print("Loading CH....")
    for _, row in ch_data.iterrows():

        side = row['PlateLocSide']
        height = row['PlateLocHeight']
        pitch_type = row['AutoPitchType']
        pitch_result = row['PitchCall']
        strikes = row['Strikes']
    
        if pitch_type == 'Changeup':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                in_zone += 1
            else:
                out_of_zone += 1

            if pitch_result == 'StrikeSwinging':
                ax.plot(side, height, 'D', color='red', markersize=11)
                ch_whiff += 1
            else:
                ax.plot(side, height, 'o', color='black', markersize=11)

            if strikes == 2:
                ax.plot(side, height, '>', color='#1F51FF', markersize=5.5)
            elif strikes == 1:
                ax.plot(side, height, '<', color='#FF6EC7', markersize=5.5)
            elif strikes == 0:
                ax.plot(side, height, 'o', markerfacecolor='none', markeredgecolor='#39FF14', markersize=5.5)

    #calculate percentages
    try:
        ch_whiff_per = round((ch_whiff/len(ch_data))*100,2)
    except:
        ch_whiff_per = 0

    try:
        in_zone_per = round((in_zone/len(ch_data))*100,2)
    except:
        in_zone_per = 0

    out_of_zone_per = 100 - in_zone_per
    
    fig.text(0.02,0.02,
        f"In-Zone: {in_zone_per}%\nOut-Of-Zone: {out_of_zone_per}%",
        va='bottom',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.98,0.02,
        f"From Pitchers View",
        va='bottom',
        ha='right',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')

    fig.text(0.02,0.50,
        f"Whiff %:\nCH: {ch_whiff_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    try:
        first, last = pitcher.split(" ")
        pitcher = f"{first}{last}"
    except:
        first, last = pitcher.split("  ")
        pitcher = f"{first}{last}"

    dir = Path(f"/Users/dannycoleman/desktop/valleycats/pitcher_plots/{pitcher}/{yesterday_month}_{yesterdays_opponent}")
    try:
        plt.savefig(f"{dir}/{pitcher}_CH_Whiff.pdf")
    except:
        dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{dir}/{pitcher}_CH_Whiff.pdf")

    plt.close(fig)

def plot_spl(fig, ax, pitch_data, pitcher, yesterday_month, today_month, yesterdays_opponent):

    draw_strike_zone(ax)

    ax.plot([], [], 'D', color='red', label='Whiff')
    ax.plot([], [], 'o', color='black', label='Non-Whiff')
    ax.plot([], [], 'o', markerfacecolor='none', markeredgecolor='#39FF14', label='No Strikes')
    ax.plot([], [], '<', color='#FF6EC7', label='1 Strike')
    ax.plot([], [], '>', color='#1F51FF', label='2 Strikes')

    fig.legend(loc='upper left', fontsize=10,frameon=True)
    
    in_zone = 0
    out_of_zone = 0
    spl_whiff = 0
    whiff_data = pitch_data[~pitch_data['PitchCall'].isin(['BallCalled','StrikeCalled','HitByPitch'])]
    spl_data = whiff_data[whiff_data['AutoPitchType']=='Splitter']
    if spl_data.empty:
        return
    print("Loading SPL....")
    for _, row in spl_data.iterrows():

        side = row['PlateLocSide']
        height = row['PlateLocHeight']
        pitch_type = row['AutoPitchType']
        pitch_result = row['PitchCall']
        strikes = row['Strikes']
    
        if pitch_type == 'Splitter':
            if -.708 <= side <= .708 and 1.5 <= height <= 3.5:
                in_zone += 1
            else:
                out_of_zone += 1

            if pitch_result == 'StrikeSwinging':
                ax.plot(side, height, 'D', color='red', markersize=11)
                spl_whiff += 1
            else:
                ax.plot(side, height, 'o', color='black', markersize=11)

            if strikes == 2:
                ax.plot(side, height, '>', color='#1F51FF', markersize=5.5)
            elif strikes == 1:
                ax.plot(side, height, '<', color='#FF6EC7', markersize=5.5)
            elif strikes == 0:
                ax.plot(side, height, 'o', markerfacecolor='none', markeredgecolor='#39FF14', markersize=5.5)

    #calculate percentages
    try:
        spl_whiff_per = round((spl_whiff/len(spl_data))*100,2)
    except:
        spl_whiff_per = 0

    try:
        in_zone_per = round((in_zone/len(spl_data))*100,2)
    except:
        in_zone_per = 0

    out_of_zone_per = 100 - in_zone_per
    
    fig.text(0.02,0.02,
        f"In-Zone: {in_zone_per}%\nOut-Of-Zone: {out_of_zone_per}%",
        va='bottom',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    fig.text(0.98,0.02,
        f"From Pitchers View",
        va='bottom',
        ha='right',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')

    fig.text(0.02,0.50,
        f"Whiff %:\nSPL: {spl_whiff_per}%",
        va='center',
        ha='left',
        fontsize=15,
        fontname='Arial',
        fontweight='bold',
        bbox=dict(facecolor='white',edgecolor='gray',boxstyle='round'),
        color='black')
    
    try:
        first, last = pitcher.split(" ")
        pitcher = f"{first}{last}"
    except:
        first, last = pitcher.split("  ")
        pitcher = f"{first}{last}"
        
    dir = Path(f"/Users/dannycoleman/desktop/valleycats/pitcher_plots{pitcher}/{yesterday_month}_{yesterdays_opponent}")
    try:
        plt.savefig(f"{dir}/{pitcher}_SPL_Whiff.pdf")
    except:
        dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{dir}/{pitcher}_SPL_Whiff.pdf")

    plt.close(fig)

def draw_strike_zone(ax):
    #this sets the boundry for a visible pitch, if outside this boundry you will not see it
    ax.set_xlim(-3,3)
    ax.set_ylim(0,5)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    #creates the outer boundry of strike zone (MLB size)
    ax.add_patch(plt.Rectangle((-0.708, 1.5), 1.416, 2, fill=False, color='Black', linewidth=2))
    col1_x = -0.708 + 1.416/3
    col2_x = -0.708 + 2*1.416/3
    #lines below create the 9-box grid inside the strikezone
    ax.plot([col1_x, col1_x], [1.5, 3.5], color='black', linewidth=1)
    ax.plot([col2_x, col2_x], [1.5, 3.5], color='black', linewidth=1)
    row1_y = 1.5 + 2/3
    row2_y = 1.5 + 2*2/3
    ax.plot([-0.708, 0.708], [row1_y, row1_y], color='black', linewidth=1)
    ax.plot([-0.708, 0.708], [row2_y, row2_y], color='black', linewidth=1)

    
def main():
    #------------------------------------------------------------#

    # --- Import All Necessary Data --- #
    today_full = datetime.today().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1))
    yesterday_full = yesterday.strftime("%Y-%m-%d")
    yesterday_month = yesterday.strftime("%m-%d")

    today_month = datetime.today().strftime("%m-%d")
    schedule = pd.read_csv("/Users/dannycoleman/desktop/valleycats/schedule/schedule.csv")
    todays_game = schedule[schedule['date']==today_full]
    yesterdays_game = schedule[schedule['date']==yesterday_full]

    try:
        todays_opponent = todays_game.iloc[0]['opponent']
    except:
        print("No game today")
    
    try:
        yesterdays_opponent = yesterdays_game.iloc[0]['opponent']
    except:
        print("No game yesterday")
    game_today = input("Is this program running day of game occuring?(y/n): ").strip().lower()

    if game_today == 'no' or game_today == 'n':
        game_data = pd.read_csv(f"/Users/dannycoleman/desktop/valleycats/trackmancsv/{yesterdays_opponent}-{yesterday_month}.csv")

    elif game_today == 'yes' or game_today == 'y':
        game_data = pd.read_csv(f"/Users/dannycoleman/desktop/valleycats/trackmancsv/{todays_opponent}-{today_month}.csv")
    
    else:
        print("Must be (y)es or (n)o! Try again, Bye")
        

    pitch_data = game_data[game_data['PitcherTeam']=='TRI_VAL']
    bat_data = game_data[game_data['BatterTeam']=='TRI_VAL']
    pitch_data = pitch_data.dropna(subset=['PlateLocSide','PlateLocHeight'])
    dir_path = "/Users/dannycoleman/desktop/valleycats/trackmancsv/"
    season_csv = glob.glob(os.path.join(dir_path, "*.csv"))
    all_data = []
    for csv in season_csv:
        game = pd.read_csv(csv)
        all_data.append(game)
    season_data = pd.concat(all_data, ignore_index=True)
    season_data = season_data[season_data['PitcherTeam']=='TRI_VAL']
    unique_pitchers = season_data['Pitcher'].unique()
    
    #------------------------------------------------------------#

    # --- Individual Game Pitching Report --- #
    unique_pitchers = pitch_data['Pitcher'].unique()
    for pitcher in unique_pitchers:
        pitcher_data = pitch_data[pitch_data['Pitcher']==pitcher]
        fig, ax = plt.subplots(figsize=(7,7), constrained_layout=True, facecolor='whitesmoke')
        fig.suptitle("Pitcher Game Report", fontweight='bold', fontsize=16, x=.5,y=.98, ha='center')
        last, first = pitcher.split(", ")
        pitcher = f"{first} {last}"
        ax.set_title(f"{pitcher} vs {yesterdays_opponent} | {yesterday_month}", fontfamily='Arial', pad=8, loc='center')
        plot_game_pitches(fig, ax, pitcher_data, pitcher, yesterday_month, today_month, yesterdays_opponent)

    #------------------------------------------------------------#
    """
    # --- Individual Season Pitching Report --- #

    for pitcher in unique_pitchers:
        pitcher_season_data = season_data[season_data['Pitcher']==pitcher]
        fig, ax = plt.subplots(figsize=(7,7), facecolor='lightgray', constrained_layout=True)
        fig.suptitle("Season Pitcher Data", fontweight='bold',fontsize=16, x=.5, y=.98, ha='center')
        last, first = pitcher.split(", ")
        pitcher = f"{first} {last}"
        print(pitcher)
        ax.set_title(f"{pitcher} as of {today_month}", fontfamily='Arial', pad=45, loc='center')
        plot_season_pitches(fig, ax, pitcher_season_data, pitcher)

    #------------------------------------------------------------#
    """
    # --- Individual Whiff Rates by Pitch (Season) --- #

    # --- FB --- #
    #using filtered data from above
    for pitcher in unique_pitchers:
        pitcher_data = pitch_data[pitch_data['Pitcher']==pitcher]
        fig, ax = plt.subplots(figsize=(7,7), constrained_layout=True, facecolor='whitesmoke')
        fig.suptitle("FB Whiff % (Season)", fontweight='bold',fontsize=16, x=.5, y=.98, ha='center')
        last, first = pitcher.split(", ")
        pitcher = f"{first} {last}"
        ax.set_title(f"{pitcher} as of {today_month}", fontfamily='Arial', pad=10, loc='center')
        plot_fb(fig, ax, pitcher_data, pitcher, yesterday_month, today_month, yesterdays_opponent)
        
    # --- CB --- #
    for pitcher in unique_pitchers:
        pitcher_data = pitch_data[pitch_data['Pitcher']==pitcher]
        fig, ax = plt.subplots(figsize=(7,7), constrained_layout=True, facecolor='whitesmoke')
        fig.suptitle("CB Whiff % (Season)", fontweight='bold',fontsize=16, x=.5, y=.98, ha='center')
        last, first = pitcher.split(", ")
        pitcher = f"{first} {last}"
        ax.set_title(f"{pitcher} as of {today_month}", fontfamily='Arial', pad=10, loc='center')
        plot_cb(fig, ax, pitcher_data, pitcher, yesterday_month, today_month, yesterdays_opponent)
    
    # --- SL --- #
    for pitcher in unique_pitchers:
        pitcher_data = pitch_data[pitch_data['Pitcher']==pitcher]
        fig, ax = plt.subplots(figsize=(7,7), constrained_layout=True, facecolor='whitesmoke')
        fig.suptitle("SL Whiff % (Season)", fontweight='bold',fontsize=16, x=.5, y=.98, ha='center')
        last, first = pitcher.split(", ")
        pitcher = f"{first} {last}"
        ax.set_title(f"{pitcher} as of {today_month}", fontfamily='Arial', pad=10, loc='center')
        plot_sl(fig, ax, pitcher_data, pitcher, yesterday_month, today_month, yesterdays_opponent)

    # --- CH --- #
    for pitcher in unique_pitchers:
        pitcher_data = pitch_data[pitch_data['Pitcher']==pitcher]
        fig, ax = plt.subplots(figsize=(7,7), constrained_layout=True, facecolor='whitesmoke')
        fig.suptitle("CH Whiff % (Season)", fontweight='bold',fontsize=16, x=.5, y=.98, ha='center')
        last, first = pitcher.split(", ")
        pitcher = f"{first} {last}"
        ax.set_title(f"{pitcher} as of {today_month}", fontfamily='Arial', pad=10, loc='center')
        plot_ch(fig, ax, pitcher_data, pitcher, yesterday_month, today_month, yesterdays_opponent)

    # --- SPL --- #
    for pitcher in unique_pitchers:
        pitcher_data = pitch_data[pitch_data['Pitcher']==pitcher]
        fig, ax = plt.subplots(figsize=(7,7), constrained_layout=True, facecolor='whitesmoke')
        fig.suptitle("SPL Whiff % (Season)", fontweight='bold',fontsize=16, x=.5, y=.98, ha='center')
        last, first = pitcher.split(", ")
        pitcher = f"{first} {last}"
        ax.set_title(f"{pitcher} as of {today_month}", fontfamily='Arial', pad=10, loc='center')
        plot_spl(fig, ax, pitcher_data, pitcher, yesterday_month, today_month, yesterdays_opponent)

if __name__ == '__main__':
    main()


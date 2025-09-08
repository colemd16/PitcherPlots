from pathlib import Path
team_dir = None
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import glob
from ftplib import FTP
import os

def normalize_name(name):
    name = str(name).strip().lower()
    name = name.replace("-", " ").replace(".", "").replace(",", "")
    name = " ".join(name.split()) 
    return name.title()  

def draw_field(ax):
    # Constants
    fence_radius = 400
    mound_radius = 9  # typical mound radius

    # Draw foul lines (solid, stopping at the fence)
    ax.plot([0, fence_radius * np.cos(np.radians(45))],
            [0, fence_radius * np.sin(np.radians(45))],
            color='gray', linewidth=1.5)
    ax.plot([0, fence_radius * np.cos(np.radians(135))],
            [0, fence_radius * np.sin(np.radians(135))],
            color='gray', linewidth=1.5)

    # Draw outfield fence arc (from left to right field)
    theta = np.linspace(np.radians(135), np.radians(45), 300)
    arc_x = fence_radius * np.cos(theta)
    arc_y = fence_radius * np.sin(theta)
    ax.plot(arc_x, arc_y, color='lightgray')

    # Outfield grass arc (just beyond bases)
    grass_radius = 160  # typical outfield grass starts ~160ft from home
    grass_theta = np.linspace(np.radians(45), np.radians(135), 150)
    grass_x = grass_radius * np.cos(grass_theta)
    grass_y = grass_radius * np.sin(grass_theta)
    ax.plot(grass_x, grass_y, color='green', linewidth=2)

    # Mound circle
    mound = plt.Circle((0, 60.6), mound_radius, color='saddlebrown', fill=True, alpha=0.6)
    ax.add_patch(mound)

    # Bases
    base_size = 5
    ax.scatter(0, 0, color='brown', s=20, label='Home')  # Home plate
    ax.add_patch(plt.Rectangle((90 - base_size/2, 90 - base_size/2), base_size, base_size, color='brown'))    # First base
    ax.add_patch(plt.Rectangle((0 - base_size/2, 127.28 - base_size/2), base_size, base_size, color='brown'))    # Second base
    ax.add_patch(plt.Rectangle((-90 - base_size/2, 90 - base_size/2), base_size, base_size, color='brown'))   # Third base

from matplotlib.patches import Patch

def plot(x, y, color, fig, ax, player, all_angles, textstr=None, handedness=None):
    # Set very light gray background for both figure and axis
    fig.patch.set_facecolor('#f2f2f2')  # very light gray background
    ax.set_facecolor('#f2f2f2')

    # Plot batted ball point
    ax.scatter(x, y, color=color)

    # Full field view
    ax.set_xlim(-300, 300)
    ax.set_ylim(0, 400)
    ax.axis('off')

    # Set title
    title = f"{player}"
    ax.set_title(title, fontsize=16, fontweight='bold', fontname='serif', pad=30)

    # Custom legend
    legend_elements = [
        Patch(facecolor='orange', label='LineDrive'),
        Patch(facecolor='saddlebrown', label='GroundBall'),
        Patch(facecolor='skyblue', label='FlyBall'),
        Patch(facecolor='plum', label='Popup'),
        Patch(facecolor='green', label='Bunt'),
        Patch(facecolor='dimgray', label='Other')
    ]
    ax.legend(handles=legend_elements, loc='lower right', title='Hit Type', fontsize=8)

    if textstr:
        ax.text(
            -290, 10, textstr, fontsize=10,
            bbox=dict(
                facecolor='white',
                edgecolor='gray',
                boxstyle='round,pad=0.5',
                alpha=0.9
            )
        )

    safe_player = str(player).replace(" ", "_").replace("/", "-").replace(",", "")
    file_path = team_dir / f"{safe_player}.pdf"
    plt.savefig(file_path)

def filter_result(hit_type):
    if hit_type == 'LineDrive':
        return 'orange'
    elif hit_type == 'GroundBall':
        return 'saddlebrown'
    elif hit_type == 'FlyBall':
        return 'skyblue'
    elif hit_type == 'Popup':
        return 'plum'
    elif hit_type == 'Bunt':
        return 'green'
    else:
        return 'dimgray'  # Unknown or other types


    plt.show()
def name_to_code(user_input):
    mapping = {
        "Quebec": "QUE_CAP",
        "Down East": "DOW_EAS1",
        "Ottawa": "OTT_TIT",
        "Florence": "FLO_Y'A",
        "Lake Erie": "LAK_ERI24",
        "Gateway": "GAT_GRI",
        "Brockton": "NEW_ENG23",
        "Sussex": "SUS_COU1",
        "New Jersey": "NEW_JER6",
        "Trois-Rivieres": "TRO_AIG",
        "New York": "NEW_YOR13",
        "Joliett": "JOL_SLA"
    }
    return mapping.get(user_input, None)

def main():

    schedule = pd.read_csv("/Users/dannycoleman/desktop/valleycats/schedule/schedule.csv")
    team_options = {
        "1": "Quebec",
        "2": "Down East",
        "3": "Ottawa",
        "4": "Florence",
        "5": "Lake Erie",
        "6": "Gateway",
        "7": "Brockton",
        "8": "Sussex",
        "9": "New Jersey",
        "10": "Trois-Rivieres",
        "11": "New York",
        "12": "Joliett"
    }

    print("Select a team by number:")
    for num, name in team_options.items():
        print(f"{num}. {name}")

    selection = input("Enter the number of the team you want to get player plots from: ")
    user_team = team_options.get(selection)
    if not user_team:
        print("Invalid selection.")
        return
    team_code = name_to_code(user_team)
    
    global team_dir
    team_dir = Path(f"/Users/dannycoleman/desktop/valleycats/spraycharts/{user_team}")
    team_dir.mkdir(parents=True, exist_ok=True)
    
    dir_path = "/Users/dannycoleman/desktop/valleycats/python/spraycharts/opposing_csv"
    season_csv = glob.glob(os.path.join(dir_path, "*.csv"))
    all_data = []
    for csv in season_csv:
        game = pd.read_csv(csv)
        if game.empty or game.isna().all().all():
            continue

        if "Batter" not in game.columns:
            continue  # Skip files that don’t have a Batter column

        game["Batter"] = game["Batter"].apply(normalize_name)
        all_data.append(game)
    
    season_data = pd.concat(all_data, ignore_index=True)
    season_data = season_data[
        (season_data['BatterTeam'] == team_code) &
        (season_data['PitchCall'] == 'InPlay')
    ]
    quebec_hitting_data = season_data
    
    for player, group in quebec_hitting_data.groupby('Batter'):
        for pitcher_side in ['Left', 'Right']:
            split_group = group[group['PitcherThrows'] == pitcher_side]
            if split_group.empty:
                continue

            label = 'LHP' if pitcher_side == 'Left' else 'RHP'
            name_parts = player.split()
            player_name = f"{name_parts[1]} {name_parts[0]}" if len(name_parts) == 2 else player
            fig, ax = plt.subplots(figsize=(8, 8))
            draw_field(ax)
            all_angles = []

            def calculate_spray_stats(df):
                left = sum(df['Direction'] < 0)
                right = sum(df['Direction'] > 0)
                total = left + right
                left_pct = round(100 * left / total, 1) if total > 0 else 0
                right_pct = round(100 * right / total, 1) if total > 0 else 0
                return left_pct, right_pct

            gb_bunt = split_group[split_group['TaggedHitType'].isin(['GroundBall', 'Bunt']) & split_group['Direction'].notna()]
            other = split_group[~split_group['TaggedHitType'].isin(['GroundBall', 'Bunt']) & split_group['Direction'].notna()]

            gb_left_pct, gb_right_pct = calculate_spray_stats(gb_bunt)
            other_left_pct, other_right_pct = calculate_spray_stats(other)

            textstr = (
                f'$\\bf{{On\\ the\\ Ground}}$:\nLeft: {gb_left_pct}%\nRight: {gb_right_pct}%\n'
                f'$\\bf{{In\\ the\\ Air}}$:\nLeft: {other_left_pct}%\nRight: {other_right_pct}%'
            )

            handedness = split_group['BatterSide'].iloc[0] if 'BatterSide' in split_group.columns else None
            if handedness == 'Left':
                handedness = 'LHB'
            elif handedness == 'Right':
                handedness = 'RHB'

            for _, row in split_group.iterrows():
                if pd.isna(row['Distance']) or pd.isna(row['Direction']):
                    continue

                radians = np.radians(row['Direction'])
                x = row['Distance'] * np.sin(radians)
                y = row['Distance'] * np.cos(radians)
                color = filter_result(row.get('TaggedHitType'))
                all_angles.append(row['Direction'])
                plot(x, y, color, fig, ax, f"{handedness} {player_name} (vs {label})", all_angles, textstr, handedness)
            plt.close(fig)
        
main()
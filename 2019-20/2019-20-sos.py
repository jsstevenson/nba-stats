import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import team_colors

def sos_raw():
    wl = pd.read_csv('2019-20-wl.csv')
    wl = wl.set_index('team')
    wl['pct'] = wl.apply(lambda row: row['w']/(row['w'] + row['l']), axis=1)
    sched = pd.read_csv('2019-20-rem-sch.csv')
    sched = sched.set_index('team')

    # sos = average win pct of opponents
    sos = sched.apply(lambda team: sum([wl.loc[opp]['pct'] for opp in team])/8, axis=1)
    sos = pd.DataFrame(sos, columns=["sos"])
    sos['teams_index'] = [x.capitalize() for x in sos.index.values]
    sos = sos.set_index('teams_index')

    colors = sns.color_palette([team_colors.nba_colors[team.lower()] for team in sos.index.values])
    chart = sns.barplot(x=sos.index.values, y=sos['sos'], palette=colors)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45,
                          horizontalalignment='right', fontweight='light')
    chart.set(xlabel="Team", ylabel="Avg Opp Win %")
    chart.set_title("NBA Seeding Games Strength of Schedule")
    plt.tight_layout()
    plt.savefig('sos_wl.png')
    plt.show()

    # diff b/w self wl and opp wl
    wl['opp-pct'] = wl.apply(lambda team: sos.loc[team.name.capitalize()], axis=1)
    wl['diff'] = wl.apply(lambda row: row['pct'] - row['opp-pct'], axis=1)
    wl_diff = wl.sort_values('diff', ascending=False)

    colors_2 = sns.color_palette([team_colors.nba_colors[team.lower()] for team in wl_diff.index.values])
    chart = sns.barplot(x=[x.capitalize() for x in wl_diff.index.values], y=wl_diff['diff'], palette=colors_2)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45,horizontalalignment='right', fontweight='light')
    chart.set(xlabel="Team", ylabel="Win % - Avg Opp Win %")
    chart.set_title("Team Win % Vs Opponent Win %")
    plt.tight_layout()
    plt.savefig('sos_wl_diff.png')
    plt.show()


def main():
    sos_raw()


if __name__ == '__main__':
    main()

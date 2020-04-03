
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd

def plot_gmean_rates(df_in, title, filename=False):
    df_in['growth_rate']= df_in.cases / df_in.cases.shift(1)
    df_in['avg_growth'] = df_in.growth_rate.rolling(5).apply(stats.gmean)
    df_in['avg_growth'] = df_in['avg_growth'].shift(-2)
    df_in['time'] = pd.to_datetime(df_in['date'], format='%Y-%m-%d')
    df_in.set_index(['time'], inplace=True)
    df_in[['avg_growth', 'growth_rate']].plot()
    plt.title(title)
    if not filename:
        plt.show()
    else:
        plt.savefig(filename)


if __name__ == '__main__':
    title_beginning = 'Geometric Moving Avg for COVID-19 Daily Case Growth Rate in '
    dates_peru = pd.date_range(start='3/07/2020', end='4/02/2020')
    peru_cases = [6, 7, 9, 11, 17, 22, 38, 43, 71, 86, 117,
                145, 234, 263, 318, 363, 395, 416, 480, 580, 635, 671, 852,
                  950, 1065, 1323, 1414]
    peru_df = pd.DataFrame({'date': dates_peru, 'cases': peru_cases})

    df = pd.read_csv('./us-states.csv')
    plot_gmean_rates(peru_df, title_beginning + 'Peru',
                     filename='./Plots/Peru.png')

    usa_cases = df[df['date'] >= '2020-02-15'].groupby('date')['cases'].sum()
    usa_cases = pd.DataFrame({'date':usa_cases.index, 'cases':usa_cases.values})
    plot_gmean_rates(usa_cases, title_beginning + 'USA',
                     filename='./Plots/USA.png')

    df = df[df['date'] >= '2020-02-23']
    for state in df['state'].unique():
        title = title_beginning + state
        plot_gmean_rates(df[df['state']==state], title,
                        filename='./Plots/' + state + '.png')

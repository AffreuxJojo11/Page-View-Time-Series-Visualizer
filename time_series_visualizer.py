import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date']).set_index('date')

# Clean data
df = df.loc[(df['value']<=df['value'].quantile(0.975)) & (df['value']>=df['value'].quantile(0.025))]

def draw_line_plot():
    # Draw line plot

    fig, axes = plt.subplots(figsize=(19, 6))
    axes.plot(pd.to_datetime(df.index), df['value'],color='red')
    axes.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    date_form = mdates.DateFormatter("%Y-%m")
    axes.xaxis.set_major_formatter(date_form)
    axes.tick_params(axis="x", labelrotation= 0)
    axes.xaxis.set_ticks(['2016-07-01','2017-01-01','2017-07-01','2018-01-01','2018-07-01',
                      '2019-01-01','2019-07-01','2020-01-01'])



    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby([df.index.year,df.index.month_name()]).mean()
    df_bar.index.names=['Years','Months']
    df_bar.reset_index(inplace=True)
    df_bar.rename(columns={'value':'Average Page Views'}, inplace=True)

    # Draw bar plot

    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    df_bar['Months'] = pd.Categorical(df_bar['Months'], categories=months, ordered=True)

    df_bar.sort_values(by=['Months'], inplace=True)


    # Draw bar plot
    fig, axes = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df_bar, x='Years', y="Average Page Views",hue="Months", palette=sns.color_palette())
    plt.legend(loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_box['month'] = pd.Categorical(df_box['month'], categories=months, ordered=True)

    # Draw box plots (using Seaborn)
    plot_objects = plt.subplots(ncols=2, figsize=(14, 6))
    fig, (ax1, ax2) = plot_objects
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    sns.boxplot(data=df_box, x='year', y='value', ax=ax1)
    sns.boxplot(data=df_box, x='month', y='value', ax=ax2)
    ax1.set_ylabel('Page Views')
    ax2.set_ylabel('Page Views')
    ax1.set_xlabel('Year')
    ax2.set_xlabel('Month')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

from datetime import date
import click
import pygdg.events as e
import pygdg.features as f

# events

DEFAULT_EVENTS_DATE=str(date.today())
DEFAULT_EVENTS_PLAYERS=10
DEFAULT_EVENTS_DAYS=7

# features

DEFAULT_FEATURES_CHURN_DAYS=5
DEFAULT_FEATURES_LAST_MINUTES=0
DEFAULT_FEATURES_LAST_HOURS=0
DEFAULT_FEATURES_LAST_DAYS=7
DEFAULT_FEATURES_LAST_WEEKS=3
DEFAULT_FEATURES_LAST_MONTHS=2

# common

DEFAULT_SEED=0
DEFAULT_PLOT=False
DEFAULT_DEBUG=False

@click.group()
@click.version_option()
def main():
    pass

@main.command()
@click.option('--date', type=click.DateTime(formats=["%Y-%m-%d"]), default=DEFAULT_EVENTS_DATE, help='The acquisition starting date')
@click.option('--players', default=DEFAULT_EVENTS_PLAYERS, help='The number of daily acquired players')
@click.option('--days', default=DEFAULT_EVENTS_DAYS, help='The number of acquisition days')
@click.option('--seed', default=DEFAULT_SEED, help='The random seed')
@click.option('--plot/--no-plot', default=DEFAULT_PLOT, help='The plot flag')
@click.option('--debug/--no-debug', default=DEFAULT_DEBUG, help='The debug flag')
@click.argument('filename', default='events')
def events(filename, date, players, days, seed, plot, debug):
    e.generate(filename, date, players, days, seed, plot, debug)

@main.command()
@click.option('--churn-days', default=DEFAULT_FEATURES_CHURN_DAYS, help='The number of inactivity days to be flagged as churn')
@click.option('--last-minutes', default=DEFAULT_FEATURES_LAST_MINUTES, help='The number of minutes to sample before last event date')
@click.option('--last-hours', default=DEFAULT_FEATURES_LAST_HOURS, help='The number of hours to sample before last event date')
@click.option('--last-days', default=DEFAULT_FEATURES_LAST_DAYS, help='The number of days to sample before last event date')
@click.option('--last-weeks', default=DEFAULT_FEATURES_LAST_WEEKS, help='The number of minutes to sample before last event date')
@click.option('--last-months', default=DEFAULT_FEATURES_LAST_MONTHS, help='The number of months to sample before last event date')
@click.option('--events', default='events', help='The name of the input events file')
@click.option('--seed', default=DEFAULT_SEED, help='The random seed')
@click.option('--debug/--no-debug', default=DEFAULT_DEBUG, help='The debug flag')
@click.argument('filename', default='features')
def features(filename, events, churn_days, last_minutes, last_hours, 
                last_days, last_weeks, last_months, 
                seed, debug):
    f.generate(filename, events, churn_days, last_minutes, last_hours, 
                last_days, last_weeks, last_months, 
                seed, debug)

@main.command()
@click.option('--seed', default=DEFAULT_SEED, help='The random seed')
@click.option('--debug/--no-debug', default=DEFAULT_DEBUG, help='The debug flag')
@click.option('--events', default='events', help='The name of the input events file')
@click.argument('filename', default='metrics')
def metrics(filename, events, seed, debug):
    click.echo('no metrics yet!')

if __name__ == '__main__':
    main()
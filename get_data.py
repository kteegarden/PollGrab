import bs4
import requests
import pandas as pd
import os

def get_data(year, week, final_poll):
    if not final_poll:
        base_url = 'https://www.espn.com/college-football/rankings/_/poll/2/week/{}/year/{}/seasontype/2'.format(week, year)
    else:
        base_url='https://www.espn.com/college-football/rankings/_/poll/2/week/1/year/{}/seasontype/3'.format(year)

    print(base_url)
    website_HTML = requests.get(base_url).text  # returns the HTML at url

    soup = bs4.BeautifulSoup(website_HTML, 'html.parser')  # plug HTML into Beautiful Soup

    table = soup.find_all('table')[0]  # pull the first table on the web page
    rows = table.find_all('tr')[1:]  # throw out the first three rows (this is unusable data)

    teams = []
    points = []

    for row in rows:
        team_name = row.find_all('a')[2].get_text()  # Get text for each team name
        teams.append(team_name)

        team_points = row.find_all('td')[3].get_text()  # Get text for team points
        points.append(team_points)

    additional_text = soup.find(class_='pt4').get_text()  # Get all the teams also receiving votes
    additional_teams, additional_points = parse_end_of_poll_text(additional_text)  # parse these teams

    for t in additional_teams:  # add additional teams to list
        teams.append(t)
    for p in additional_points:  # add additional points to list
        points.append(p)

    teams, points = add_unranked_teams(teams, points)  # add teams received no votes

    Header = 'Week {}'.format(week)
    data = {'Team': teams, Header: points}
    df = pd.DataFrame(data=data, index=None)  # create Pandas datframe with this data
    return df  # return dataframe


def parse_end_of_poll_text(text):  # Extract all the poll data from the gross 'Others receiving votes' area
    others_receiving_votes = text.split('Others receiving votes: ')[1]  # split data and take second half
    remove_dropped_teams = others_receiving_votes.split('Dropped from rankings:')[0]  # split off dropped teams if needed
    teams = remove_dropped_teams.split(',')
    teams = [t.strip() for t in teams]  # remove whitespace that can mess up parsing
    additional_teams = []
    additional_points = []

    for t in teams:
        team = t.rsplit(' ', 1)[0]  # take the number portion of the string
        points = t.rsplit(' ', 1)[1]  # take the team portion of the string
        additional_teams.append(team)
        additional_points.append(points)

    return additional_teams, additional_points


def add_unranked_teams(team_names, team_points):  # adds teams that are not in the poll
    teams = ['Air Force', 'Akron', 'Alabama', 'Appalachian State', 'Arizona', 'Arizona State', 'Arkansas', 'Arkansas '
                                                                                                           'State',
             'Army', 'Auburn', 'Ball State', 'Baylor', 'Boise State', 'Boston College', 'Bowling Green', 'Buffalo',
             'BYU', 'California', 'Central Michigan', 'Charlotte', 'Cincinnati', 'Clemson', 'Coastal Carolina',
             'Colorado', 'Colorado State', 'Connecticut', 'Duke', 'East Carolina', 'Eastern Michigan', 'Florida',
             'Florida Atlantic', 'Florida Intl', 'Florida State', 'Fresno State', 'Georgia',
             'Georgia Southern', 'Georgia State', 'Georgia Tech', "Hawai'i", 'Houston', 'Illinois', 'Indiana',
             'Iowa', 'Iowa State', 'Kansas', 'Kansas State', 'Kent State', 'Kentucky', 'Liberty', 'Louisiana',
             'Louisiana Monroe', 'Louisiana Tech', 'Louisville', 'LSU', 'Marshall', 'Maryland', 'Memphis', 'Miami',
             'Miami (OH)', 'Michigan', 'Michigan State', 'Middle Tennessee', 'Minnesota', 'Mississippi State',
             'Missouri', 'Navy', 'NC State', 'Nebraska', 'Nevada', 'New Mexico', 'New Mexico State',
             'North Carolina', 'Northern Illinois', 'North Texas', 'Northwestern', 'Notre Dame', 'Ohio',
             'Ohio State', 'Oklahoma', 'Oklahoma State', 'Old Dominion', 'Ole Miss', 'Oregon', 'Oregon State',
             'Penn State', 'Pittsburgh', 'Purdue', 'Rice', 'Rutgers', 'San Diego State', 'San José State', 'SMU',
             'South Alabama', 'South Carolina', 'Southern Mississippi', 'South Florida', 'Stanford', 'Syracuse',
             'TCU', 'Temple', 'Tennessee', 'Texas', 'Texas A&M', 'Texas State', 'Texas Tech', 'Toledo', 'Troy',
             'Tulane', 'Tulsa', 'UAB', 'UCF', 'UCLA', 'UMass', 'UNLV', 'USC', 'Utah', 'Utah State', 'UTEP',
             'UT San Antonio', 'Vanderbilt', 'Virginia', 'Virginia Tech', 'Wake Forest', 'Washington', 'Washington '
                                                                                                       'State',
             'Western Kentucky', 'Western Michigan', 'West Virginia', 'Wisconsin', 'Wyoming']

    for t in teams: # compare team names in the poll to the master list of names. If a team is not in the poll, add it with zero votes.
        if t not in team_names:
            team_names.append(t)
            team_points.append(0)

    return team_names, team_points
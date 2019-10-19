"""
Script that creates a ncaaf_subdivisions.csv file
containing the mapping between conferences/teams/subdivisions
"""
import os
import pandas as pd
import numpy as np

# Assumes you have https://github.com/NathanDeMaria/EndGame cloned next to py-glicko
conferences_path = os.path.join('..', '..', '..', '..', 'EndGame', 'applications', 'ncaaf', 'ncaaf_conferences.csv')
conferences = pd.read_csv(conferences_path)

# Start with some so I don't have to do a bunch of requests
conference_info = [
    (1, 'ACC', 'fbs'),
    (4, 'Big 12', 'fbs'),
    (5, 'Big Ten', 'fbs'),
    (8, 'SEC', 'fbs'),
    (9, 'Pac-12', 'fbs'),
    (10, 'Big East', 'fbs'),
    (12, 'C-USA', 'fbs'),
    (15, 'MAC', 'fbs'),
    (16, 'WAC', 'fbs'),
    (17, 'MW', 'fbs'),
    (18, 'FBS Indep.', 'fbs'),
    (19, 'A 10', 'fcs'),
    (20, 'Big Sky', 'fcs'),
    (21, 'MVFC', 'fcs'),
    (22, 'Ivy', 'fcs'),
    (23, 'MAAC', 'fcs'),
    (24, 'MEAC', 'fcs'),
    (25, 'NEC', 'fcs'),
    (26, 'OVC', 'fcs'),
    (27, 'Patriot', 'fcs'),
    (28, 'Pioneer', 'fcs'),
    (29, 'Southern', 'fcs'),
    (30, 'Southland', 'fcs'),
    (31, 'SWAC', 'fcs'),
    (32, 'FCS Indep.', 'fcs'),
    (37, 'Sun Belt', 'fbs'),
    (40, 'Big South', 'fcs'),
    (43, 'Great West', 'fcs'),
    (48, 'CAA', 'fcs'),
    (100, 'American Southwest', 'd3'),
    (102, 'CCIW', 'd3'),
    (103, 'Centennial', 'd3'),
    (104, 'CIAA', 'd2'),
    (105, 'ECFC', 'd3'),
    (106, 'Empire 8', 'd3'),
    (107, 'GLIAC', 'd2'),
    (108, 'Great Lakes', 'd2'),
    (109, 'Great Northwest', 'd2'),
    (110, 'Gulf South', 'd2'),
    (111, 'Heartland', 'd3'),
    (112, 'Independent DII', 'd2'),
    (113, 'Independent DIII', 'd3'),
    (114, 'American Rivers', 'd3'),
    (115, 'Liberty League', 'd3'),
    (116, 'Lone Star', 'd2'),
    (117, 'Michigan', 'd3'),
    (118, 'Mid America', 'd2'),
    (119, 'Mid Atlantic', 'd3'),
    (120, 'Midwest', 'd3'),
    (121, 'Minnesota', 'd3'),
    (122, 'NESCAC', 'd3'),
    (123, 'Commonwealth Coast', 'd3'),
    (124, 'New Jersey', 'd3'),
    (126, 'North Coast', 'd3'),
    (127, 'Northeast 10', 'd2'),
    (128, 'Northern Athletics', 'd3'),
    (129, 'Northern Sun', 'd2'),
    (130, 'Northwest', 'd3'),
    (131, 'Ohio', 'd3'),
    (132, 'Old Dominion', 'd3'),
    (133, 'Pennsylvania State Athletic', 'd2'),
    (134, "Presidents'", 'd3'),
    (135, 'Rocky Mountain', 'd2'),
    (136, 'SIAC', 'd2'),
    (138, 'So. Cal.', 'd3'),
    (139, 'South Atlantic', 'd2'),
    (141, 'University', 'd3'),
    (142, 'Upper Midwest', 'd3'),
    (143, 'USA South', 'd3'),
    (144, 'Mountain East', 'd2'),
    (145, 'Wisconsin', 'd3'),
    (146, 'Great American', 'd2'),
    (147, 'Southern Athletic', 'd3'),
    (148, 'Southern Collegiate', 'd3'),
    (151, 'American', 'fbs'),
    (160, 'MSCAC', 'd3'),
    (165, 'Great Midwest Athletic', 'd2'),
]


subdivisions = ['fbs', 'fcs', 'd2', 'd3']
for _, row in conferences.sort_values('season', ascending=False).iterrows():
    if np.isnan(row.group):
        # print(f"Skipping {row['name']} {row.season}")
        continue
    group = int(row.group)
    if group in [c[0] for c in conference_info]:
        continue
    # print(group)
    for s in subdivisions:
        url = f'https://www.espn.com/college-football/standings/_/season/{int(row.season)}/group/{group}/view/{s}'
        body = requests.get(url).content
        soup = BeautifulSoup(body)
        header = soup.find(class_='headline__h1').text
        conf_name = header[:-len(' Football Standings - 2018')]
        if conf_name != '%{conference}':
            print(f"Found: {conf_name}")
            conference_info.append((group, conf_name, s))


subdivision_lookup = {i: s for i, _, s in conference_info}
subdivisions = [subdivision_lookup.get(g) for g in conferences.group]
conferences['conference_id'] = conferences.group
conferences['group'] = subdivisions

# For whatever reason, these didn't show up
manual_conferences = pd.DataFrame([
    # No football team until 2003
    # [None, "Southeastern Louisiana Lions", 2001],
    # [None, "Southeastern Louisiana Lions", 2002],
    ['fbs', "Louisiana Monroe Warhawks", 2001, 37],
    ['fbs', "Louisiana Monroe Warhawks", 2018, 37],
    ['fcs', "Central Connecticut Blue Devils", 2001, 25],
    # Technically no football for these 2 years
    ['fbs', "UAB Blazers", 2015, 12],
    ['fbs', "UAB Blazers", 2016, 12],
    ['fcs', "The Citadel Bulldogs", 2001, 29],
    ['d2', "Gardner-Webb Bulldogs", 2001, 112],
    ['fcs', "VMI Keydets", 2001, 29],
    # These three teams were part of the North Central Conference, but I don't know that ESPN conf id
    ['d2', "Northern Colorado Bears", 2001, 10000],
    ['d2', "North Dakota State Bison", 2001, 10000],
    ['d2', "North Dakota State Bison", 2002, 10000],
    ['d2', "North Dakota State Bison", 2003, 10000],
    ['d2', "South Dakota State Jackrabbits", 2001, 10000],
    ['d2', "South Dakota State Jackrabbits", 2002, 10000],
    ['d2', "South Dakota State Jackrabbits", 2003, 10000],
    # Didn't exist until 2003
    # [None, "Coastal Carolina Chanticleers", 2001],
    # [None, "Coastal Carolina Chanticleers", 2002],
    ['fcs', "St Francis (PA) Red Flash", 2001, 25],
    # Didn't exist until 2002
    # [None, "Florida Intl Golden Panthers", 2001],
    ['d2', "UC Davis Aggies", 2001, 112],
    ['d2', "UC Davis Aggies", 2002, 112],
    ['fcs', "UC Davis Aggies", 2003, 32],
    ['fcs', "UC Davis Aggies", 2004, 43],
    ['fcs', "North Dakota State Bison", 2004, 43],
    ['fcs', "South Dakota State Jackrabbits", 2004, 43],
], columns=['group', 'name', 'season', 'conference_id'])

conferences = pd.concat([conferences, manual_conferences])
# Hack b/c later script expects them to be ordered
ordered = dict(
    fbs='1fbs',
    fcs='2fcs',
    d2='3d2',
    d3='4d3',
)
ordered[None] = None
conferences['group'] = [ordered[g] for g in conferences.group]
conferences.to_csv('ncaaf_subdivisions.csv')

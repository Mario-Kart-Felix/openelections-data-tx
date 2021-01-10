#!/usr/bin/env python3
# This script takes looks for an ASC file with 208-character lines in the
# current directory and outputs a CSV file in the format preferred by OpenElections.
import code
import csv
import sys

if len(sys.argv) != 2:
    print("Usage: {} <County name>".format(sys.argv[0]))
    exit(1)

County = sys.argv[1]
county = County.lower()

def print_asc(line):
    print('Contest Number: {}'.format(line[0:4]))
    print('Candidate Number: {}'.format(line[4:7]))
    print('Precinct Code: {}'.format(line[7:11]))
    print('Total Votes: {}'.format(line[11:17]))
    print('Early Voting: {}'.format(line[35:41]))
    print('Election Day: {}'.format(line[23:29]))
    print('Provisional: {}'.format(line[29:35]))
    print('Vote Group 4: {}'.format(line[35:41]))
    print('Vote Group 5: {}'.format(line[41:47]))
    print('Party Code: {}'.format(line[47:50]))
    print('District Type ID: {}'.format(line[50:53]))
    print('District Code: {}'.format(line[53:57]))
    print('Contest Title: {}'.format(line[57:113]))
    print('Candidate Name: {}'.format(line[113:151]))
    print('Precinct Name: {}'.format(line[151:181]))
    print('District Name: {}'.format(line[181:206]))
    print('Votes Allowed: {}'.format(line[206:208]))
    print('Referendum Flag: {}'.format(line[208]))

def create_csv(datafile, output_filename):
    with open(output_filename, 'w', newline='') as f:
        with open(datafile) as data:
            fieldnames=['county','precinct','office','district','party','candidate','votes','early_voting','election_day','mail']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            current_precinct = 0
            current_race = 0
            for line in data:
                temp = {'county': County,
                        'precinct': line[151:181].strip().split(None)[1],
                        'office': line[57:113].strip(),
                        'party': line[47:50].strip(),
                        'candidate': line[113:151].strip(),
                        'votes': int(line[11:17]),
                        'early_voting': int(line[35:41]),
                        'election_day': int(line[23:29]),
                        'mail': int(line[43:47])}
                if 'State Representative' in temp['office']:
                    temp['district'] = int(temp['office'].split(None)[-1])
                    temp['office'] = 'State Representative'
                elif 'State Senator' in temp['office']:
                    temp['district'] = int(temp['office'].split(None)[-1])
                    temp['office'] = 'State Senator'
                elif 'United States Representative' in temp['office']:
                    temp['district'] = int(temp['office'].split(None)[-1])
                    temp['office'] = 'U.S. House'
                #elif 'United States Senator' in temp['office']:
                #    temp['office'] = 'U.S. Senate'
                writer.writerow(temp)


def load_data(filename):
    with open(filename) as f:
        datadict = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    return datadict

def sum_keys(datadict, office, candidate=None, field='votes'):
    total = 0
    for row in datadict:
            if row['office'] == office:
                    if candidate:
                            if row['candidate'] == candidate:
                                    total += int(row[field])
                    else:
                             total += int(row[field])
    return total

create_csv('{}.asc'.format(county), '{}-staging.csv'.format(County))

gendata = load_data('{}-staging.csv'.format(County))

code.interact(local=dict(globals(), **locals()))

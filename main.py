#!/usr/bin/env python

import pandas as pd
from award_api import NIHAwardAPI
import sys


def cong_district_fix(award_row):
    """
    Takes in the row of the awards dataframe and returns '01' if the state is Delaware or Vermont (where they only have
    one district for the whole state) or just the congressional district as it exists in the dataframe.
    """
    if award_row['org_state'] in ['DE', 'VT']:
        return '01'
    else:
        return award_row['cong_district']


def district_to_str(district_int):
    """
    Takes the integer of a district and transforms it to a string, appending a '0' to the district if it's under 10
    """
    if district_int < 10:
        return '0' + str(district_int)
    else:
        return str(district_int)


def main():
    sys.stdout.write('Starting process...\n')
    sys.stdout.flush()
    # the dictionary of the parameters I want to send to the api
    param_dict = {'agency': ['NIH'],
                  'orgstate': ['NY', 'DE', 'MD', 'NJ', 'PA', 'CT', 'RI', 'MA', 'VT', 'NH', 'ME'],
                  'fy': ['2019']}

    # instantiate and construct the full results list from the NIH api, given the above parameters
    api = NIHAwardAPI()
    api.construct_list(param_dict)

    # transform the results list from my api object to a pandas dataframe and fix the district labels for Delaware
    # and Vermont for easier joining and readability
    award_df = pd.DataFrame(api.result_list)
    award_df['cong_district'] = award_df.apply(lambda x: cong_district_fix(x), axis=1)

    # transform the legislators csv to a pandas dataframe and change all imported districts from integers to 2 character
    # strings for easier joining and readability
    legislator_df = pd.read_csv('legislators.csv')
    legislator_df['congressional_district'] = legislator_df['congressional_district'].apply(
        lambda x: district_to_str(x))

    # to avoid duplicate awards, and ensure the output can be easily searched by state and district, we remove since
    # resigned or deceased congresspeople from the legislator dataframe before joining
    legislator_removal = ['Elijah Cummings', 'Chris Collins', 'Tom Marino']
    legislator_df = legislator_df[~legislator_df['legislator_name'].isin(legislator_removal)]

    sys.stdout.write('\nAward and Legislator DataFrames generated.\n')
    sys.stdout.flush()

    # merge the legislators and awards dataframes on state and congressional district
    leg_award_df = legislator_df.merge(award_df,
                                       how='left',
                                       left_on=['state', 'congressional_district'],
                                       right_on=['org_state', 'cong_district'])

    leg_award_df.drop(['org_state', 'cong_district'], axis=1, inplace=True)

    leg_award_df = leg_award_df.sort_values(by=['state', 'congressional_district', 'total_cost'],
                                            ascending=[True, True, False])

    # NOTE: In this join, we lose any awards that do not have a congressional district associated with them (as of
    # 2021-03-04 that's approximately 17 awards). Given the focus of this project, to show congresspeople the value of
    # science in their districts, it was not pertinent to include these in the final output. This would likely change
    # were the focus on senators instead of members of the House

    # output the full dataframe to a csv
    leg_award_df.to_csv('legislators_awards.csv', index=False)
    sys.stdout.write('Legislator and Award CSV generated.')
    sys.stdout.flush()


if __name__ == "__main__":
    main()

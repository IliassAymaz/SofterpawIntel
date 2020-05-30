# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example for using the Google Search Analytics API (part of Search Console API).

A basic python command-line example that uses the searchAnalytics.query method
of the Google Search Console API. This example demonstrates how to query Google
search results data for your property. Learn more at
https://developers.google.com/webmaster-tools/

To use:
1) Install the Google Python client library, as shown at https://developers.google.com/webmaster-tools/v3/libraries.
2) Sign up for a new project in the Google APIs console at https://code.google.com/apis/console.
3) Register the project to use OAuth2.0 for installed applications.
4) Copy your client ID, client secret, and redirect URL into the client_secrets.json file included in this package.
5) Run the app in the command-line as shown below.

Sample usage:

  $ python search_analytics_api_sample.py 'https://www.example.com/' '2015-05-01' '2015-05-30'

"""
from __future__ import print_function

import argparse
import sys
from googleapiclient import sample_tools

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('-l', '--last_entry', required=False, action='store_false',
                       help=('Optional: Get last entry in the table only.'))

arguments = argparser.parse_args()


def main(argv):
    service, flags = sample_tools.init(
        argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/webmasters.readonly')

    # First run a query to learn which dates we have data for. You should always
    # check which days in a date range have data before running your main query.
    # This query shows data for the entire range, grouped and sorted by day,
    # descending; any days without data will be missing from the results.
    request = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'dimensions': ['date']
    }
    response = execute_request(service, flags.property_uri, request)
    print(response)
    # don't print, for log purposes
    # print_table(response, 'Available dates')


def execute_request(service, property_uri, request):
    """Executes a searchAnalytics.query request.

  Args:
    service: The webmasters service to use when executing the query.
    property_uri: The site or app URI to request data for.
    request: The request to be executed.

  Returns:
    An array of response rows.
  """
    return service.searchanalytics().query(
        siteUrl=property_uri, body=request).execute()


def print_table(response, title):
    """Prints out a response table.

  Each row contains key(s), clicks, impressions, CTR, and average position.

  Args:
    response: The server response to be printed as a table.
    title: The title of the table.
  """
    print('\n --' + title + ':')

    if 'rows' not in response:
        print('Empty response')
        return

    rows = response['rows']
    row_format = '{:<20}' + '{:>20}' * 4
    print(row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position'))

    '''if not arguments.last_element:
    list_of_keys = []'''
    for row in rows:
        keys = ''

        # Keys are returned only if one or more dimensions are requested.
        if 'keys' in row:
            keys = u','.join(row['keys']).encode('utf-8').decode()
        print(row_format.format(
            keys, row['clicks'], row['impressions'], row['ctr'], row['position']))
        '''if not arguments.last_element:
      list_of_keys.append(keys)
      return list_of_keys[-1]'''

    import json
    with open('./SofterPawInsights/querying/data/data_{}.json'.format(title), 'w') as f:
        json.dump(response, f, indent=2)
    print(response, 'checked')

if __name__ == '__main__':
    main(sys.argv)

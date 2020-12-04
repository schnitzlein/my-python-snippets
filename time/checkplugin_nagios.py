#!/usr/bin/env python3

"""
Copyright 2020 Christoph Schwalbe

Description: Strange solution for a internal use case.
Maintainer: Christoph Schwalbe
Create Date: 2020-02-24
"""

import argparse
import json
import locale

import adal
import nagiosplugin
import requests
from datetime import datetime
from msrestazure.azure_active_directory import AdalAuthentication
from msrestazure.azure_cloud import AZURE_GERMAN_CLOUD, AZURE_PUBLIC_CLOUD


PLUGIN_VERSION = "1.0.0"


"""
# Example call 
curl "https://api.applicationinsights.io/{api-version}/{app-id}/{query-path}?[query-parameters] -H "X-Api-Key: {api-key}"
app-id:  The ID from the Function in azure
api-key: The app-key must be created in azure for each Function
 
# Online Documentation: https://dev.applicationinsights.io/documentation/Authorization/API-key-authentication
# Online API-Tester: https://dev.applicationinsights.io/apiexplorer
Local you can use postman
"""

def _get_cloud(cloud):
    """
    get cloud environment object from string
    possible values
    'public'
    'german'
    """
    if cloud == "public":
        return AZURE_PUBLIC_CLOUD
    if cloud == "german":
        return AZURE_GERMAN_CLOUD
    return None


def _get_authheaders(token):
    '''
    accepts token dictionary from adal
    '''
    headers = dict()
    headers["Authorization"] = f"Bearer {token['accessToken']}"
    headers["Content-Type"] = "application/json"

    return headers


def _get_locale():
    '''
    returns the systems preferred locale
    '''
    return locale.getpreferredencoding()


def _get_applicationinsights_url(api_version, app_id, query):
    '''
    returns the url for REST Call
    '''
    if not api_version:
        api_version = "v1"
    host = f"https://api.applicationinsights.io/{api_version}/apps/{app_id}/{query}"
    return host

def _get_applicationinsights_url_header(api_key):
    '''
    returns the requests headers format for REST Call
    '''
    headers = {
      'x-api-key': api_key
    }
    return headers

class AliveStateContext(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        # alles True
        if metric.value == 'OK':
            """
            result = nagiosplugin.Result(nagiosplugin.Ok)
            print(result)
            print(type(self.result_cls(nagiosplugin.Ok, metric=metric)))
            print(self.result_cls(nagiosplugin.Ok, metric=metric))
            print(self.result_cls(nagiosplugin.Ok, metric=metric).state)
            print(self.result_cls(nagiosplugin.Ok, metric=metric).state.text)
            print(self.result_cls(nagiosplugin.Ok, metric=metric).metric)
            print(self.result_cls(nagiosplugin.Ok, metric=metric).metric.value)
            print( self.result_cls(nagiosplugin.Ok, metric=metric).__repr__ )
            """
            return self.result_cls(nagiosplugin.Ok, metric=metric)
        # laenger als 10 min ausgefallen und False
        elif metric.value == 'CRITICAL':
            return self.result_cls(nagiosplugin.Critical, metric=metric)
        # keine Daten erhalten
        elif metric.value == 'UNKNOWN':
            return self.result_cls(nagiosplugin.Unknown, metric=metric)
        # False festgestellt aber Regeneration innerhalb von 10 min
        elif metric.value == 'WARNING':
            return self.result_cls(nagiosplugin.Warn, metric=metric)
        elif metric.value == '-1':
            return self.result_cls(nagiosplugin.Unknown, metric=metric)
        else:
            return self.result_cls(nagiosplugin.Unknown, None, metric=metric)

    def describe(self, metric):
        #print(metric)
        if metric.value == '-1':
            return f'{metric.name}'
        else:
            if isinstance(metric.name, str):
                name = metric.name
                value = metric.value
            elif isinstance(metric.name, bytes):
                name = name.decode('utf-8')
                value = value.decode('utf-8')
            else:
                # fix encoding errors
                name = metric.name.encode(_get_locale(), 'ignore')
                value = metric.value.encode(_get_locale(), 'ignore')
            return f'{value} {name}'


class Alive(nagiosplugin.Resource):
    def __init__(self, **kwargs):
        self.cloud = _get_cloud(kwargs["cloud"])
        self.app_id = kwargs["app_id"]
        self.api_key = kwargs["api_key"]
        self.url = ""
        self.headers = ""

    def util_str_2_bool(self, s):
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            return -1

    def format_time(self, s, delim):
        '''
        ignore miliseconds and Timezone Z is UTC
        '''
        return s.partition(delim)[0]
    
    def get_date_object(self, dt):
        '''
        parse a timestamp string to datetime object in Format Year-month-dayTHH:MM:SS
        '''
        return datetime.strptime( dt, "%Y-%m-%dT%H:%M:%S" )
    
    def parse_timestamp(self, dt):
        '''
        get a parsed timestamp from string in datetime object
        '''
        date_object = self.get_date_object( self.format_time(dt, '.') )
        return date_object
     
    def calc_timediff(self, dt1, dt2):
        '''
        calc time between to datetime objects return in minutes
        dt1 ::= is the previous time
        dt2 ::= is the later time
        for example: dt2 - dt1 = time_between_dt2_and_dt1 , 
          if dt1 and dt2 are equal it will return 0
          else it will return int(-1)
        '''
        #print(dt1)
        dt1 = self.parse_timestamp(dt1)
        #print(dt2)
        dt2 = self.parse_timestamp(dt2)
        timediff = -1
        if dt2 > dt1:
            timediff = dt2 - dt1
        elif dt1 > dt2:
            timediff = dt1 - dt2
        elif dt1 == dt2:
            #timediff = datetime.timedelta(0)
            return -2
        else:
            return -1
        return int(timediff.seconds / 60)

    def get_incidents(self, data):
        '''
        it checks the latest timestamps
        if found False, compare latest timestamp,
          if more than 10 minutes and found False it is still False
        '''
        state = True
        incident = []
        if not data:
            return { 'state': "UNKNOWN", 'incidents': [] }
        
        for event in data:
            if bool(event[1])==False:
                incident.append(event)
        if len(incident) == 0:
            state = True # all is fine
        elif len(incident) > 0:
            state = False # incident !
        else:
            return -1
        return { 'state': state, 'incidents': incident }


    def check_incidents(self, data, incidents):
        '''
        check if incident took longer since 10 mins
        '''
        
        state = True
        if incidents == -1:
            raise ValueError('Data Format is wrong or input from get_incidents(self, data) is not valid!')
            return -1
        if incidents['state'] == True:
            state = "OK" # all is fine
        elif incidents['state'] == "UNKNOWN":
            state = "UNKNOWN"
        elif incidents['state'] == False:
            first_incident = incidents['incidents'][-1][0]
            last_incident  = incidents['incidents'][0][0]
            #print(first_incident)
            #print(last_incident)
            #print("alle: {}".format(incidents['incidents']))

            time_between_incident = self.calc_timediff(first_incident, last_incident)
            #print(time_between_incident)
            if time_between_incident >= 10:
                state = "CRITICAL"
            elif time_between_incident >= 0 and time_between_incident < 10:
                state = "WARNING"
            else:
                state = True
        else:
            raise KeyError('wrong input detected')
        return state

    def check_logic(self, data):
        '''
        return the state from monitoring log, 
        it checks the latest timestamps
        if found False longer than 10 mins -> False
        if found False and recover to True -> True
        if found True -> True
        else -> False
        '''
        incidents = self.get_incidents(data)
        return self.check_incidents(data, incidents)



    def probe(self):
        try:
            self.url = _get_applicationinsights_url('v1', self.app_id, "query?your_query_here")
            self.headers = _get_applicationinsights_url_header(self.api_key)
            payload = {}

            response = requests.request("GET", self.url, headers=self.headers, data = payload)
            
            if response.ok:
                content = response.json()
                
                # data collection and format
                # retrieve needed data in list of lists
                myfield = []
                for rows in content['tables'][0]['rows']:
                    #                    [ timestamp              , bool ]
                    myfield.append( [self.parse_timestamp(rows[0]), self.util_str_2_bool(rows[3])] )
                
                # set state from evaluating the log
                state = self.check_logic(myfield)

                yield nagiosplugin.Metric(str(state), state, context='Alive')

            else:
                yield nagiosplugin.Metric(f"Error {response.status_code}: {json.loads(response.text)['message']}", "-1", context='Alive')

        except Exception as ex:
            yield nagiosplugin.Metric(f"{ex.args}", "-1", context='Alive')


    def test(self, data):
        try:
            # set state from evaluating the log
            state = self.check_logic(data)
            print(state)
        except Exception as ex:
            print("Error in test: {}".format(ex))


def resourcehealth():
    check = nagiosplugin.Check(
        Alive(
        cloud = "public",
        app_id = "XXXXXX-XXXXXX-1234-1234-XXXXXX",
        api_key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        ),
        AliveStateContext('Alive')
    )
    check.main()


@nagiosplugin.guarded
def main():
    resourcehealth()


if __name__ == '__main__':
    main()

    """
    # Test
    # create an API-Key
    testclass = Alive(
        cloud = "public",
        app_id = "XXXXXX-XXXXXX-1234-1234-XXXXXX",
        api_key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    #testclass.probe()
    import test_data
    #TODO: Refactor me, put in base and complex class and put test in test_cases
    # should be UNKNOWN
    x = []
    testclass.test(x)

    # should be True (OK)
    x = test_data.test_data1()
    for d in x:
        d[1] = testclass.util_str_2_bool(d[1])
    testclass.test(x)

    # should be False (WARNING)
    x = test_data.test_Fail_Recovery()
    for d in x:
        d[1] = testclass.util_str_2_bool(d[1])
    testclass.test(x)

    # should be False (WARNING)
    x = test_data.test_Fail_still_Failing()
    for d in x:
        d[1] = testclass.util_str_2_bool(d[1])
    testclass.test(x)

    # should be False (CRITICAL)
    x = test_data.test_Fail_always_Failing()
    for d in x:
        d[1] = testclass.util_str_2_bool(d[1])
    testclass.test(x)
    """

    # initiate the parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        action="version",
        help="Print version number",
        version="%(prog)s version " + str(PLUGIN_VERSION),
    )
    apps = parser.add_argument_group("ApplicationInsight")
    apps.add_argument(
        "--app-id", help="Azure Application Insight API-Key for Application", required=True, dest="app_id",
    )
    apps.add_argument(
        "--app-key", help="Azure Application Insight App-Key", required=True, dest="app_key",
    )
    apps.add_argument(
        "--client-secret", help="client secret of service principal", required=True, dest="client_secret",
    )
    apps.add_argument(
        "--cloud",
        nargs="?",
        choices=["german", "public"],
        default="public",
        help="select azure cloud to check (public, german)",
        dest="cloud",
    )

    resource = parser.add_argument_group("Resource")
    resource.add_argument(
        "--resource-id", help="resource id of azure resource", required=True, dest="resource_id"
    )

    # default: 2017-07-01
    resource.add_argument(
        "--api-version",
        required=False,
        default="2017-07-01",
        help="Azure ResourceHealth API Version",
        dest="api_version")

    parser.set_defaults(func=resourcehealth)

    # Evaluate Arguments
    args = parser.parse_args()

    # call the determined function with the parsed arguments
    args.func(args)

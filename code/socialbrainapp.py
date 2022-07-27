import pandas as pd, numpy as np
from datetime import datetime

def get_demographics(element):
    assert type(element) is dict, 'Input should be dictionary'
    assert ('Age' in element.keys()), '"Age" should exist in dictionary'

    demo_df = pd.DataFrame(index=[element['UserId']], 
                           columns=['Age','Gender','Race',
                                    'Ethnicity','Education',
                                    'Income','Zip',
                                    'Withdrawal','HasPreviouslyInstalled',
                                    'Year', 'Month','Day',
                                    'Hour','Minute','Second'])

    demo_df.at[element['UserId'], 'Age'] = element['Age']
    demo_df.at[element['UserId'], 'Gender'] = element['Gender']
    demo_df.at[element['UserId'], 'Race'] = element['Race']
    demo_df.at[element['UserId'], 'Ethnicity'] = element['Ethnicity']
    demo_df.at[element['UserId'], 'Education'] = element['Education']
    demo_df.at[element['UserId'], 'Income'] = element['Income']
    demo_df.at[element['UserId'], 'Zip'] = element['Zip']
    demo_df.at[element['UserId'], 'Withdrawal'] = element['Withdrawal']
    demo_df.at[element['UserId'], 'HasPreviouslyInstalled'] = element['HasPreviouslyInstalled']

    # convert timestamp
    tmp_date = datetime.strptime(element['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    demo_df.at[element['UserId'], 'Year'] = int(tmp_date.year)
    demo_df.at[element['UserId'], 'Month'] = int(tmp_date.month)
    demo_df.at[element['UserId'], 'Day'] = int(tmp_date.day)
    demo_df.at[element['UserId'], 'Hour'] = int(tmp_date.hour)
    demo_df.at[element['UserId'], 'Minute'] = int(tmp_date.minute)
    demo_df.at[element['UserId'], 'Second'] = int(tmp_date.second)

    return demo_df

def get_oci(element):
    assert type(element) is dict, 'Input should be dictionary'
    assert ('SurveyName' in element.keys()), '"SurveyName" should exist in dictionary'
    assert (element['SurveyName'] == 'OCI'), '"SurveyName" should be "OCI"'

    oci_df = pd.DataFrame(index=[element['UserId']], 
                          columns=['SurveyName',
                                   'SurveyQuestion',
                                   'SurveyAnswer',
                                   'Response',
                                   'Question',
                                   'Year', 'Month','Day',
                                   'Hour','Minute','Second'])

    oci_df.at[element['UserId'], 'SurveyName'] = element['SurveyName']
    oci_df.at[element['UserId'], 'SurveyQuestion'] = element['SurveyQuestion']
    oci_df.at[element['UserId'], 'SurveyAnswer'] = element['SurveyAnswer']
    
    # recode responses
    if element['SurveyAnswer'] == 'Not at all':
        oci_df.at[element['UserId'], 'Response'] = 0
    elif element['SurveyAnswer'] == 'A little':
        oci_df.at[element['UserId'], 'Response'] = 1
    elif element['SurveyAnswer'] == 'Moderately':
        oci_df.at[element['UserId'], 'Response'] = 2
    elif element['SurveyAnswer'] == 'A lot':
        oci_df.at[element['UserId'], 'Response'] = 3
    elif element['SurveyAnswer'] == 'Extremely':
        oci_df.at[element['UserId'], 'Response'] = 4
    elif element['SurveyAnswer'] == '':
        oci_df.at[element['UserId'], 'Response'] = np.nan
    
    oci_df.at[element['UserId'], 'Question'] = element['Que']

    # convert timestamp
    tmp_date = datetime.strptime(element['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    oci_df.at[element['UserId'], 'Year'] = int(tmp_date.year)
    oci_df.at[element['UserId'], 'Month'] = int(tmp_date.month)
    oci_df.at[element['UserId'], 'Day'] = int(tmp_date.day)
    oci_df.at[element['UserId'], 'Hour'] = int(tmp_date.hour)
    oci_df.at[element['UserId'], 'Minute'] = int(tmp_date.minute)
    oci_df.at[element['UserId'], 'Second'] = int(tmp_date.second)

    return oci_df

def get_sds(element):
    assert type(element) is dict, 'Input should be dictionary'
    assert ('SurveyName' in element.keys()), '"SurveyName" should exist in dictionary'
    assert (element['SurveyName'] == 'SDS'), '"SurveyName" should be "SDS"'

    sds_df = pd.DataFrame(index=[element['UserId']], 
                          columns=['SurveyName',
                                   'SurveyQuestion',
                                   'SurveyAnswer',
                                   'Response',
                                   'Question',
                                   'Year', 'Month','Day',
                                   'Hour','Minute','Second'])

    sds_df.at[element['UserId'], 'SurveyName'] = element['SurveyName']
    sds_df.at[element['UserId'], 'SurveyQuestion'] = element['SurveyQuestion']
    sds_df.at[element['UserId'], 'SurveyAnswer'] = element['SurveyAnswer']

    # recode responses
    if element['SurveyAnswer'] == 'A little of the time':
        sds_df.at[element['UserId'], 'Response'] = 1
    elif element['SurveyAnswer'] == 'Some Of The Time':
        sds_df.at[element['UserId'], 'Response'] = 2
    elif element['SurveyAnswer'] == 'Good Part Of The Time':
        sds_df.at[element['UserId'], 'Response'] = 3
    elif element['SurveyAnswer'] == 'Most Of The Time':
        sds_df.at[element['UserId'], 'Response'] = 4
    elif element['SurveyAnswer'] == '':
        sds_df.at[element['UserId'], 'Response'] = np.nan
    
    sds_df.at[element['UserId'], 'Question'] = element['Que']

    # convert timestamp
    tmp_date = datetime.strptime(element['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    sds_df.at[element['UserId'], 'Year'] = int(tmp_date.year)
    sds_df.at[element['UserId'], 'Month'] = int(tmp_date.month)
    sds_df.at[element['UserId'], 'Day'] = int(tmp_date.day)
    sds_df.at[element['UserId'], 'Hour'] = int(tmp_date.hour)
    sds_df.at[element['UserId'], 'Minute'] = int(tmp_date.minute)
    sds_df.at[element['UserId'], 'Second'] = int(tmp_date.second)
    
    return sds_df

def get_lsas(element):
    assert type(element) is dict, 'Input should be dictionary'
    assert ('SurveyName' in element.keys()), '"SurveyName" should exist in dictionary'
    assert (element['SurveyName'] == 'LSAS'), '"SurveyName" should be "LSAS"'

    lsas_df = pd.DataFrame(index=[element['UserId']], 
                        columns=['SurveyName',
                                'SurveyQuestion',
                                'SurveyAnswer',
                                'Response',
                                'Question',
                                'Year', 'Month','Day',
                                'Hour','Minute','Second'])

    lsas_df.at[element['UserId'], 'SurveyName'] = element['SurveyName']
    lsas_df.at[element['UserId'], 'SurveyQuestion'] = element['SurveyQuestion']
    lsas_df.at[element['UserId'], 'SurveyAnswer'] = element['SurveyAnswer']
    
    # recode responses
    if element['SurveyAnswer'] == 'Never (0%)':
        lsas_df.at[element['UserId'], 'Response'] = 1
    elif element['SurveyAnswer'] == 'Occasionally (1-33%)':
        lsas_df.at[element['UserId'], 'Response'] = 2
    elif element['SurveyAnswer'] == 'Often (34-66%)':
        lsas_df.at[element['UserId'], 'Response'] = 3
    elif element['SurveyAnswer'] == 'Usually (67-100%)':
        lsas_df.at[element['UserId'], 'Response'] = 4
    elif element['SurveyAnswer'] == '':
        lsas_df.at[element['UserId'], 'Response'] = np.nan
    
    lsas_df.at[element['UserId'], 'Question'] = element['Que']

    # convert timestamp
    tmp_date = datetime.strptime(element['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    lsas_df.at[element['UserId'], 'Year'] = int(tmp_date.year)
    lsas_df.at[element['UserId'], 'Month'] = int(tmp_date.month)
    lsas_df.at[element['UserId'], 'Day'] = int(tmp_date.day)
    lsas_df.at[element['UserId'], 'Hour'] = int(tmp_date.hour)
    lsas_df.at[element['UserId'], 'Minute'] = int(tmp_date.minute)
    lsas_df.at[element['UserId'], 'Second'] = int(tmp_date.second)

    return lsas_df
    
def get_hardball(element):
    assert type(element) is dict, 'Input should be dictionary'
    assert ('Game' in element.keys()), '"Game" should exist in dictionary'
    assert ('Screen' not in element.keys()), '"Screen" should NOT exist in dictionary -- Use to get subjective influence ratings'
    assert (element['Game'] == 'Hardball'), '"Game" should be "Hardball"'

    hardball_df = pd.DataFrame(index=[element['UserId']], 
                               columns=['Condition','OpponentNum',
                                        'Game','TeamName',
                                        'Opponent','Offer',
                                        'Response','Accept','Reject',
                                        'Year', 'Month','Day',
                                        'Hour','Minute','Second'])

    hardball_df.at[element['UserId'], 'Condition'] = element['Condition']
    hardball_df.at[element['UserId'], 'OpponentNum'] = element['OpponentNum']
    hardball_df.at[element['UserId'], 'Game']  = element['Game']
    hardball_df.at[element['UserId'], 'TeamName'] = element['TeamName']
    hardball_df.at[element['UserId'], 'Opponent'] = element['Opponent']
    hardball_df.at[element['UserId'], 'Offer'] = float(element['Offer'].strip('$'))
    hardball_df.at[element['UserId'], 'Response'] = element['Response']

    # recode responses with 1s and 0s
    if element['Response'] == 'Accept':
        hardball_df.at[element['UserId'], 'Accept'] = 1
        hardball_df.at[element['UserId'], 'Reject'] = 0
    else:
        hardball_df.at[element['UserId'], 'Accept'] = 0
        hardball_df.at[element['UserId'], 'Reject'] = 1

    # convert timestamp
    tmp_date = datetime.strptime(element['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    hardball_df.at[element['UserId'], 'Year'] = int(tmp_date.year)
    hardball_df.at[element['UserId'], 'Month'] = int(tmp_date.month)
    hardball_df.at[element['UserId'], 'Day'] = int(tmp_date.day)
    hardball_df.at[element['UserId'], 'Hour'] = int(tmp_date.hour)
    hardball_df.at[element['UserId'], 'Minute'] = int(tmp_date.minute)
    hardball_df.at[element['UserId'], 'Second'] = int(tmp_date.second)

    return hardball_df

def get_hardball_ratings(element):
    assert type(element) is dict, 'Input should be dictionary'
    assert ('Game' in element.keys()), '"Game" should exist in dictionary'
    assert ('Screen' in element.keys()), '"Screen" should exist in dictionary'
    assert (element['Game'] == 'Hardball'), '"Game" should be "Hardball"'

    hardball_behav_df = pd.DataFrame(index=[element['UserId']], 
                                    columns=['Game','TeamName','Rate',
                                                'Year', 'Month','Day',
                                                'Hour','Minute','Second'])

    hardball_behav_df.at[element['UserId'], 'Game']  = element['Game']
    hardball_behav_df.at[element['UserId'], 'TeamName'] = element['TeamName']
    hardball_behav_df.at[element['UserId'], 'Rate'] = element['Rate']

    # convert timestamp
    tmp_date = datetime.strptime(element['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    hardball_behav_df.at[element['UserId'], 'Year'] = int(tmp_date.year)
    hardball_behav_df.at[element['UserId'], 'Month'] = int(tmp_date.month)
    hardball_behav_df.at[element['UserId'], 'Day'] = int(tmp_date.day)
    hardball_behav_df.at[element['UserId'], 'Hour'] = int(tmp_date.hour)
    hardball_behav_df.at[element['UserId'], 'Minute'] = int(tmp_date.minute)
    hardball_behav_df.at[element['UserId'], 'Second'] = int(tmp_date.second)

    return hardball_behav_df

def get_journey(element):
    print('Need to add')

    return 0
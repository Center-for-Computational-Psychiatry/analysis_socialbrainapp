import pandas as pd, numpy as np
from datetime import datetime
from itertools import combinations

def get_withdrawn_ids(list1, list2):
    matching = []
    nonmatch1 = []
    nonmatch2 = []
    
    for item in list1:
        if item in list2:
            matching.append(item)
        else:
            nonmatch1.append(item)
            
    for item in list2:
        if item not in list1:
            nonmatch2.append(item)
            
    return list(np.unique(matching)), list(np.unique(nonmatch1)), list(np.unique(nonmatch2))

def get_hardball_blocks(df):
    '''
    DF is subject specific and should be contain the following columns:
    ['OpponentNum','Condition','Year','Month','Day','Hour','Minute','Second']
    '''

    # Create a new column "BlockID" filled with NaNs
    df['BlockID'] = np.nan

    # Iterate over rows
    curr_block_id = 0
    for i, row in df.iterrows():

        # Check if the current row starts a new session
        if row['OpponentNum'] == 1:

            # Iterate over the next 30 rows
            this_block_first_opp_count = []
            this_block_first_idx_count = []
            this_block_first_cond_count = []
            end_current_block = False
            for j_idx, j in enumerate(range(i, i+30)):
                # Check if the row exists
                if j < len(df):

                    # check that OpponentNum is counting up
                    if int(j_idx+1) == int(df.loc[j,'OpponentNum']):
                        this_block_first_idx_count += [j]
                        this_block_first_opp_count += [df.loc[j,'OpponentNum']]
                        this_block_first_cond_count += [df.loc[j,'Condition']]
                    else:
                        end_current_block = True
                    
                    if len(this_block_first_idx_count) == 30:
                        end_current_block = True
                    
                    if end_current_block:
                        if len(this_block_first_idx_count) == 30 and np.sum(this_block_first_opp_count)==465 and np.sum([1 for x in this_block_first_cond_count if x==this_block_first_cond_count[0]]):
                            curr_block_id += 1
                            df.loc[this_block_first_idx_count,'BlockID'] = curr_block_id
    return df

def get_hardball_sessions(df):
    '''
    DF is subject specific and should be contain the following columns:
    ['OpponentNum','Condition','BlockID','Year','Month','Day','Hour','Minute','Second']
    '''
    df = df[~np.isnan(df.BlockID)]

    # create a dictionary that groups the block_id values by condition_id
    cond_block_dict = {}
    for cond_id, block_ids in df.groupby("Condition")["BlockID"]:
        cond_block_dict[cond_id] = set(block_ids)

    # create a list of all possible pairs of condition ids
    cond_pairs = list(combinations(cond_block_dict.keys(), 2))

    # create a dictionary to store the time differences for each pair of block_ids
    time_diff_dict = {}

    # loop through all pairs of condition ids
    for cond_pair in cond_pairs:
        # get the block_ids for each condition id
        block_ids1 = cond_block_dict[cond_pair[0]]
        block_ids2 = cond_block_dict[cond_pair[1]]
        
        # create a list of all possible pairs of block_ids
        block_pairs = list(combinations(block_ids1.union(block_ids2), 2))
        
        # loop through all pairs of block_ids
        for block_pair in block_pairs:
            # get the rows corresponding to the two block_ids
            rows1 = df[(df["BlockID"] == int(block_pair[0]))]
            rows2 = df[(df["BlockID"] == int(block_pair[1]))]
            
            # get the earliest and latest timestamps for the two blocks
            row2_times = rows2[["Year", "Month", "Day", "Hour", "Minute", "Second"]].apply(lambda x: pd.Timestamp(*x), axis=1)
            row1_times = rows1[["Year", "Month", "Day", "Hour", "Minute", "Second"]].apply(lambda x: pd.Timestamp(*x), axis=1)

            if row1_times.mean() > row2_times.mean(): # row 1 later
                earliest_timestamp = min(row2_times)
                latest_timestamp = max(row1_times)
            elif row1_times.mean() < row2_times.mean(): # row 1 earlier
                earliest_timestamp = min(row1_times)
                latest_timestamp = max(row2_times)
            
            # calculate the time difference between the two blocks
            time_diff = (latest_timestamp - earliest_timestamp).total_seconds()
            
            # store the time difference in the dictionary
            time_diff_dict[block_pair] = time_diff

    # create a list of all possible pairs of block_ids
    block_pairs = list(combinations(set(df["BlockID"]), 2))

    # create a dictionary to store the session_id for each block_id
    session_id_dict = {}
    session_count = 0

    # loop through all pairs of block_ids
    for block_pair in block_pairs:
        # get the condition ids for each block_id
        cond_ids1 = set(df[df["BlockID"] == block_pair[0]]["Condition"])
        cond_ids2 = set(df[df["BlockID"] == block_pair[1]]["Condition"])
        
        # check if the two block_ids correspond to two unique condition_ids
        if len(cond_ids1) == 1 and len(cond_ids2) == 1 and len(cond_ids1.union(cond_ids2)) == 2:
            # calculate the time difference between the two blocks
            time_diff = time_diff_dict[block_pair]
            
            # get dict of time_diff for other pairs
            other_time_diffs = {i:time_diff_dict[i] for i in time_diff_dict if ((block_pair[0] in i) or (block_pair[1] in i)) and (i!=block_pair)}

            # check if the time difference is minimal
            if other_time_diffs:
                if time_diff < min([time_diff_dict[b] for b in other_time_diffs]):
                    session_count += 1
                    # assign a new session_id to the two block_ids
                    session_id_dict[np.round(block_pair[0],1)] = session_count
                    session_id_dict[np.round(block_pair[1],1)] = session_count
            else:
                session_count += 1
                # assign a new session_id to the two block_ids
                session_id_dict[np.round(block_pair[0],1)] = session_count
                session_id_dict[np.round(block_pair[1],1)] = session_count
                
    #create a new column called session_id in the dataframe
    df['SessionID'] = df['BlockID'].map(session_id_dict)

    return df

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
    if element['SurveyQuestion'] in [1, 3, 4, 7, 8, 9, 10, 13, 15, 20]: # regular code
        if element['SurveyAnswer'] == 'A little of the time':
            sds_df.at[element['UserId'], 'Response'] = 1
        elif element['SurveyAnswer'] == 'Some of the time':
            sds_df.at[element['UserId'], 'Response'] = 2
        elif element['SurveyAnswer'] == 'Good part of the time':
            sds_df.at[element['UserId'], 'Response'] = 3
        elif element['SurveyAnswer'] == 'Most of the time':
            sds_df.at[element['UserId'], 'Response'] = 4
        elif element['SurveyAnswer'] == '':
            sds_df.at[element['UserId'], 'Response'] = np.nan
    else: # reverse code
        if element['SurveyAnswer'] == 'A little of the time':
            sds_df.at[element['UserId'], 'Response'] = 4
        elif element['SurveyAnswer'] == 'Some of the time':
            sds_df.at[element['UserId'], 'Response'] = 3
        elif element['SurveyAnswer'] == 'Good part of the time':
            sds_df.at[element['UserId'], 'Response'] = 2
        elif element['SurveyAnswer'] == 'Most of the time':
            sds_df.at[element['UserId'], 'Response'] = 1
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
    
    # recode responses (no attention check)
    if element['SurveyAnswer'] == 'Never (0%)':
        lsas_df.at[element['UserId'], 'Response'] = 0
    elif element['SurveyAnswer'] == 'Occasionally (1-33%)':
        lsas_df.at[element['UserId'], 'Response'] = 1
    elif element['SurveyAnswer'] == 'Often (34-66%)':
        lsas_df.at[element['UserId'], 'Response'] = 2
    elif element['SurveyAnswer'] == 'Usually (67-100%)':
        lsas_df.at[element['UserId'], 'Response'] = 3
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
                                        'Response','Accept','Reject','Reward',
                                        'Year', 'Month','Day',
                                        'Hour','Minute','Second'])

    hardball_df.at[element['UserId'], 'Condition'] = element['Condition']
    hardball_df.at[element['UserId'], 'OpponentNum'] = element['OpponentNum']
    hardball_df.at[element['UserId'], 'Game']  = element['Game']
    hardball_df.at[element['UserId'], 'TeamName'] = element['TeamName']
    hardball_df.at[element['UserId'], 'Opponent'] = element['Opponent']
    hardball_df.at[element['UserId'], 'Offer'] = float(element['Offer'].strip('$'))
    hardball_df.at[element['UserId'], 'Response'] = element['Response']

    # recode responses with 1s and 0s and add reward if accept
    if element['Response'] == 'Accept':
        hardball_df.at[element['UserId'], 'Accept'] = 1
        hardball_df.at[element['UserId'], 'Reject'] = 0
        hardball_df.at[element['UserId'], 'Reward'] = float(element['Offer'].strip('$'))
    else:
        hardball_df.at[element['UserId'], 'Accept'] = 0
        hardball_df.at[element['UserId'], 'Reject'] = 1
        hardball_df.at[element['UserId'], 'Reward'] = 0.0

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
    char_roles = ['First', 'Second', 'Assistant', 'Newcomb', 'Hayworth', 'Neutral'] 
    sub_id = element['UserId']

    if any(name in element for name in ['SlideNum', 'Task', 'CharFirstX']):

        # get task version info
        if 'SlideNum' in element:

            if element['SlideNum'] == 1:
                snt_df = pd.DataFrame(index=[sub_id], 
                                      columns=list(np.array([[char + '_name', 
                                                              char + '_gender', 
                                                              char + '_image'] for char in char_roles]).flatten()))
                characters = []
                for role in char_roles:
                    name = element['CharName' + role]
                    img = element['CharImage' + role].split('/')[-1]
                    gender = element['CharGender' + role]
                    characters.append([name, gender, img])
                snt_df.at[sub_id, :] = list(np.array(characters).flatten())
                task_name = 'characters'

        # get task data
        if 'Task' in element:

            task = element['Task']
            time_on = element['Timestamp']

            if 'Decision' in task: 
                snt_df = pd.DataFrame(index=[sub_id], columns=['decision_num','decision'],
                                      data=np.array([task, element['JourneyAnswer']]).reshape(1,-1))
                task_name = 'decisions'

            elif ('Attention' in task) or ('Memory' in task):
                snt_df = pd.DataFrame(index=[sub_id], columns=['question_num','answer'],
                                      data=np.array([task, element['Option']]).reshape(1,-1))
                task_name = 'memory' 

        # get dots data
        elif 'CharFirstX' in element:

            dots = list(np.array([[element['Char'+role+'X'], element['Char'+role+'Y']] for role in char_roles]).flatten())
            snt_df = pd.DataFrame(index=[sub_id], columns=list(np.array([['dots_' + char + '_affil', 'dots_' + char + '_power'] for char in char_roles]).flatten()),
                                  data=dots)
            task_name = 'dots'

        # convert timestamp
        tmp_date = datetime.strptime(element['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        snt_df.at[element['UserId'], 'Datetime'] = element['Timestamp']
        snt_df.at[element['UserId'], 'Year'] = int(tmp_date.year)
        snt_df.at[element['UserId'], 'Month'] = int(tmp_date.month)
        snt_df.at[element['UserId'], 'Day'] = int(tmp_date.day)
        snt_df.at[element['UserId'], 'Hour'] = int(tmp_date.hour)
        snt_df.at[element['UserId'], 'Minute'] = int(tmp_date.minute)
        snt_df.at[element['UserId'], 'Second'] = int(tmp_date.second)

        output = [task_name, snt_df]

    return output
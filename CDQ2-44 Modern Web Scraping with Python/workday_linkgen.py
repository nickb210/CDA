import re
"""
========== Booz Allen Hamilton ==========
https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs/job/USA-DC-Washington-1000-Independence-Ave-SW/Information-Systems-Security-Officer--Junior_R0102774
https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs/job/USA-TX-San-Antonio-3133-General-Hudnell-Dr/Cyber-Network-Engineer--Junior_R0097661

========== Trend Micro ==========
https://trendmicro.wd3.myworkdayjobs.com/en-US/External/job/San-Jose/Cloud-Security-Architect_R0000907
"""

url_dict = {'Booz Allen Hamilton': 'https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs/job/', 
            'Trend Micro'        : 'https://trendmicro.wd3.myworkdayjobs.com/en-US/External/job/'}

'''
==============================================================
This is a helper function for 'linkGen()' to help format the 
URL string.
flag=Flase ---> replacing non alpha characters for job location 
flag=True  ---> replacing non alpha characters for the job title
============================================================== 
'''
def replaceNonAlpha(my_str, flag=False):
    if '(' in my_str and ')' in my_str:
        my_str = my_str.replace('(', ',')
        my_str = my_str.replace(')', '')

    # flag is used for job title
    if flag:
        my_str = my_str.replace(',', ' ')
    else:    
        my_str = my_str.replace(',', '')
    my_str = my_str.replace(' ', '-')

    return my_str

'''
==============================================================
This function generates a valid URL when given a JOB TITLE, 
JOB LOCATION, JOB ID and a BASE URL. URL's are formatted by the following:
(E.g. Booze Allen Hamilton)

BASE_URL = https://bah.wd1.myworkdayjobs.com/en-US/job
JOB LOCATION = Country_State_City_Address
JOB TITLE = Full_Job_Title
JOB ID = jobID

Url Generated --> BASE URL/JOB LOCATION/JOB TITLE_JOB ID
============================================================== 
'''
def linkGen(job_title, job_location, job_id, site_title):
    link = ''
    link_start = ''

    for key in url_dict:
        if key == site_title:
            link_start = url_dict[key]
    link += link_start
    
    # replace non alpha characters for job location
    link += replaceNonAlpha(job_location) + '/'

    # replace non alpha characters for job title
    link += replaceNonAlpha(job_title, True) + '_'
    link += job_id
    return link
    



title = 'Information Systems Security Officer, Junior'
loc = 'USA, DC, Washington (1000 Independence Ave SW)'
#loc = 'USA, TX, San Antonio (3133 General Hudnell Dr)'
j_id = 'R0102774'

"""
2. Cyber Network Engineer, Junior
        JobID   : R0097661
        Location: USA, TX, San Antonio (3133 General Hudnell Dr)
        Date    : Posted 30+ Days Ago
"""

#replaceNonAlpha(loc)
#linkGen(title, loc,j_id)
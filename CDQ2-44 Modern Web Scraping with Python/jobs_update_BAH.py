#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, sys, itertools, re
from typeWriterEffect import typeWriter
import workday_linkgen

"""
How to use css selector for selenium
https://saucelabs.com/resources/articles/selenium-tips-css-selectors
"""
CHROME_PATH     = "/Users/nicholausbrell/python/selenium/chromedriver"
BAH_WORKDAY_URL = "https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs"
TM_WORKDAY_URL = "https://trendmicro.wd3.myworkdayjobs.com/en-US/External"

url_dict = {'Booz Allen Hamilton': 'https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs', 
            'Trend Micro'        : 'https://trendmicro.wd3.myworkdayjobs.com/en-US/External'}

'''
==============================================================
Create Options to make chrome browser 'headless'
When using selelium exectues, we will not see the automation taking place.
============================================================== 
'''
chrome_options = Options()
chrome_options.headless = True

'''
==============================================================
create selenium webdriver session using google chrome, and use 
the options created from the options object above
============================================================== 
'''
driver = webdriver.Chrome(CHROME_PATH, options=chrome_options)

'''
==============================================================
go to the Workday Booz Allen Hamilton page specifed by BAH_WORKDAY_URL
============================================================== 
'''
driver.get(BAH_WORKDAY_URL)
#driver.get(TM_WORKDAY_URL)
time.sleep(3)

'''
==============================================================
Checking to see if the URL matches the predefined URL inside
the dictionary url_dict
============================================================== 
'''
site_title = None
for key in url_dict:
    if url_dict[key] == driver.current_url:
        site_title = key
        break

'''
==============================================================
SEARCH
============================================================== 
'''
if len(sys.argv) == 1:
    job_search_str = 'cyber security'
elif len(sys.argv) > 1:
    job_search_str = " ".join([str(x) for x in sys.argv[1:]])
typeWriter("Searching for jobs containing '%s' ..." % job_search_str)
#print("Searching for jobs containing '%s'" % job_search_str)

'''
==============================================================
Using selenium to find the 'seach' bar by its XPATH on the WorkDay
website. Here is where we search using the jobs_search_str variable.
============================================================== 
'''
search = driver.find_element_by_xpath('//*[@id="wd-AdvancedFacetedSearch-SearchTextBox-input"]')
search.send_keys(job_search_str)
search.send_keys(Keys.ENTER)

'''
==============================================================
wait so the URL can finish loading 
============================================================== 
'''
time.sleep(4)

'''
==============================================================
Retrieve the inner HTML (html inside the opeing and closing tags, with 
th tag excluded) of the page source, then create a BeautifulSoup 
object so we can parse the URL source.
============================================================== 
'''
body = driver.execute_script('return document.documentElement.innerHTML') # HTML from '<body>'
soup = BeautifulSoup(body, 'lxml')


'''
# locations is found using the css selector for every <span> tag whos "class" attribute begins with "gwt-InlineLabel"
i.e. <span class="gwt-InlineLabel WCAG WB5F" title="R0097267   |   USA, VA, Fort Belvoir (8725 John J Kingman Rd)
   |   Posted 30+ Days Ago" id="gwt-uid-2" data-automation-id="compositeSubHeaderOne">
        "R0097267   
        |   USA, VA, Fort Belvoir (8725 John J Kingman Rd)   
        |   Posted 30+ Days Ago"
</span> '''

'''
==============================================================
Find the jobs by CSS selector
============================================================== 
'''
jobs = driver.find_elements_by_css_selector('div[class^=gwt-Label')

'''
==============================================================
Find job location(s) using CSS selector. 
--> for every <div> tag whos "class" attribute begins with "gwt-Label"
============================================================== 
'''
locations = driver.find_elements_by_css_selector('span[class^=gwt-InlineLabel')


'''
==============================================================
Dictionary (jobs_dict) to store job information. This dictionary 
will end up being a nested dictionary with each unique jobID being 
used as the key.
# jobs_dict = {_jobID_ : {'job_title': value0, 'job_location': value1, 'job_post_date': value2}, _jobID_: {...}, ... }
============================================================== 
'''
jobs_dict = {}

'''
==============================================================
Iterate through 'locations' element 
============================================================== 
'''
for k in locations:
    # get the text from each element in 'locations'
    line = k.text

    # condition used to check if the items in the locations list are actually what we are looking for
    if '|' not in line:
        continue
    line = line.split('|')
    j_id = line[0].strip()
    j_location = line[1].strip()
    j_post_date = line[2].strip()

    # add values into the jobs_dict dictionary 
    # the 'job_title' is filled with a temporary value (None) I added in the for loop below
    jobs_dict[j_id] = {'job_title': None, 'job_location': j_location, 'job_post_date': j_post_date}
    

'''
==============================================================
Iterate through 'jobs' element
============================================================== 
'''
# this for loop iterates through my_dict and adds the job title each unique jobID key
for f in jobs:
    # get the text for each element in 'jobs'
    line = f.text

    # condition used to check if the items in the locations list are actually what we are looking for
    if line.strip() == "":
        continue

    # below is where we need to check for the temporary value (None), 
    # and if its found, replace it with the job title (line)
    for c in jobs_dict:
        if jobs_dict[c]['job_title'] == None:
            jobs_dict[c]['job_title'] = line
            break

'''
==============================================================
Get the total # of results displayed from job search query
============================================================== 
'''
results_count = soup.select("span[id$=Report_Entry]")
results_count = results_count[0].text
results_count = results_count.split()[0]

if int(results_count) == 0:
    print("NO JOBS FOUND")
    typeWriter("EXITING ...")
    driver.quit()
    sys.exit(0)

print("\nJOB POSTINGS (%s)\n%s" % (site_title.upper(), '-'*50))
count_jobs = 1

'''
==============================================================
Here is where the jobs and its details are displayed.
Jobs are displayed in the following manner:

#. Job_Title
    JobID   : _______
    Location: _______
    Date    : _______
    Link    : _______
============================================================== 
'''
#my_file = open('/Users/nicholausbrell/Desktop/jobs.txt', 'a')
for job_id in jobs_dict.keys():
    # grab values from our dictionary 'jobs_dict'
    job_title = jobs_dict[job_id]['job_title']
    job_location = jobs_dict[job_id]['job_location']
    job_post_date = jobs_dict[job_id]['job_post_date']

    link = workday_linkgen.linkGen(job_title, job_location, job_id, site_title)

    print("%d. %s" % (count_jobs, job_title))
    print("\tJobID   : %s\n\tLocation: %s\n\tDate    : %s\n\tLink    : %s\n\n" % (job_id, job_location, job_post_date, link))
    
    #my_file.write("%d. %s\n" % (count_jobs, job_title))
    #my_file.write("\tJobID   : %s\n\tLocation: %s\n\tDate    : %s\n\tLink    : %s\n\n" % (job_id, job_location, job_post_date, link))
    count_jobs += 1

#my_file.close()
driver.quit()
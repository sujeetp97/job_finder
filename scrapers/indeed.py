# -*- coding: utf-8 -*-

from urllib import parse
import requests
from lxml import html
import pandas as pd

#CHROMEDRIVER_PATH = "C:/Users/sujit/OneDrive/Documents/Work/Job Finder/res/chromedriver"
#driver = webdriver.Chrome(CHROMEDRIVER_PATH)

# Job Search
#job = "Data Scientist $105,600"
#location = "Tampa, FL"
#url = 'https://www.indeed.com/jobs?q=' + parse.quote_plus(job) + "&l=" + parse.quote_plus(location)
##driver.get('https://www.indeed.com/jobs?q=' + parse.quote_plus(job) + "&l=" + parse.quote_plus(location))
#

def scrape_jobs(max_page_index = 100):
    
    skill_search = {
            "Data Science" : 10,
            "Data Scientist" : 10,
            "Business Intelligence" : 10,
            "R Language" : 9,
            "R Program" : 9,
            "R Develop" : 9,
            "R Cod" : 9,
            "R Model" : 9,
            "Python" : 9,
            "Tableau" : 9,
            "Alteryx" : 9,
            "Data Analyst" : 4,
            "Regression" : 5,
            "Forecast" : 5,
            "ARIMA" : 5,
            "Classification" : 5,
            "Senior" : 1
            }
    
    next_page_link = ""
    next_page_nums = [1]
    job_titles = []
    job_companies = []
    job_links = []
    job_descriptions = []
    jobs_found_cnt = 0
    duplicate_jobs_found_cnt = 0
    for page_index in range(max_page_index):
        # Enter URL for first iteration and then prepare URL with next page's link
        if page_index == 0:
            job = "Data Scientist"
            location = "Tampa, FL"
            url = 'https://www.indeed.com/jobs?q=' + parse.quote_plus(job) + "&l=" + parse.quote_plus(location)
        else:
            url = 'https://www.indeed.com' + next_page_link
        
        print("\nPage " + str(page_index + 1) + " : ", end = "")
        job_page = requests.get(url) # Get the Job Page Response
        tree = html.fromstring(job_page.content)
        
        # Extracting job details
        titles = tree.xpath("//*[@class='jobsearch-SerpJobCard unifiedRow row result']//*[@class='title']/a")
        companies = tree.xpath("//*[@class='jobsearch-SerpJobCard unifiedRow row result']//*[@class='company']")
        
        for index in range(len(titles)):
            jobs_found_cnt += 1
            if len(companies[index].getchildren()) > 0 :
                companies[index] = companies[index].getchildren()[0] # Companies can have a span within span or just 1 span element.
    #        print("\n" + titles[index].get('title') + " \t::\t " + companies[index].text.strip() + " :: " + titles[index].get('href'))  
            
            # If link is found duplicate, go to next job
            if titles[index].get('href') in job_links:
                print("|", end = "")
                duplicate_jobs_found_cnt += 1
                continue
            
            # Extracting Job Description
            company_url = 'https://www.indeed.com' + titles[index].get('href')
            company_page = requests.get(company_url)
            company_tree = html.fromstring(company_page.content)
            job_description = company_tree.xpath("//div[@class='jobsearch-jobDescriptionText']")
            if("list" in str(type(job_description))):
                job_description = html.tostring(job_description[0])
            
            # If JD is found duplicate, go to next job
            if job_description in job_descriptions:
                print("*", end = "")
                duplicate_jobs_found_cnt += 1
                continue
            
            print(".", end = "")
            
            job_links.append(titles[index].get('href'))
            job_titles.append(titles[index].get('title'))
            job_companies.append(companies[index].text.strip())
            job_descriptions.append(job_description)
            
       
        # Getting the next page link    
        pagination = tree.xpath("//*[@class='pagination']/a/span/span") # Only Previous and Next can have span within span, numbers have only 1 span
        
        next_page_link = ""
        for page in pagination:
            # Next Button dissapears on the last page
            if "NEXT" in str(page.text).strip().upper():
                next_page_link = page.getparent().getparent().get('href')
        
        if next_page_link == "":
            print("scraped.")
            print("All pages have been scraped!")
            break
        else:
            print("scraped.")
        
    
    print("Found " + str(jobs_found_cnt - duplicate_jobs_found_cnt) + " jobs. (" + str(duplicate_jobs_found_cnt) + " duplicates removed)")
    
    job_list = {'TITLE' : job_titles, 'COMPANY' : job_companies, 'LINK' : job_links, 'JD' : job_descriptions}
    job_table = pd.DataFrame(job_list, index = range(len(job_titles)))
    
    print("Analyzing Job Description")
    relevance_list = []
    for index in range(len(job_table)):
        jd = ' '.join(str(job_table['JD'][index]).lower().split())
        relevance = 0
        for word in skill_search:
            relevance += (  skill_search[word] * jd.count(word.lower()) )
        relevance_list.append(relevance)
    
    job_table['RELEVANCE'] = relevance_list


#from tkinter import *
#root = Tk()
#top_frame = Frame(root)
#top_frame .pack()
#bottom_frame = Frame(root)
#bottom_frame .pack(side = BOTTOM)
#
#head_label = Label(top_frame, text = "Indeed Job Infos")
#head_label.pack()
#refresh_btn = Button(bottom_frame, text = "Refresh List", fg = "white", bg = "green")
#refresh_btn.pack(side = LEFT)
#close_btn = Button(bottom_frame, text = "Close", fg = "white", bg = "black")
#close_btn.pack(side = RIGHT)
#
#root.mainloop()




    
    print("Done")
    return(job_table)
# See detail of a job


# Keyword Check for checking relavance


# Present links with relavance

#time.sleep(120) # Let the user actually see something!
#driver.quit()


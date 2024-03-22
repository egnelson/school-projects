DB_Final_Project_Website
========================

A website developed as the final project for my databases class in the winter quarter of 2014.

##What is implemented?

* Employer accounts:
  * Contact info
  * CRUD job posting
  * CRUD event posting
* Job seeker accounts
  * Save job and event postings for later reference
* Job and event searching searches:
  * Description text
  * Job title
  * Event name
  * Location

---

##Testing Instructions

###Setup and Starting the Server

* Install a Linux VM (I used Fedora 20)

* Using the package manager, install python 3 and pip, the python package manager)

  (python3 and python3-pip in Fedora 20)

* As root, use pip to install django 1.6: `# pip install django1.6`

  (In Fedora 20: `# python3-pip install django1.6`)

* As a normal user (still in the terminal), go to the 'website' directory in the cloned repository

* Run `$ python3 ./manage.py runserver`, leaveing the terminal running.

* Open up the web browser to "localhost:8000"

###Testing!

* Before logging in, please test the search functionality. You can choose to search for jobs or events in the drop-down box to the left of the search bar. 

* If you leave the search field empty, it will display all jobs or events.

* There are several example jobs, users, and events.

* When you're done testing the search, go to localhost:8000/admin, login (username 'admin', password 'admin'), and click on 'Users' to view all the users. All but one (asdf, a job seeker account) is an employer account.

* Each user's password is the same as the username (of course, I wouldn't do this in a live website).

* Go ahead and log in as one of the employers (any except admin or asdf).

* Play around with the jobs and events- you can create, view, edit, and delete jobs and events. Don't forget to try searching for them!

* Log out, then log back in as 'asdf' (password 'asdf')

* asdf should be following no jobs or events

* Search for a job or event and click on a view link

* At the bottom of the job/event table, there should be a button that says 'Watch'. Click on it. This creates a row in the WatchedJob (or WatchedEvent) table, and redirects back to the home page. You should see a new entry in the watched job (or event) list.

---

##Leftovers from the assignment readme

###WHAT I IMPLEMENTED

* Employer: can create, update, delete jobs.

* job seeker (signed in): can view, watch and unwatch jobs

* job seeker (anonymous): can view jobs

###IMPLEMENTED EXTRA CREDIT 

* Events and related employer functionality (create, update, delete)

* Job seeker- watch/unwatch events

* sign up and login for job seekers and employers

* Administration site (using Django's excellent administration tools)

* Job and event search

###WHAT I IMPLEMENTED THAT WASN'T IN THE PROPOSAL

* A searching function that appears on most pages when an applicant is browsing.

###WHAT I DIDN'T IMPLEMENT FULLY

* Job seeker: view employer info pages- There are no links anywhere to the public employer pages, so only someone who knew the correct url would be able to view them.

###WHAT SHOULD HAVE BEEN IN THE PROPOSAL

* Search function: there was no way to discover jobs and events in the original proposal. This is an important function of a job website, and I overlooked it.


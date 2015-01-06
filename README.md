Island.byu.edu
======


This repository hosts the code for the student/alumni forum at BYU's Information Systems department. We host it on GitHub so any student in the program can contribute to the code.  We hope many students will work to make the site fantastic.

# Description

Island.byu.edu is comprised of two parts:

* A set of forums that can be accessed via the web or via email.  This functionality is live and running.
* A "My Service" area that both alumni and students can complete to contribute to the department.   Service opportunities are posted often, and they include things like reviewing a few student resumes, answering student questions, reading/contributing to the newsletter, contributing to the forum topics, reviewing class curriculum, coding on the site, etc.  This section of the site is not fully functional yet.


# Installation

The code is built on top of Django, Python 3, Django-Mako-Plus, and Postgresql.  You need to have all of these technologies installed on your computer to get the code running.

The following is a quick installation guide.  As one of you install, please make this more complete so others can install more easily.

## PostgreSQL

Install PostgreSQL, the database we use for Island.  It is at http://www.postgresql.org/. 

Create a database named `thecproject`, username `thecproject`, password `thecproject2014`.  This will be your development database. See the settings.py file for the full DB settings.

## Python 3

Install Python 3 (http://www.python.org) on your machine.  Ensure you can run "python3" from the command line.  Then install PIP (https://pip.pypa.io/en/latest/installing.html).

Finally, install several additional libraries.  Some of these are complex and may be more easily installed by downloading an installation package (such as MSI on Windows).  The difficult ones are noted:

* pip3 install django              # framework
* pip3 install mako                # templating language
* pip3 install django-mako-plus    # connects django to mako
* pip3 install lxml                # xml parser (this might be easier to install via a binary installation package)
* pip3 install psycopg2            # database driver (this might be easier to install via a binary installation package)
* pip3 install django-jsonfield    # allows json in models
* pip3 install shortuuid           # creates short guids
* pip3 install rjsmin              # for filters.py



## Download the Code

For Windows users, you need to install Git on your machine (see https://windows.github.com/).  Mac and Linux users already have Git.  

Create an empty directory, then download the code from https://github.com/doconix/island.  You don't need a password to download the code, but you won't be able to commit changes until you are granted rights (see Dr. Albrecht).

# Committing Your Changes

Before working, always pull the most recent changes from GitHub: `git pull origin master`.

When you are finished working, commit changes back to GitHub: `git commit` and `git push origin master`.  Note that you can only commit changes if you have been granted rights by Dr. Albrecht.

# Notes

Some random notes about the system.

## CAS Authentication

We included the django_cas_ng module directly in our code because we had to change some of it to work right with Py3 and BYU's CAS server.  We didn't document all the changes,
but they are all in views.py and backend.py.  Run diff on these files if you need to upgrade it.


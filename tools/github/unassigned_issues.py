#!/usr/bin/env python

import sys, os, getpass, datetime
from github import Github
from github_issues import GithubIssues

repo_full_name = 'autotest/virt-test'

gh = Github(login_or_token=raw_input("Enter github username: "),
            password=getpass.getpass('Enter github password: '),
            user_agent='PyGithub/Python')
print

issues = GithubIssues(gh, repo_full_name)

print "Enter github labels, blank to end:"
labels = []
while True:
    label = raw_input("labels[%d]" % (len(labels) + 1))
    label = label.strip()
    if label:
        try:
            # http://jacquev6.github.io
            #       /PyGithub/github_objects/Label.html#github.Label.Label
            labels.append(issues.get_gh_label(label).name)
        except ValueError, detail:
            print str(detail)
    else:
        break
print

criteria = {'state':'open', 'assignee':'none', 'labels':labels,
            'sort':'updated', 'direction':'desc'}

heading = ("Unassigned %s issues from %s, oldest-first"
           % (",".join(labels), repo_full_name))
print heading
print "-" * len(heading)
print

for number in issues.search(criteria):
    print issues[number]['url']

# make sure cache is cleaned and saved up
del issues

print

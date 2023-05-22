from atlassian import Jira
from dotmap import DotMap
import os, sys, re

'''
Add JIRA_USERNAME & JIRA_ACCESS_TOKEN to the environment variables for the JIRA access
'''

class JiraTest():
    def __init__(self):
        self.jira = Jira(
        url='https://portworx.atlassian.net',
        username=os.getenv("JIRA_USERNAME"),
        password=os.getenv("JIRA_ACCESS_TOKEN"),
        cloud=True
        )

    def get_issue_by_id (self, id=None):
        issue = self.jira.issue(id)
        issue = DotMap(issue)
        return issue
    
    def get_issues_by_jql (self, jql=None):
        issues = self.jira.jql(jql)
        issues = DotMap(issues)
        issues = self.extract_imp_fields (issues)
        return issues
    
    def extract_imp_fields (self, input):
        issues = []
        for i in range(input.total):
            issue = {}
            issue["id"] = str(input.issues[i].key)
            issue["status"] = str(input.issues[i].fields.status.name)
            issue["project"] = str(input.issues[i].fields.project.name)
            issue["summary"] = str(input.issues[i].fields.summary)
            issue["assignee"] = str(input.issues[i].fields.assignee.displayName)
            issue["reporter"] = str(input.issues[i].fields.reporter.displayName)
            lastComment = str(input.issues[i].fields.comment.comments[-1].body)
            if "accountid" in lastComment:
                lastComment = self.replace_account_id(lastComment)
            issue["lastComment"] = "{} : {}".format(str(input.issues[i].fields.comment.comments[-1].author.displayName), lastComment)
            issues.append(issue)
        return issues
    
    def replace_account_id(self, input_string):
        for acc_id in re.findall(r'\[~accountid:\w+\]', str(input_string)):
            acc_id_num = acc_id.split(':')[1][:-1]
            username = self.jira.user(account_id='{}'.format(acc_id_num))['displayName']
            input_string = input_string.replace(acc_id, "@{}".format(username))
        return input_string
        
if __name__ == "__main__":
    jira = JiraTest()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "Give me open issues reported by me":
            jql = "status = Open AND reporter = currentUser()"
        if sys.argv[1] == "Give me issues that needs to be verified by me":
            jql = "status = Done AND Verifier = currentUser()"
        # if sys.argv[1].startswith("Give me issues reported by "):
        #     jql = "reporter in (\"{}\")".format(sys.argv[1].split()[-1])
        issues = jira.get_issues_by_jql(jql)
        print(issues)
# AWS_workspaces_activity_report
If you're tasked with reviewing a large number of workspaces and assessing user activity, a simple script can assist you in generating a comprehensive report.

To generate this report, you'll need to utilize both the AWS CLI and Python:

a) Begin by using the command:
aws workspaces describe-workspaces --directory-id <d-XXXXX> >workspaces.json

b) Next, execute the convert.py script.

c) Finally, run the report.py script.

Ensure all Python commands are executed from your command line interface (CLI).

Your resulting report will be named: workspaces_report.html.

from metasdk import MetaApp

META = MetaApp()

IssueService = META.IssueService

test_issue_id = 12067
IssueService.add_issue_msg(test_issue_id, "robo test")
IssueService.done_issue(test_issue_id)

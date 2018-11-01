import os

from metasdk import MetaApp
from metasdk.utils import pretty_json

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(os.path.abspath(__file__)))
__DIR__ = os.getcwd() + "/"

reports = [
    "campaign_stats_report",
    "campaign_goal_stats_report",
    "campaign_calls_stats_report",
    "campaign_depth_stats_report",
    "campaign_orders_stats_report",
    "campaign_avg_depth_stats_report",
]

metaql = META.MetaqlService

for report_name in reports:
    resp = metaql.get_schema("adplatform", report_name)
    print(u"report_name = %s" % str(report_name))
    print("Schema:\n")
    print(pretty_json(resp))

log.info("end")

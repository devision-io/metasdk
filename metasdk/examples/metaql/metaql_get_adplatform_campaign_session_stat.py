import os

from metasdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

q = """
SELECT
  channel_name,
  ROUND( COALESCE(SUM(pageviews) / NULLIF(SUM(sessions), 0), 0) , 2) as pv
FROM adplatform.campaign_avg_depth_stats_report
WHERE stat_date BETWEEN '2017-08-01' AND '2017-08-31'
AND system = 'googleAnalytics'
and client_id=1460
GROUP BY channel_name
ORDER BY channel_name
"""

configuration = {
    "download": {
        # "skipHeaders": True,
        "dbQuery": {
            "command": q
        }
    }
}
META.auth_user_id = 10191
metaql = META.MetaqlService
resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/campaign_sessions_stats_report.tsv')
log.info("end")

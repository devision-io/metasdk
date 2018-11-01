import os

from metasdk import MetaApp

META = MetaApp()
log = META.log

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"

q = """
SELECT
  engine as platform,
  campaign_remote_id,
  SUM(impressions) as impressions,
  SUM(clicks) as clicks,
  1.0 * SUM(clicks) / NULLIF(SUM(impressions), 0) * 100 as ctr,
  ROUND(SUM(cost), 3) as cost
FROM adplatform.campaign_stats_report
WHERE stat_date BETWEEN '2017-03-01' AND '2017-03-31'
GROUP BY platform, campaign_remote_id
ORDER BY platform, campaign_remote_id
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
resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/campaign_stats_report.tsv')
log.info("end")

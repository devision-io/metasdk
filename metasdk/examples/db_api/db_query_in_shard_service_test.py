from metasdk import MetaApp
from metasdk.utils import pretty_json

META = MetaApp(meta_url="https://meta.realweb.ru")
log = META.log

log.info('start')
try:
    db_general = META.db("garpun_main")
    camps = db_general.all("""
        SELECT
            "adHandsCampaignId" as id,
             name,
             "accountId" as account_id,
             "campaignRemoteId",
             "engine"
        FROM global.campaigns
        WHERE "virtualCampaignId" > 0
        LIMIT 2
    """)
    for camp in camps:
        storage_db = META.db("garpun_storage", camp['account_id'])
        search_params = {"engine": camp['engine'], "camp_remote_id": camp['campaignRemoteId'],}
        res = storage_db.one("""
            SELECT count(1) as ads_cnt
            FROM #shard.ads
            INNER JOIN #shard."campaigns" c USING("campaignLocalId")
            INNER JOIN #shard."virtualCampaigns" vc USING("virtualCampaignId")
            WHERE vc.engine=:engine::"enum_engineType" AND c."campaignRemoteId"=:camp_remote_id
        """, search_params)
        camp.setdefault('counter', {})
        camp['counter']['ads'] = res['ads_cnt']

        res = storage_db.one("""
            SELECT count(1) as phrases_cnt
            FROM #shard."conditionsPhrases"
            INNER JOIN #shard.ads USING("adLocalId")
            INNER JOIN #shard."campaigns" c USING("campaignLocalId")
            INNER JOIN #shard."virtualCampaigns" vc USING("virtualCampaignId")
            WHERE vc.engine=:engine::"enum_engineType" AND c."campaignRemoteId"=:camp_remote_id
        """, search_params)
        camp['counter']['phrases'] = res['phrases_cnt']
    print(pretty_json(camps))
finally:
    log.info('finish')

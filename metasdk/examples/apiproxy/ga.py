from metasdk import MetaApp

META = MetaApp()


refresh_token ="XXXXX"
ga_property_id = 'XXXX'

resp = META.ApiProxyService.call_proxy("google_analytics", {
    "refresh_token": refresh_token,
    "version": "v4",
    "method": "reports.batchGet",
    "method_params": {
        "body": {
            # "useResourceQuotas": True, # Включение привелений GA360
            "reportRequests": [
                {
                    "viewId": ga_property_id,
                    "dateRanges": [
                        {
                            "startDate": "2015-06-15",
                            "endDate": "2015-06-30"
                        }],
                    "metrics": [
                        {
                            "expression": "ga:sessions"
                        }],
                    "dimensions": [
                        {
                            "name": "ga:browser"
                        }]
                }]
        }
    }
}, "native_call", False, [])
print(u"resp = %s" % str(resp.text))

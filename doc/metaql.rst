======
METAQL
======

Основан на синтаксисе Oracle
METAQL - Это защищенный SQL для запросов к данным меты.

Особенности
-----------
- Нельзя называть поля или алясы зарезарвированными именами: date
- Добавлен оператор ILIKE для регистронезависимного сравнения строк
- Пока нет прообразований типов
- Поддерживаются только SELECT запросы
- JOIN пока не поддерживаются

Функции
-------
Работают функции агрегации:
 - MIN, MAX, SUM, AGV
 - COUNT(*), COUNT(DISTINCT поле)

Функции преобразований:
 - ROUND
 - CONCAT
 - NULLIF
 - COALESCE

Примеры
-------

`Полный список metaql примеров
<https://github.com/devision-io/metasdk/tree/master/metasdk/examples/metaql>`_

`Список отчетов
<https://github.com/devision-io/metasdk/tree/master/metasdk/examples/metaql/metaql_get_schema.py>`_

.. code-block:: python

    import os
    from metasdk import MetaApp

    META = MetaApp()
    log = META.log

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    __DIR__ = os.getcwd() + "/"

    q = """
    SELECT
      engine as platform,
      campaign_remote_id,
      SUM(impressions) as impressions,
      SUM(clicks) as clicks,
      ROUND(SUM(cost), 3) as cost
    FROM adplatform.campaign_stats_report
    WHERE stat_date BETWEEN '2017-02-01' AND '2017-03-31'
    AND engine = 'banner'
    GROUP BY platform, campaign_remote_id
    ORDER BY platform, campaign_remote_id
    """

    configuration = {
        "download": {
            # "skipHeaders": True,
            "dbQuery": {
                "command": q,
            }
        }
    }
    metaql = META.MetaqlService
    resp = metaql.download_data(configuration, output_file=__DIR__ + 'assets/stat.tsv')
    log.info("end")


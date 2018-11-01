from metasdk import MetaApp
from metasdk.utils import pretty_json

META = MetaApp()
log = META.log

#
# Db.one
#
db_adplatform = META.db("adplatform")
u = db_adplatform.one("""
    SELECT id, name, info
    FROM users
    WHERE id = -1
    LIMIT 1
""")
# Выдаст None
print(u"u = %s" % u)

#
# Db.query
#
db_adplatform = META.db("adplatform")
dr = db_adplatform.query("""
    SELECT id, name, info
    FROM users
    WHERE name ILIKE 'Андре%'
    ORDER BY name
    LIMIT 1
""")
print(u"dr = %s" % pretty_json(dr))

for r in dr['rows']:
    print("\n")
    print(u"r['id'] = %s" % r['id'])
    print(u"r['name'] = %s" % r['name'])
    print(u"r['info'] = %s" % pretty_json(r['info']))

db_adhands_ui = META.db("adhands_ui")
dr = db_adhands_ui.query("""
    SELECT id, name
    FROM user
    WHERE name LIKE :uname
    AND id IN ( :ids )
    ORDER BY name
    LIMIT 3
""", {
    "uname": "Андре%",
    "ids": [8734, 3840]
})

for r in dr['rows']:
    print("\n")
    print(u"r['id'] = %s" % r['id'])
    print(u"r['name'] = %s" % r['name'])

db_adhands_ui = META.db("adhands_ui")
user = db_adhands_ui.one("""
    SELECT id, name
    FROM user
    WHERE id=:id
""", {"id": 4501})
print(u"user = %s" % pretty_json(user))

#
# Db.update
#
db_meta_samples = META.db("meta_samples")
dr = db_meta_samples.update("""
    UPDATE counters SET inc = inc + 1 WHERE name = :name
""", {"name": "md_source_update"})
print(u"dr = %s" % pretty_json(dr))

# Db.batch_update

db_meta_samples = META.db("meta_samples")
dr = db_meta_samples.batch_update("""
    INSERT INTO test_batch_update VALUES (:id, :mytime::timestamp)
    ON CONFLICT(id) DO UPDATE SET mod_time=NOW()
""", [
    {"id": "py_1", "mytime": "2014-01-01"},
    {"id": "py_2", "mytime": "2014-01-01"},
])
print(u"dr = %s" % pretty_json(dr))

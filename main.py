import requests
import json
import sys
import psycopg2

from src import config

def get_data_from_twx(entity, services=None):
    # GET
    if not services:
        url = "{}/Things/{}/Properties".format(config.twx_url, entity)
        response = requests.get(url, headers=config.twx_headers, data={})

    # POST
    if services:
        url = "{}/Things/{}/Services/{}"\
            .format(config.twx_url, entity, services.get("method", None))
        response = requests.post(url, headers=config.twx_headers)

    if not response.content:
        return None

    response_data = json.loads(response.content.decode("latin1"))
    return response_data["rows"]

def insert_data(data, table_name, on_duplicate=None, on_duplicate_update=None, conn=None):

    # INSERT INTO query
    cols = list(data[0].keys())
    cols_str = ", ".join(cols)
    vals_str = ", ".join(["%({})s".format(val) for val in cols])
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, cols_str, vals_str)

    # If needed to update existing columns
    if on_duplicate and on_duplicate_update:
        sql += " ON CONFLICT ({}) DO UPDATE SET ".format(on_duplicate)
        sql += ", ".join(["{0} = excluded.{0}".format(update_col) for update_col in on_duplicate_update])

    # Init connection if not
    own_conn = False
    if not conn:
        own_conn = True
        host = config.db_remotehost
        name = config.db_name
        user = config.db_user
        conn = psycopg2.connect("host={0} dbname={1} user={2}".format(host, name, user))

    # Get cursor
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()

    # End
    if own_conn:
        conn.close()
        cur.close()

if __name__ == "__main__":

    # Params

    # Get data
    data = get_data_from_twx("Assy_Line_Station_0_DT", services={'method': 'GetDataTableEntries'})

    # Process data


    # Init connection
    conn = psycopg2.connect("host={0} dbname={1} user={2}".format(config.db_remotehost,
                                                                  config.db_name,
                                                                  config.db_user))

    # Insert data
    data = [{"text1": i, "text2": "haha"} for i in range(10)]
    insert_data(data, "test_table", "time", ["text1", "text2"], conn=conn)

    # End connection
    conn.close()
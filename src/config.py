# Switch
isDev = False

# Database
db_remotehost = '192.168.129.26'
db_localhost = 'localhost' # local
db_port = '5432'
db_user = 'postgres'
db_name = 'kpi' # database

# TWX config
twx_token = 'bWljcjptaWNy'
twx_url = 'http://192.168.128.51:8080/Thingworx'
twx_headers = {
    'Authorization': 'Basic {0}'.format(twx_token),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
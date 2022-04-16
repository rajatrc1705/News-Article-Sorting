from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def connect():
    # configuration
    cloud_config= {
            'secure_connect_bundle': '/home/rajat/Downloads/secure-connect-news-articles.zip'
    }

    # authentication details
    auth_provider = PlainTextAuthProvider('dZwqwPnfhMcUHZOuLrrPygWI', 'r7a0dE0jk4t7H0zOHwLPnhOLslkEdm-,tLtquJkUXbza0bCQgsXAT3A_w7d+Ol5A8hXHYJWPQ5_nL,CA,lfqREBxZ58,jaRB4Z2gig9lWyAi9-E4pZW7RpmBkwHEAovB')

    # connecting to cluster using configuration and authentication details
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    # using the session we can execute commands on the cassandra database
    row = session.execute("select release_version from system.local").one()

    # checking for a successful query
    if row:
        print("Connection Successful: ", row[0])
    else:
        print("An error occurred.")
    return session
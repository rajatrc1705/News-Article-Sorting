from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def connect():

    # configuration
    cloud_config= {
            'secure_connect_bundle': r"C:\Users\rajat\Downloads\secure-connect-news-articles.zip"
    }

    # authentication details
    auth_provider = PlainTextAuthProvider('KQXuSjNiyLpIXJSpjwhZHSmD', 'ilouHT6e.xn_LaXhxZ-WAdi0wwR-2.wQFe.-0Nawqv+TDAEO+RF-cZe9WrLzPB+_26eKQWBLgbAO61l5.RtYqqS2GPsmZTNe0,fTFJlIo7+Um+pRKWtUOA8-0Qgr0edl')

    # connecting to cluster using configuration and authentication details
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    # using the session we can execute commands on the cassandra database
    row = session.execute("select release_version from system.local").one()

    # checking for a successful query
    if row:
        print(row[0])
    else:
        print("An error occurred.")
      
    return session
import streamlit as st

# not really much here - I use Mongo as database


@st.cache_resource
def init_connection():
    max_idle_time = 3  # minutes
    max_server_select_time = 2  # seconds
    connection = (
        f"mongodb://{st.secrets.mongo.user}:{st.secrets.mongo.password}"
        f"@{st.secrets.mongo.ip}:27017/"
        "?directConnection=true&retryWrites=true&w=majority"
        f"&serverSelectionTimeoutMS={max_server_select_time * 1000}"
        f"&maxIdleTimeMS={max_idle_time * 60000}"
    )
    # no connection in this example :)
    # return MongoClient(connection)
    return True


def database_instance(mode):
    return 0, 1

    # I used different databases for dev and prod
    mongo = init_connection()
    if mode == "DEVELOPMENT":
        return mongo.dev_app_main, mongo.dev_app_support
    return mongo.app_main, mongo.app_support


# since I cache the connection resource, I can run once the DB instance here
DBM, DBS = database_instance(st.secrets.mongo.level)
print(f"> Logged in {st.secrets.script.mode} mode")

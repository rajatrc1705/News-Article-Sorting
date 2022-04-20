from python_project import connect_database
import pandas as pd
import logging

def get_session():
    """
    Description: Gets session after successfully connecting with database.
    Params: None
    Returns: session
    """
    # connecting to the database and creating a session 
    try_again = True
    while try_again:
        try:
            session = connect_database.connect()
            try_again = False
        except:
            logging.error("Connection attempt failed! Trying again")
            try_again = True
            
    return session


def display_data(limit = 20):
    
    
    session = get_session()
    
    row = session.execute("SELECT * FROM news_articles.train_2").all()
    print("="*20)
    count = 0
    for r in row:
        count += 1
        if count == limit:
            break
        print(r)
    print("="*20)
    

def insert_query(query, display=False):
    
    session = get_session()
    
    row = session.execute(query)
    row = session.execute("SELECT * FROM news_articles.train_2").all()
    if display:
        display_data()
        
        
def delete_query(id_=0):
    
    session = get_session()
    
    if id_ == -1:
        query_delete_one = "DELETE FROM news_articles.train_2"
    else:
        query_delete_one = "DELETE FROM news_articles.train_2 WHERE article_id = {};".format(id_)
    
    row = session.execute(query_delete_one)
    
    row = session.execute("SELECT * FROM news_articles.train_2").all()
    if len(row) == 0:
        print("Deletion Successful👍️")
    else:
        print("Something doesn't feel right!")
        print(row)
        
        
def get_dataframe():
    
    session = get_session()
    row = session.execute("SELECT * FROM news_articles.train_2").all()
    article_id_list = list()
    news_list = list()
    category_list = list()
    
    for r in row:
        article_id_list.append(r.article_id)
        news_list.append(r.text)
        category_list.append(r.category)
    
    data_db = pd.DataFrame({
        'article_id': article_id_list,
        'news': news_list,
        'category': category_list
    })
    
    return data_db
import pandas as pd
import datetime
import sys

def spliter(filename):
    
    df = pd.read_json(filename, lines = True,  compression = 'gzip')

    visits_main = []
    hits_main = []
    
    for index, line in df.iterrows():
        
        visits = [index]
        hits = [index]
        
        for item_visits in [line['fullVisitorId']
                  , line['visitId']
                  , line['visitNumber']
                  , line['visitStartTime']
                  , line['device']['browser']
                  , line['geoNetwork']['country']]:
            visits.append(item_visits)
            
        for item_hits in [line['hits'][0]['hitNumber']
                , line['hits'][0]['type']
                , line['hits'][0]['page']['pagePath']
                , line['hits'][0]['page']['pageTitle']
                , line['hits'][0]['page']['hostname']
                , line['visitStartTime']
                , datetime.datetime.fromtimestamp(float(line['hits'][0]['time'])/1000.0)]:
            hits.append(item_hits)

        hits_main.append(hits)
        visits_main.append(visits)

    hits_df = pd.DataFrame(hits_main)
    visits_df = pd.DataFrame(visits_main)
    
    hits_df.columns = ['key', 'hit_number', 'hit_type', 'hit_timestamp', 'page_path', 'page_title', 'hostname', 'country']
    visits_df.columns = ['key', 'full_visitor_id', 'visit_id', 'visit_number', 'visit_start_time', 'browser', 'country']

    visits_df.drop_duplicates(['full_visitor_id', 'visit_id'], inplace = True)
    
    hits_df.to_json('hits.json', orient = 'records')
    visits_df.to_json('visits.json', orient = 'records')
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
	raise ValueError('Please provide file name.')
    filename = sys.argv[-1]
    spliter(filename)

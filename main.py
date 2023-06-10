import crawler
import mapping
import preprocessing
import model
import graph
import pandas as pd
import os

def crawling_skip(name) -> bool:
    for (path, dir, files) in os.walk("./data"):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if filename == name:
                return True
    return False

if __name__ == '__main__':
    pd.set_option('mode.chained_assignment',  None)
    if crawling_skip('whiskeybase.csv')  == False and crawling_skip('whiskeybase_raw.csv')  == False: 
        crawling_process = crawler.crawler()
        crawling_process.whisky_base_crawler()
        crawling_process.raw_data_preprocessing()
        
    mapping_process = mapping.mapping()
    mapping_process.main()
    preprocessing_process = preprocessing.preprocessing()
    whiskey_df = preprocessing_process.main()
    main_model_process = model.model(whiskey_df)
    main_model_process.main()
    graph_process = graph.graph(graph_num=4)
    graph_process.main()

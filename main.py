import crawler
import preprocessing
import os

def crawling_skip(name) -> bool:
    for (path, dir, files) in os.walk("./data"):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if filename == name:
                return True
    return False

if __name__ == '__main__':
    if crawling_skip('whiskeybase.csv')  == False and crawling_skip('whiskeybase_raw.csv')  == False: 
        crawling_process = crawler.crawler()
        crawling_process.whisky_base_crawler()
        crawling_process.raw_data_preprocessing()
    
    preprocessing_process = preprocessing.preprocessing()
    whiskey_df = preprocessing_process.main()
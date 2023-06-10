import crawler

if __name__ == '__main__':
    crawling_process = crawler.crawler()
    crawling_process.whisky_base_crawler()
    crawling_process.raw_data_preprocessing()
        
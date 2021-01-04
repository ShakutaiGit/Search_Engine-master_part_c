from search_engine_best import SearchEngine
from configuration import ConfigClass
if __name__ == '__main__':
    config = ConfigClass()
    sg = SearchEngine(config)
    sg.main()

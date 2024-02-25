class UsedUrlsSingleton:
    _instance = None
    _used_urls = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def used_urls(self):
        return self._used_urls

    def add(self, url):
        self._used_urls.add(url)

    def __iter__(self):
        return iter(self._urls)
    
    def if_here(self, url):
        if url in self._used_urls:
            return True
        return False

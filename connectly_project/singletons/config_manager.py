class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance
    
    def _initialize(self):
        if not hasattr(self, '_initialized') or not self._initialized:
            self.settings = {
                "DEFAULT_PAGE_SIZE": 20,
                "ENABLE_ANALYTICS": True,
                "RATE_LIMIT": 100
            }
        self._initialized = True
    
    def get_setting(self, key):
        self._initialize()
        return self.settings.get(key)
    
    def set_setting(self, key, value):
        self._initialize()
        self.settings[key] = value
        
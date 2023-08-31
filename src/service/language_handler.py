from langdetect import detect

# The structure and the __call__ method of this file was created following this site: https://refactoring.guru/design-patterns/singleton/python/example


# This class is the metaclass for LanguageHandler
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    

# This is the class that detects the language of the user's message.
# It is a Singleton because only one instance of _current_language
class LanguageHandler(metaclass=SingletonMeta):

    # This variable contains the current language used by the system to help the functions select the right message to show
    # Its default value is set to "en"
    _current_language = "en"
    
    def detect_language(self, message):
        self._current_language = detect(message)
        return self.get_current_language()
    
    def get_current_language(self):
        return self._current_language
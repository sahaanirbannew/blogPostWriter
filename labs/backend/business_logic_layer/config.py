import yaml


class Config:
    """
    This is the Configuration class. 
    The end user should be able to configure these variables in configuration.yaml.

    ---------------------------------------------------------------------
    Attributes                      | Configurable variables related to: 
    ---------------------------------------------------------------------
    ---------------------------------------------------------------------
    """
    config_file = 'configurations.yaml' 
    
    def __init__(self):   
        self.admin = self.admin()
        self.load_config(self.config_file)  
    
    class admin:
        def __init__(self): 
            self.language = None
    
    class openai:
        def __init__(self): 
            self.api_key = None
            self.model = None

            
    def load_config(self, config_file: str): 
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)       # load the configuration file
 
            self.openai.api_key =               config['openai']['key']
            self.openai.model =                 config['openai']['model']

            #self.admin.language =               config['admin']['language'] 
            pass
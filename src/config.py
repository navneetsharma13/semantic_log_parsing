import configparser

# Parse config.ini file
config = configparser.ConfigParser()
config.read('config.ini')


#Extract API keys
openai_api_key = config['OPENAI']['token']
openai_org_id = config['OPENAI']['org_id']
openai_proj_id = config['OPENAI']['proj_id']

claude_api_key = config['CLAUDE']['token']
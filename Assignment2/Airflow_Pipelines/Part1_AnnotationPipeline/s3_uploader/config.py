from configparser import ConfigParser
config = ConfigParser()

config.read('config.ini')
config.add_section('main1')
config.set('main1', 'bucket', 'edgarfile-storage')
config.set('main1', 'filepath', '/Users/prathyusha/Desktop/pranathi/Assignment2/airflow_edgar/dags/sec-edgar/call_transcripts')

with open('config.ini', 'w') as f:
    config.write(f)
Snowflake Pipeline:<br/>




**Getting Started**<br/>
Download & Configure Apache Superset from [here](https://superset.apache.org/docs/installation/installing-superset-from-scratch)<br/>
Connect to Apache Superset with connection string :<br/>
              **snowflake://{username}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}**<br/><br/>
*Python Libraries*<br/>
- ConfigParser<br/>
- sqlalchemy<br/>
- apache-superset<br/><br/>

**Usage**<br/><br/>

Using **snowflake_scripts**<br/>

Run this file in snowflake database to create tables/views and import data from S3 <br/><br/>

Using **config_file.ipynb** <br/>

Add the database connection details and run the file for setting up database connection parameters<br/><br/>

Using **SQLAlchemy.ipynb**<br/>

Run this file for querying the snowflake database<br/>

**Apache Superset Dashboard**













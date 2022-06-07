from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE Users (
   user_id INT NOT NULL AUTO INCREMENT,
   username VARCHAR(100) NOT NULL,
   password VARCHAR(40) NOT NULL,
   submission_date DATE,
   PRIMARY KEY ( user_id )
);
"""

result = DDLParser(ddl).run(output_mode="mysql")

import pprint
pprint.pprint(result) 

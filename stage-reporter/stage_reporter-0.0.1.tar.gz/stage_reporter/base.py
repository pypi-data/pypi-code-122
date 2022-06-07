#takes in list of headers 
# creates dict with header name: [empty list] paring 
#appending will happen based on colum id - another dict will be made with headers enumerated and have numbers as keys? or just use names 
class stage_reporter(): 
    #input list of headers 
    #def __init__(self):
        #self.cerate_frame()
        
        
    #method to create header dict 
    def create_report(self):
        report_dict = {'stage': [], 'execution_time': [], 'execution_type': []}
        self.report_dict = report_dict
        
    def update_headers(self,headers):
        self.headers = headers
                  
    #method to log stages 
    # need to be able to start and stop time - so need a method to start time and one ot stop - or both in on method based o nstage? 
    #execution types: 'start' or 'finish'
    def log_stage(self,stage_name,execution_type):
        self.stage_name = stage_name
        self.execution_type = execution_type
        self.exec_time = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        
        self.report_dict['stage'].append(self.stage_name)
        self.report_dict['execution_time'].append(self.exec_time)
        self.report_dict['execution_type'].append(self.execution_type)
        
    #create data frame fromnested dict 
    def create_frame(self):
        dataframe_report = pd.DataFrame.from_dict(self.report_dict)
        return dataframe_report

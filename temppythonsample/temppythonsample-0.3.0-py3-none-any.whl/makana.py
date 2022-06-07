import os
from temppythonsample.authService import Authentication
from temppythonsample.models import PipelineShape, PipelineConnection, Pipeline, PipelineShapeAttribute
import json
import uuid
import string
import random
pipelineShapes = []
pipelineShapeConnections : PipelineConnection = []
pipelineShapesId = []
pythonScriptShape : PipelineShape = []

class Makana():
    global baseUrl
    baseUrl = 'https://localhost:44350/'
    
    def getProjects():
        url = baseUrl + "api/makana/projects"
        response = Authentication.getRequest(url)
        if response.ok:
            result = response.json()
            print(json.dumps(result, indent=2))
            return result
        else:
            print(result)

    def getBaseImages():
        url = baseUrl + "api/makana/baseimages"
        response = Authentication.getRequest(url)
        if response.ok:
            result = response.json()
            print(json.dumps(result, indent=2))
            return result
        else:
            print(result)
    
    def createPipeline(name: str, projectId: int, baseImageId: int):
        url = baseUrl + "api/makana/pipelines"
        
        pipeline = json.dumps(Pipeline(0, name, projectId, baseImageId).__dict__)
    
        response = Authentication.postRequest(url,pipeline)
        
        if response.ok:
            global pipelineId
            result = response.json()
            pipelineId = result['id']
            print(json.dumps(result, indent=2))
        else:
            print("Error" + response.text)
    
    def getDataStores():
        url = baseUrl + "api/makana/workspace/datastores"

        response = Authentication.getRequest(url)
        if response.ok:
            results = response.json()
            for result in results:
                print(result['name'])
        else:
            print(result)
    
    
    def createSourceDataStep(name: str, blobStoreName: str, path: str):
        
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapesId.append(pipelineShapeId)
        internalName = name.lower().replace(" ", "_")
        global pipelineId
        pipelineId = 11
        global sourceDataShape
        
        PipelineShapeAttributes = []
        PipelineShapeAttributes.append(PipelineShapeAttribute(blobStoreName, 1).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute(path, 2).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 3).__dict__)
        
        sourceDataShape = PipelineShape(pipelineShapeId, 3, PipelineShapeAttributes, name, internalName, 
                                         1, 0, "assets/images/diagram/icon-none.svg", 0, 0, 0).__dict__
        
    def CreatePythonScriptStep(name: str, scriptFileDirectory: str, condaDependencies: str, pipPackages: str, arguments: list):
        
        scriptFileName = os.path.basename(scriptFileDirectory)
        internalName = name.lower().replace(" ", "_")
        
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapesId.append(pipelineShapeId)
       
        url = baseUrl + "api/makana/pipelines/uploadscript"
        
        data = {
            'pipelineId': pipelineId
        }
        
        files=[
            ('files',(scriptFileName,open(scriptFileDirectory,'rb'),'application/octet-stream'))
        ]
         
        response = Authentication.postRequest(url, data, files)
        if response.ok:
            result = response.json()
            print(json.dumps(result, indent=2))
        else:
            print("Error" + response.text)
        
        PipelineShapeAttributes = []
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 5).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute(scriptFileName, 6).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute(condaDependencies, 7).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute(pipPackages, 8).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute(arguments, 9).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 10).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 11).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 12).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 13).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 14).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 15).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 16).__dict__)
        
        step = PipelineShape(pipelineShapeId, pipelineId, PipelineShapeAttributes, name, internalName, 
                                         2, 0, "assets/images/diagram/icon-none.svg", 0, 0, 0).__dict__
                   
        pythonScriptShape.append(step)
         
    
    def createDataTransferStep(name: str, blobStoreName: str, path_on_datastore: str):
        
        internalName = name.lower().replace(" ", "_")
        
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapesId.append(pipelineShapeId)
        
        PipelineShapeAttributes = []
        PipelineShapeAttributes.append(PipelineShapeAttribute(blobStoreName, 17).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute(path_on_datastore, 18).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 19).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 20).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 21).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 22).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 23).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 24).__dict__)
        PipelineShapeAttributes.append(PipelineShapeAttribute("", 25).__dict__)
        
        global dataTransferShape
        
        dataTransferShape = PipelineShape(pipelineShapeId, pipelineId, PipelineShapeAttributes, name, internalName, 
                                         3, 0, "assets/images/diagram/icon-none.svg", 0, 0, 0).__dict__
        
    def savePipeline(name: str):
        
        pipelineShapes.append(sourceDataShape)
        for shape in pythonScriptShape:
            pipelineShapes.append(shape)
        pipelineShapes.append(dataTransferShape)    

        
        x = 450
        y = 80
        sortOrder = 1
        for pipelineShape in pipelineShapes:
            pipelineShape['sortOrder'] = sortOrder
            pipelineShape['x'] = x
            pipelineShape['y'] = y
            sortOrder+=1
            y+=100
        
        
        for id in range(0,len(pipelineShapesId)-1):
            randomId = ''.join(random.choices(string.ascii_lowercase +
                             string.ascii_uppercase + 
                             string.digits, k = 10))
            
            pipelineShapeConnection = PipelineConnection(pipelineId, pipelineShapesId[id], "bottom", randomId,
                                                          pipelineShapesId[id+1], "top").__dict__
            
            
            pipelineShapeConnections.append(pipelineShapeConnection)

        
        pipeline = json.dumps(Pipeline(pipelineId, name, 1, 1, pipelineShapes, pipelineShapeConnections).__dict__)
        
       
        url = baseUrl + "api/makana/pipelines/pipelineShapes"
        
        response = Authentication.postRequest(url, pipeline)
        if response.ok:
            # global pipelineResult
            result = response.json()
            print(json.dumps(result, indent=2))
            # return response.json()
        else:
            print("Error" + response)
        
        
    def getPipeline(pipelineId: int):
        url = baseUrl + "api/makana/pipelines/" + str(pipelineId)
    
        response = Authentication.getRequest(url)
        if response.ok:
            result = response.json()
            print(result)
            return result
        else:
            print("Error" + response)
            
    def runPipeline(pipelineId: int):
        pipelineResult = Makana.getPipeline(pipelineId)
        
        url = baseUrl + "api/makana/makanafunction/runrequest"
       
        pipeline = json.dumps(pipelineResult)
        
        # pipeline = pipelineResult
        
        response = Authentication.postRequest(url, pipeline)
        if response.ok:
            result = response.json()
            # print(result['id'])
            return response.json()
        else:
            print("Error" + response)
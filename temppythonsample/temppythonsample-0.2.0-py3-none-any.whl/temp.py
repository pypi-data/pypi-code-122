from inspect import Parameter
import json
import uuid
import string
import random
from authService import Authentication
import requests




class PipelineShapeAttributes:
    def __init__(self, attributeValue: str, shapeAttributeId: int):
            self.attributeValue = attributeValue
            self.shapeAttributeId = shapeAttributeId

class PipelineShapes:
     # init method or constructor
    def __init__(self, id : int, pipelineId: int, pipelineShapeAttributes: PipelineShapeAttributes, shapeDisplayName: str,
                 shapeInternalName: str, shapeId: int, sortOrder:int, statusImageUrl: int, stepOrder: int, x: int, y: int):
        self.id = id
        self.pipelineId = pipelineId
        self.pipelineShapeAttributes = pipelineShapeAttributes
        self.shapeDisplayName = shapeDisplayName
        self.shapeInternalName = shapeInternalName
        self.shapeId = shapeId
        self.sortOrder = sortOrder
        self.statusImageUrl = statusImageUrl
        self.stepOrder = stepOrder
        self.x = x
        self.y = y
        

class PipelineConnections:
    def __init__(self, pipelineId: int, From:  str, fromConnector: int, id: int, to: int, toConnector: str):
        self.pipelineId = pipelineId
        self.From = From
        self.fromConnector = fromConnector
        self.id = id
        self.to = to
        self.toConnector = toConnector

class Pipeline:
    # init method or constructor
    def __init__(self, id : int = None, name: str = None, projectId: int = None, baseImageId: int = None, pipelineShapes: PipelineShapes = None,
                 pipelineShapeConnections: PipelineConnections = None):
        self.id = id
        self.name = name
        self.projectId = projectId
        self.baseImageId = baseImageId
        self.pipelineShapes = pipelineShapes
        self.pipelineShapeConnections = pipelineShapeConnections

    # # Sample Method
    # def setPipeline(self):
    #     return self
    

# a = pipeline.setPipeline()
# print(a)

class Makana:
    def createPipeline(name, projectId, baseImageId):
        # authentication = Authentication
        # access_token_header = authentication.getToken()
        # url = "https://localhost:44350/api/makana/pipelines"
        # headers = {
        #     'Authorization': access_token_header,
        #     'Content-Type': 'application/json'
        # }
        shape1 = PipelineShapes("temp", 1, 1).__dict__
        shape2 = PipelineShapes("temp", 1, 1).__dict__
        shape : PipelineShapes = []
        shape.append(shape1)
        shape.append(shape2)
        
        pipeline = Pipeline(name, projectId, baseImageId, shape)
        abc=json.dumps(pipeline.__dict__)
        print(abc)
        # response = requests.post(url, headers=headers, data=abc, verify=False)
        # result = response.json()
        # if response.ok:
        #     global pipelineId
        #     pipelineId = result['id']
        #     print(json.dumps(result, indent=2))
        # else:
        #     print("Error" + response.text())
    def CreateSourceDataStep():
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapeAttributes = []
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 1))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 2))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 3))
        name = "Source Data"
        internalName = name.lower().replace(" ", "_")
        sourceDataShape = PipelineShapes(pipelineShapeId, 3, pipelineShapeAttributes, name, internalName, 
                                         1, 0, "assets/images/diagram/icon-none.svg", 0, 0, 0)
        
    def CreatePythonScriptStep():
        pipelineShapeId = str(uuid.uuid4())
        pipelineShapeAttributes = []
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 5))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 6))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 7))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 8))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 9))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 10))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 11))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 12))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 13))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 14))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 15))
        pipelineShapeAttributes.append(PipelineShapeAttributes("Temp", 16))
        name = "Source Data"
        internalName = name.lower().replace(" ", "_")
        pythonScriptStepShape = PipelineShapes(pipelineShapeId, 3, pipelineShapeAttributes, name, internalName, 
                                         1, 0, "assets/images/diagram/icon-none.svg", 0, 0, 0)
    

# pipeline = Makana.createPipeline('sample', 1, 2)
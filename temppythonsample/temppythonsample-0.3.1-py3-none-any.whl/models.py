class PipelineShapeAttribute:
    def __init__(self, attributeValue: str, shapeAttributeId: int):
            self.attributeValue = attributeValue
            self.shapeAttributeId = shapeAttributeId

class PipelineShape:
    def __init__(self, id : int, pipelineId: int, pipelineShapeAttribute: PipelineShapeAttribute, shapeDisplayName: str,
                 shapeInternalName: str, shapeId: int, sortOrder:int, statusImageUrl: int, stepOrder: int, x: int, y: int):
        self.id = id
        self.pipelineId = pipelineId
        self.pipelineShapeAttribute = pipelineShapeAttribute
        self.shapeDisplayName = shapeDisplayName
        self.shapeInternalName = shapeInternalName
        self.shapeId = shapeId
        self.sortOrder = sortOrder
        self.statusImageUrl = statusImageUrl
        self.stepOrder = stepOrder
        self.x = x
        self.y = y
        

class PipelineConnection:
    def __init__(self, pipelineId: int, From:  str, fromConnector: int, id: int, to: int, toConnector: str):
        self.pipelineId = pipelineId
        self.From = From
        self.fromConnector = fromConnector
        self.id = id
        self.to = to
        self.toConnector = toConnector

class Pipeline:
    def __init__(self, id : int = None, name: str = None, projectId: int = None, baseImageId: int = None, pipelineShape: PipelineShape = None,
                 pipelineShapeConnections: PipelineConnection = None):
        self.id = id
        self.name = name
        self.projectId = projectId
        self.baseImageId = baseImageId
        self.pipelineShapes = pipelineShape
        self.pipelineShapeConnections = pipelineShapeConnections
import os

from fastapi import APIRouter

state_router = APIRouter()


@state_router.get('/alive')
@state_router.post('/alive')
def alive():
    return {'detail': True}


path = os.path.join(os.path.dirname(__file__), 'static/viewController.js')
js = open(path).read()


def file():
    return js

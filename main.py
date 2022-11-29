from fastapi import FastAPI

app = FastAPI(title='CatOrBread')


@app.get('/')
async def main():
    return {'message': 'Welcome!'}

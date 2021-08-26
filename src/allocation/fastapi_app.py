from datetime import datetime
from fastapi import FastAPI, Request
from allocation import events, exceptions, messagebus, orm, unit_of_work

app = FastAPI()
orm.start_mappers()


@app.post("/add_batch")
def add_batch(request: Request):
    eta = request.json['eta']
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    event = events.BatchCreated(
        request.json['ref'], request.json['sku'], request.json['qty'], eta,
    )
    messagebus.handle([event], unit_of_work.SqlAlchemyUnitOfWork())
    return 'OK', 201


@app.post("/allocate")
def allocate_endpoint(request: Request):
    try:
        event = events.AllocationRequest(
            request.json['orderid'], request.json['sku'], request.json['qty'],
        )
        results = messagebus.handle([event], unit_of_work.SqlAlchemyUnitOfWork())
        batchref = results.pop()
    except exceptions.InvalidSku as e:
        return {'message': str(e)}, 400

    return {'batchref': batchref}, 201

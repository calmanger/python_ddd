from datetime import datetime
from fastapi import FastAPI, Request

from allocation.adapters import orm
from allocation.service_layer import services, unit_of_work

app = FastAPI()
orm.start_mappers()


@app.post("/add_batch")
def add_batch(request: Request):
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json["ref"],
        request.json["sku"],
        request.json["qty"],
        eta,
        unit_of_work.SqlAlchemyUnitOfWork(),
    )
    return "OK", 201


@app.post("/allocate")
def allocate_endpoint(request: Request):
    try:
        batchref = services.allocate(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
            unit_of_work.SqlAlchemyUnitOfWork(),
        )
    except services.InvalidSku as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201

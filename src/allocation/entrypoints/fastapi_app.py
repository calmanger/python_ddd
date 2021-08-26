from datetime import datetime
from fastapi import FastAPI, Request

from allocation.domain import commands
from allocation.adapters import orm
from allocation.service_layer import messagebus, unit_of_work
from allocation.service_layer.handlers import InvalidSku
from allocation import views

app = FastAPI()
orm.start_mappers()


@app.post("/add_batch")
def add_batch(request: Request):
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    cmd = commands.CreateBatch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta
    )
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    messagebus.handle(cmd, uow)
    return "OK", 201


@app.post("/allocate")
def allocate_endpoint(request: Request):
    try:
        cmd = commands.Allocate(
            request.json["orderid"], request.json["sku"], request.json["qty"]
        )
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        messagebus.handle(cmd, uow)
    except InvalidSku as e:
        return {"message": str(e)}, 400

    return "OK", 202


@app.get("/itemsallocations/{orderid}")
def allocations_view_endpoint(orderid: int):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = views.allocations(orderid, uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200

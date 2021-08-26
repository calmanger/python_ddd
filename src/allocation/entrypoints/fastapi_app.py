from datetime import datetime
from fastapi import FastAPI, Request
from allocation.domain import commands
from allocation.service_layer.handlers import InvalidSku
from allocation import bootstrap, views

app = FastAPI()
bus = bootstrap.bootstrap()


@app.post("/add_batch")
def add_batch(request: Request):
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    cmd = commands.CreateBatch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta
    )
    bus.handle(cmd)
    return "OK", 201


@app.post("/allocate")
def allocate_endpoint(request: Request):
    try:
        cmd = commands.Allocate(
            request.json["orderid"], request.json["sku"], request.json["qty"]
        )
        bus.handle(cmd)
    except InvalidSku as e:
        return {"message": str(e)}, 400

    return "OK", 202


@app.get("/itemsallocations/{orderid}")
def allocations_view_endpoint(orderid: int):
    result = views.allocations(orderid, bus.uow)
    if not result:
        return "not found", 404
    return result, 200

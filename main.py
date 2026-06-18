from routes.agent_routes import router_agents
from routes.mission_routes import router_missions
from routes.report_routes import router_reports
from database.db_connection import db
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from logs.logger_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    db.connection.close()

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def add_logs(request: Request, call_next):
     logger.info("%s %s", request.method, request.url)
     response = await call_next(request)

     return response

app.include_router(router=router_agents, prefix="/agents", tags=["Agents"])
app.include_router(router=router_missions, prefix="/missions", tags=["Missions"])
app.include_router(router=router_reports, prefix="/reports", tags=["Reports"])
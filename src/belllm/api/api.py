from fastapi import FastAPI

import belllm.plugins
from belllm.api.routers import chats_router
from belllm.config import get_config

app = FastAPI()
app.include_router(chats_router)

@app.get("/")
async def root():
    return "hi"


@app.get("/plugins")
def get_plugins():
    return belllm.plugins.list_plugins()


# todo disable / enable


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("belllm.api.api:app", reload=True, port=belllm.config.get("api.port"))

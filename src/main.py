from fastapi import FastAPI
import dish
import users
import canteen
import new
import carousel
from fastapi.middleware.cors import CORSMiddleware
import dish
import marks
import feedback
import uvicorn
import comments
import obj_storage
app = FastAPI()

# add CORS


origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")
app.include_router(dish.router, prefix="/dish", tags=["dish"])
app.include_router(canteen.router, prefix="/canteen", tags=["canteen"])
app.include_router(new.router, prefix="/new", tags=["new"])
app.include_router(carousel.router, prefix="/carousel", tags=["carousel"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(marks.router, prefix="/marks", tags=["marks"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(obj_storage.router, prefix="/static", tags=["storage"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

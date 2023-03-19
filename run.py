import uvicorn

if __name__ == "__main__":
    uvicorn.run(
       reload=True,
      #  host='192.168.1.112',
      #  port=90,
       app="app:app"
    )
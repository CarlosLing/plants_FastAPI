.PHONY: start_backend
start_backend: 
	uvicorn app.main:app --reload
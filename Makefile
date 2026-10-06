install:
	python -m pip install -r requirements.txt

run:
	python run.py

test:
	pytest -q

docker:
	docker compose up --build

clean:
	python -c "import shutil; [shutil.rmtree(p) for p in ['__pycache__','.pytest_cache'] if __import__('os').path.isdir(p)]"

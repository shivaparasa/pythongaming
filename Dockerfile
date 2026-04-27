FROM python
WORKDIR /shiva
COPY req.txt .
RUN pip install -r req.txt
COPY . .
CMD ["python","app.py"]


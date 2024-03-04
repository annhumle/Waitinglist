FROM python:3.9
ADD main.py . 
RUN pip install requests BeautifulSoup4 schedule
CMD ["python", "./main.py"]

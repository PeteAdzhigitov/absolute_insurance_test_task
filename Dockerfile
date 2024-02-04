FROM python:3.11

WORKDIR /absolute_insurance_test_task/

COPY reqirements.txt .

RUN pip install -r reqirements.txt

CMD python -m pytest -s --alluredir=/absolute_insurance_test_task/new_allure_results_folder
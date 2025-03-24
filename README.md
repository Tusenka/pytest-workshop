This is pytest workshop.
To run you need allure has been installed:

    pip install allure-pytes

To run tests:
1. Create venv:

        `python3 -m venv <venv>`
2. Install requirments:

     `pip3 install -r requirements.txt`
3. Run pytest:   

        `pytest --alluredir=%allure_result_folder% ./<folder>`
4. See report:

       ` allure serve %allure_result_folder%`


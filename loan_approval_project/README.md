**Программа аналізу кредитної історії**

```commandline
loan_approval_project/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   └── loan_data.csv
├── notebooks/
│   └── eda_and_modeling.ipynb
├── ml/
│   ├── __init__.py
│   ├── train.py                 # тренування моделі, gridsearch, збереження pipeline
│   ├── pipeline.py              # опис Pipeline: preprocessing + classifier
│   ├── utils.py                 # допоміжні функції для трансформацій
│   └── artifacts/
│       ├── model.joblib
│       └── feature_columns.json
├── django_app/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/                   # розділені settings: base, dev, prod
│   ├── webapp/                   # основний Django app
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── index.html        # основна програма згори
│   │   │   └── _code_block.html  # вставка для розкривного коду
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── models.py             # (не для ML — для збереження заявок/логів)
│   │   └── utils.py              # load_model(), predict(), make_plots()
│   └── tests/
│       ├── test_ml.py
│       └── test_views.py
├── infra/
│   └── github-actions.yml        # CI: lint + pytest + build image
└── presentation/
    ├── slides.pdf
    └── demo_script.md

```
## **Run the project**
### Activate virtual enviroment
Windows: 
```
venv\Scripts\activate
```
Mac/Linux:
```
source venv/bin/activate
```
### run the command in the terminal
```commandline
pip install -r requirements.txt

```
Run main file
```commandline
python main.py
```
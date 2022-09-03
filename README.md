# salary_parse

Project can analyze vacancies from popular russian recruiting sites like hh.ru and superjob.ru

### How to install
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
superjob.ru require API-token, you need set SJ_TOKEN in .env file:
```
SJ_TOKEN=
```
### How to use
Run script.py, for example:
```console
$ python3 script.py

+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Найдено вакансий | Обработано вакансий | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 29               | 20                  | 148175           |
| C                     | 15               | 9                   | 151666           |
| Java                  | 7                | 4                   | 217250           |
| C++                   | 15               | 6                   | 150000           |
| C#                    | 7                | 5                   | 216000           |
| JavaScript            | 38               | 24                  | 136208           |
| PHP                   | 19               | 15                  | 154161           |
| TypeScript            | 14               | 7                   | 172000           |
+-----------------------+------------------+---------------------+------------------+

```

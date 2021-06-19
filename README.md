# AutoCheckDocx
Автоматическая проверка текстовых документов на соответствие требованиям к составу и содержанию. Проект выполняется в рамках выпускной бакалаврской работы. 

# Взаимодействие с программой
```
> python main.py --help
usage: main.py [-h] folder pattern

positional arguments:
  folder      path to a folder with documents
  pattern     path to a pattern file

optional arguments:
  -h, --help  show this help message and exit
  
> python main.py ./docs ./patterns/pattern_1.json
```
Результат проверки сохраняется в папку с документами.

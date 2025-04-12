1) Activate virtual environment - Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
2) Get dot file - python manage.py graph_models api > models_diagram.dot
   convert dot file to SVG in this website - file:///C:/Users/isven/Downloads/graphviz.svg
3) To run testcase - python manage.py test
4) To generate api documentation to a yml file using drf spectacular package- python manage.py spectacular --color --file schema.yml
5) 
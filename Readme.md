# Sequência
1. [ZIP_Files_Extractor]
 - Busca os arquvos lá pasta financeiro Me, de modo a não ter que duplicar aumentando o consumo do armazenamento.
 - Limpa xmls de notas canceladas.
 - Extrai cada arquivo Xml de cada pasta Zip para a apasta >*data*.
 
2. [XML_to_Dataframe]
 - Lê cada xml e monta dataframe na pasta >*out*. Em 12-05-2022 levou mais de 60 minutos.
 - Salvo como "DataFrame-Generated-{{date}}.pkl"
 - Após esse processamento pode <ul>apagar todos os XML</ul> da pasta data, de modo a liberar armazenamento.
 ```python
from glob import glob
import os

arr = glob('data/*.xml')
[os.remove(f) for f in arr]
 ```

3. [Tratamento_df]
- Concat dataframe Linx
- Remoção de dados inválidos, duplicados, coverte ints e floats.
- Salvo na pasta >*out* como "Final_df.pkl"

4. [Streamlit Dashboard]
    - Dividi em 2 etapas, sendo:
    1. Arquivo *df_to_streamlit.py*  
    > Este arquivo contém as funções *df.loc* para criação dos conjuntos de dados e </br> a geração 
    > das *fig* do *Plotly*.
    2. Arquivo *streamlit.py*, 
    >Este arquivo chama as funções do arquivo anterior e cria o layout *Streamlit*. 

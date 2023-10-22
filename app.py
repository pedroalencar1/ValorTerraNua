"""
    App to estimate the value of empty land (exclude constructed improvements)
    
    Using data and models developed by:
        - Otacilio Junior
        - Pedro Medeiros
        - Alexandre Costa

    Pedro Alencar
    07.05.2023
"""

#%% import libraries

import pandas as pd
import numpy as np
import streamlit as st
import sidrapy # library to get updated ipca

import python.functions_vtn as vtn

st.set_page_config(layout="wide")

# get ipca value
# ipca_values = vtn.get_ipca()
# @st.cache
# def run_ipca():
#     # This function will only be run the first time it's called
#     vtn.get_ipca()

# ipca_val_test = run_ipca()

#%% app
coltitle, colempty1, colfig1 = st.columns([3,2,1])
with coltitle:
    st.title("Valor da Terra Nua")
    st.subheader("Assistente de precificação de propriedades rurais",
                 help = 'Insira nos campos abaixo as informações de: tamanho da propriedade em hectares; distância (km) para o centro urbano do município; se é irrigada ou não; qual o tipo de exploração atual na propriedade; qual a tipologia de uso (definições no quadro ao final da página); o valor do IPCA ou consulte-o')
    st.write("  ")
    st.write("  ")

# with colfig1:
#     st.image("figs/4_crop.png", use_column_width= True)   


# # create two columns of five text inputs
col1, col0, col2=  st.columns([5,1,10])

#input column
with col1:
    # st.subheader("Propriedades do solo")
    st.write('<p style="font-size:24px"><b>Dados da propriedade</b></p>',
                     unsafe_allow_html=True)
    area = st.number_input(label = "Área (hectares)", 
                              min_value=0.,
                              max_value= 100000., 
                              value = 10.,
                              key = "area",
                              step=0.1,format="%.1f")
    distance = st.number_input(label = "Distância até a cidade (km)", 
                              min_value=0.,
                              max_value= 1000., 
                              value = 10.,
                              key = "distance",
                              step=0.1,format="%.1f")
    
    irrigation = st.radio("Irrigabilidade:",
                          ('Não irrigavel', 'Irrigavel'))
    
    exploration = st.radio("Tipo de exploração:",
                          ('Sem exploração', 'Mista', "Agricultura"))
    
    class_of_use = st.radio("Classe de uso:",
                            ('Uso restrito',"Baixa Prod.", "Média Prod.", 
                             "Alta Prod.","Terras Arenosas", "Aluvião"),
                            help = "Dúvida sobre qual a classe de uso da propriedade? Confira no fim da página as características de cada categoria")
    
    calc_ipca = st.radio("Valor do IPCA:", 
                         ('Estimativa', 'Consulta'),
                         help = "Para mais informações consulte: https://www.ibge.gov.br/explica/inflacao.php. A opção 'Consulta' obtém dados diretos do IBGE e pode demorar alguns segundos para carregar.")
    
    if calc_ipca == 'Estimativa':
        val_ipca = st.number_input(label = "Valor do IPCA", 
                              min_value=0.,
                              max_value= 1000., 
                              value = 1.,
                              key = "val_ipca",
                              step=0.01,format="%.3f",
                              help = "Os dados para geração do resultado do valor da propriedade estão todos atualizados para outubro de 2020. Portanto, a necessidade de correção desse valor para a data em que a pesquisa está sendo realizada.")
    else:
        # val_ipca = vtn.get_ipca()
        @st.cache_data
        def run_ipca():
            # This function will only be run the first time it's called
            val = vtn.get_ipca()
            return(val)
        val_ipca = run_ipca()
        st.write(f"Valor do IPCA acumulado: {val_ipca:,.3f}")
        
    
# calculate price    
irr_id = vtn.IRRIGATION_ID[irrigation]
exp_id = vtn.EXPLORATION_ID[exploration]
use_id = vtn.CLASS_USE_ID[class_of_use]

est_price = vtn.price_empty_land(irr_id, exp_id, use_id, area, distance, val_ipca)
round_price = vtn.price_neat(est_price)
text_price = vtn.price_neat_text(round_price)

with col2:
    # st.subheader("Propriedades do sedimento")
    st.write('<p style="font-size:24px"><b>Valor da Terra Nua:</b></p>',
                     unsafe_allow_html=True)
    st.write(f"* Valor da Terra Nua, a partir de dados de pesquisa de mercado de 2020 e \
        atualizado por meio do IPCA ao corrente mês, para uma área de <b>{area:,.1f} hectares</b>, <b>{irrigation}</b>, \
            e distante <b>{distance:,.1f}  quilômetros </b> da cidade.",
             unsafe_allow_html=True)
    
    st.write(f"* Tipo de exploração: <b>{exploration}</b>",
             unsafe_allow_html=True)
    st.write(f"* Tipo de propriedade: <b>{class_of_use}</b>",
             unsafe_allow_html=True)
    st.write(" ")
    # st.write(f"<p style='font-size:20px'>&emsp;&emsp;&emsp;&emsp;Valor Médio: <b>R$ {round_price['Valor médio']:,.0f} </b></p>", unsafe_allow_html=True)
    # st.write(f"<p style='font-size:20px'>&emsp;&emsp;&emsp;&emsp;Valor Mínimo: <b>R$ {round_price['Valor mínimo']:,.0f} </b></p>", unsafe_allow_html=True)
    # st.write(f"<p style='font-size:20px'>&emsp;&emsp;&emsp;&emsp;Valor Máximo: <b>R$ {round_price['Valor máximo']:,.0f} </b></p>", unsafe_allow_html=True)

    st.write(f"<p style='font-size:20px'>&emsp;&emsp;&emsp;&emsp;Valor Médio: <b>R$ {text_price['Valor médio']} </b></p>", unsafe_allow_html=True)
    st.write(f"<p style='font-size:20px'>&emsp;&emsp;&emsp;&emsp;Valor Mínimo: <b>R$ {text_price['Valor mínimo']} </b></p>", unsafe_allow_html=True)
    st.write(f"<p style='font-size:20px'>&emsp;&emsp;&emsp;&emsp;Valor Máximo: <b>R$ {text_price['Valor máximo']} </b></p>", unsafe_allow_html=True)
    # st.write(" ")
    st.markdown("""---""")   
    
    st.write("Clique no botão abaixo para baixar os resultados da análise")
   
    
    df_export = vtn.export_dataframe(irr_id,
                                 exp_id,
                                 use_id,
                                 area,
                                 distance, 
                                 val_ipca,                      
                                 round_price)

    csv = vtn.convert_df(df_export)    
    
    st.download_button("Baixar", 
                       data = csv, 
                       file_name="Valor_terra_nua.csv")    
    st.write(" ")
    st.write(" ")
    # st.markdown("""---""")   
    # st.write("""<p style='color:#808080;'><i><u>Dica: Salve esta página como um relatório em pdf</u><br>
    #         &nbsp;&nbsp;&nbsp;&nbsp; 1) Clique com o botão direito do mouse em qualquer ponto da tela e escolha 'imprimir'.<br>
    #         &nbsp;&nbsp;&nbsp;&nbsp; 2) Escolha _layout_ paisagem para uma melhor visualização. <br>
    #         &nbsp;&nbsp;&nbsp;&nbsp; 3) Pressione salvar. <br>
    #         &nbsp;&nbsp;&nbsp;&nbsp; 4) Pronto. O arquivo será salvo automaticamente na sua pasta de downloads.
    #         </i></p>
    #         """,
    #         unsafe_allow_html=True)
    
#%% additional information
st.markdown("""---""")  
st.subheader("Sobre as tipologias de uso do solo")
st.write("Na tabela abaixo apresentamos as características e solos predominantes de cada tipologia")
col20, col21, col22 = st.columns([1,6,1])
with col21: 
    st.image("figs/Tipologias.png", use_column_width = True)

st.markdown("""---""")
st.subheader("Sobre o app")

st.write("Aplicativo desenvolvido decorrente de trabalho de tese de doutorado de Otacílio de Assis Jr. pelo Programa de Pós-graduação em Engenharia Agrícola da Universidade Federal do Ceará, no âmbito do projeto Cientista Chefe em parceria com o Governo do Estado do Ceará, e tem como objetivo auxiliar os diferentes agentes de mercado (Corretores, Compradores, Vendedores, Prefeituras, Estado do Ceará) a estimar valores de terra nua em propriedades rurais no Estado do Ceará – Brasil.")
st.write("**Equipe:**")
st.write("[MSc. Otacilio de Assis junior](http://lattes.cnpq.br/1270752252633393) (pesquisador)")
st.write("[Dr. Pedro Alencar](https://www.tu.berlin/oekohydro/team/pedro-alencar/) (desenvolvedor)")
st.write("[Prof. Dr. Pedro H. A. Medeiros](http://lattes.cnpq.br/4970091740105771) (coordenador)")
st.write("[Prof. Dr. Carlos A. G. Costa](http://lattes.cnpq.br/9346087418658759) (coordenador)")
st.write("[Profa. Dra. Patrícia V. P. S. Lima](http://lattes.cnpq.br/7172491133426747) (coordenadora)")

col71, col72, col73 = st.columns([1,2,1])
with col72:  
    st.image("figs/logos.png", use_column_width = True)


#%% notes on getting the IPCA

# Check page: https://analisemacro.com.br/economia/indicadores/analise-de-dados-de-inflacao-no-python/
#             https://www.idinheiro.com.br/tabelas/tabela-ipca/

# raw_ipca = sidrapy.get_table(table_code = '1737',
#                              territorial_level = '1',
#                              ibge_territorial_code = 'all',
#                              variable = '63,69,2263,2264,2265',
#                              period = 'last%20472')

# ipca = data[data['D3N'] == 'IPCA - Variação mensal']
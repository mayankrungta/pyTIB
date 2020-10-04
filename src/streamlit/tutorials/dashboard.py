'''
Sample Dashboard to diplays the various examples together
'''

import streamlit as st

import os
import random
import time

import networkx as nx
from pyvis.network import Network

import streamlit.components.v1 as components

def ticketing():
    st.text('Ticket to show here')

def networkx():
    G = nx.Graph()
    G2 = Network(notebook=True, height='800px', width='800px')
    G2.from_nx(G)

    path_to_imgs = './nx_images'
    html_file = './nx.html'

    prev = ''
    imgs = os.listdir(path_to_imgs)
    for index, img in enumerate(imgs):
        next_index = random.randint(0, index)
        print(next_index)
        img_path = os.path.join(path_to_imgs, img)
        #print(img_path)
        G2.add_node(img, shape='image', image =img_path)
        if prev != '':
            G2.add_edge(img, prev)
            prev = img
        if not index:
            continue
        if next_index == index:
            continue
        next = imgs[next_index]
        G2.add_edge(img, next)

    with st.spinner('Loading...'):
        time.sleep(3)
    st.success('Loaded!')

    html_file = '/home/mayank/repo/pyTIB/src/streamlit/tutorials/g.html'
    G2.show(html_file)
    with open(html_file, 'r') as html_handle:
        html_content =  html_handle.read()
        print(html_content)

    #url = './nx_images/aadhaar_c_nt.svg'
    url = 'https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/410.svg'
    url = './nx_images/410.svg'
    components.html(f'<img src="{url}" />', height=800, width=800)
    #st.write(html_content, unsafe_allow_html=True)
    #components.iframe('file:///tmp/z.html')

    if False:
        K5 = nx.complete_graph(5)
        dot = nx.nx_pydot.to_pydot(K5)
        st.graphviz_chart(dot.to_string())

sb = st.sidebar
sb.header('Demos')
sb.subheader('Demos')
sb_link = sb.radio('Choose your Demo', ('NetworkX With Images', 'Ticketing'))
if sb_link == 'Ticketing':
    ticketing()
else:
    networkx()






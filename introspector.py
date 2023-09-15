import streamlit as st
import urllib.parse        
import requests

def resolver(url):
    data2 =  requests.get(url)
    value =   data2.text
    return value

def get_input():
    total = ""
    q= st.experimental_get_query_params()
    new_messages = []
    if "text" in q:
        return q["text"]
    if "messages" in q:
        for item in q["messages"]:
            new1 = urllib.parse.unquote(item)

            if new1.startswith("http"):
                #st.write("DEBUG1",new1)
                new2 = resolver(new1)
                #st.write("DEBUG2",new2)
            else:
                st.write("OTHER",new1)
                new2 = new1
                pass
            total = total + new2
    #st.session_state['text-input'] = total
    #st.write("DEBUG",total)
    return total

import serpapi
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def compare(mach_name):
    params = {
        "engine": "google_shopping",
        "q": mach_name,
        "gl":"in",
        "api_key": "24bc3fd0b6a2ce82179644884a276f3e2972193a3046e26cf90c285a456a473a"
    }
    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return shopping_results

c1,c2 = st.columns(2)
c1.image("e_pharmacy.png" , width=300)
c2.header("Epharma Price comparison system")


st.sidebar.title("Enter the name of medicine:")
med_name = st.sidebar.text_input("Enter name here 👇:")
number = st.sidebar.text_input("Enter number of options here 👇:")
medicine_company = []
medicine_price = []

if med_name is not None:
    if st.sidebar.button("Price Compare:"):
        shopping_results = compare(med_name)
        lowest_price = float((shopping_results[0].get('price'))[1:])
        st.sidebar.image(shopping_results[0].get('thumbnail'))
        print(lowest_price)
        lowest_price_index = 0


        for i in range(int(number)):
            current_price = float(shopping_results[i].get('price')[1:])
            medicine_company.append(shopping_results[i].get('source'))
            medicine_price.append(float(shopping_results[i].get('price')[1:]))
        ##--------------------------------------------------------------
            st.title(f"option{i+1}")


            c1,c2 = st.columns(2)
            c1.write("Company:")
            c2.write(shopping_results[i].get('source'))

            c1.write("Title:")
            c2.write(shopping_results[i].get('title'))

            c1.write("Price:")
            c2.write(shopping_results[i].get('price'))

            url = shopping_results[i].get('product_link')
            c1.write("Buy Link:")
            c2.write("[Link](%s)"%url)
            """--------------------------------------------"""
            if (current_price < lowest_price):
                lowest_price = current_price
                lowest_price_index = i

        ## this is best option

        st.title("Best Option:")

        c1, c2 = st.columns(2)
        c1.write("Company:")
        c2.write(shopping_results[lowest_price_index].get('source'))

        c1.write("Title:")
        c2.write(shopping_results[lowest_price_index].get('title'))

        c1.write("Price:")
        c2.write(shopping_results[lowest_price_index].get('price'))

        url = shopping_results[lowest_price_index].get('product_link')
        c1.write("Buy Link:")
        c2.write("[Link](%s)" % url)

        #---------------------------------------
        ## graph comparison
        df = pd.DataFrame(medicine_price,medicine_company)
        st.title("Chart Comparison:")
        st.bar_chart(df)

        fig,ax = plt.subplots()
        ax.pie(medicine_price,labels=medicine_company,shadow=True)
        ax.axis("equal")
        st.pyplot(fig)
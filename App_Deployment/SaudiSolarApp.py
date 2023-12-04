import numpy as np
import streamlit as st
import tensorflow
from keras.preprocessing import image
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
global picture
from streamlit_folium import st_folium
import leafmap.kepler as leafmap
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from geopy.distance import geodesic
import folium
from folium.plugins import Draw


def home_function():
    pass

def dirt_detection():
    loaded_model = tensorflow.keras.models.load_model('MobileNet_model.h5')
    #picture = st.camera_input("Take a picture")

    #if picture:
    #    st.image(picture)

    # File uploader widget
    picture = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Display the uploaded image
    if picture is not None:
        # Read the image
        picture = Image.open(picture)

        # Display the image
        st.image(picture, caption="Uploaded Image", use_column_width=True)


    def pic(pictures):
        test_image2 = np.array(pictures.resize((224, 224))) # test_image2 = image.load_img(pictures, target_size=(224, 224))
        test_image2 = image.img_to_array(test_image2)
        test_image2 = test_image2/255
        test_image2 = np.expand_dims(test_image2, axis = 0)
        preds = loaded_model.predict(test_image2)
        preds = np.argmax(preds, axis=1)
        return preds


    def predic(pictures):
        preds = pic(pictures)
        diction = {'Clean': 0, 'Electrical Damage': 1, 'Physical Damage': 2, 'Snow Covered': 3, 'Weather Damage': 4}

        for key, value in diction.items():
            if preds[0] == value:
                return key

        return False


    if st.button('Predict'):
        st.write(predic(picture))
    else:
        st.write('')


def power_prediction():
    model = joblib.load(r'ridge.sav')

    # Input features
    dc = st.text_input("DC Power:")
    a_temp = st.selectbox("Ambient Temperature:", range(20, 41))
    m_temp = st.text_input("Module Temperature:")
    irr = st.text_input("Irradiation:")
    

    # Prediction button
    if st.button("Predict"):
        # Check if all input fields are filled
        if dc and a_temp and m_temp and irr:
            # Make a prediction
            input_data = {
                'DC Power': float(dc),
                'Ambient Temperature': int(a_temp),
                'Module Temperature': float(m_temp),
                'Irradiation': float(irr),
                
            }

            # Create a DataFrame for prediction
            input_df = pd.DataFrame([input_data])

            # Rename the columns to match the names used during training
            input_df.columns = ['DC_POWER',  'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION']

            # Make prediction
            prediction = model.predict(input_df)[0]

            # Display the prediction with two decimal places
            st.success(f"Predicted Solar Output: {prediction:.2f} KW")
        else:
            st.warning("Please fill in all the input fields.")



def solar_locations():
    st.subheader("You can scan the barcode to see possible locations!!")
    st.image('barcode_loc.jpg')



 
    


#background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #e5e5f7 10px ), repeating-linear-gradient( #444cf755, #444cf7 );
#background-color: #e5e5f7;

###############################################--MainPage--####################################################

page_bg_img= """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://cdn.pixabay.com/photo/2023/09/10/11/16/solar-8244680_1280.jpg");
background-size: cover;
opacity: 0.8;
}

</style>


"""
#<div class="appview-container st-emotion-cache-1wrcr25 ea3mdgi6" data-testid="stAppViewContainer" data-layout="narrow"><div data-testid="collapsedControl" class="st-emotion-cache-aw8l5d eczjsme1"><button kind="headerNoPadding" data-testid="baseButton-headerNoPadding" class="st-emotion-cache-6q9sum ef3psqc4"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-fblp2m ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6-6-6z"></path></svg></button></div><section class="st-emotion-cache-68vbgh eczjsme11" data-testid="stSidebar" aria-expanded="false" style="position: relative; user-select: auto; width: 336px; height: 717px; box-sizing: border-box; flex-shrink: 0;"><div data-testid="stSidebarContent" class="st-emotion-cache-6qob1r eczjsme3"><div class="st-emotion-cache-1b9x38r eczjsme2"><button kind="header" data-testid="baseButton-header" class="st-emotion-cache-ch5dnh ef3psqc5"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp51 st-emotion-cache-fblp2m ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"></path></svg></button></div><div data-testid="stSidebarUserContent" class="st-emotion-cache-16txtl3 eczjsme4"><div class="block-container st-emotion-cache-1v7bkj4 ea3mdgi4" data-testid="block-container"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="0" data-testid="stVerticalBlock" class="st-emotion-cache-g70r9e e1f1d6gn1"><div data-stale="false" width="0" class="element-container st-emotion-cache-1kd0zmy e1f1d6gn3" data-testid="element-container"><iframe allow="accelerometer; ambient-light-sensor; autoplay; battery; camera; clipboard-write; document-domain; encrypted-media; fullscreen; geolocation; gyroscope; layout-animations; legacy-image-formats; magnetometer; microphone; midi; oversized-images; payment; picture-in-picture; publickey-credentials-get; sync-xhr; usb; vr ; wake-lock; xr-spatial-tracking" src="http://localhost:8501/component/streamlit_option_menu.option_menu/index.html?streamlitUrl=http%3A%2F%2Flocalhost%3A8501%2F" width="0" height="468" scrolling="no" sandbox="allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads" title="streamlit_option_menu.option_menu"></iframe></div></div></div></div></div></div><div><div class="" style="position: absolute; user-select: none; width: 8px; height: 100%; top: 0px; cursor: col-resize; right: -6px;"><div class="st-emotion-cache-1i2wz1k eczjsme0"></div></div></div></section><section tabindex="0" class="main st-emotion-cache-uf99v8 ea3mdgi5"><div class="block-container st-emotion-cache-1y4p8pa ea3mdgi4" data-testid="block-container"><div class="st-emotion-cache-1wmy9hl e1f1d6gn0"><div width="704.0017700195312" data-testid="stVerticalBlock" class="st-emotion-cache-1yfd1go e1f1d6gn1"><div data-stale="false" width="704.0017700195312" class="element-container st-emotion-cache-1aj9tr7 e1f1d6gn3" data-testid="element-container"><div class="stHeadingContainer"><div class="stMarkdown" style="width: 704.002px;"><div data-testid="stMarkdownContainer" class="st-emotion-cache-nahz7x e1nzilvr5" style="width: 704.002px;"><div class="st-emotion-cache-k7vsyb e1nzilvr2"><h1 id="you-have-selected-home"><div data-testid="StyledLinkIconContainer" class="st-emotion-cache-zt5igj e1nzilvr4"><a href="#you-have-selected-home" class="st-emotion-cache-15zrgzn e1nzilvr3"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a><span class="st-emotion-cache-10trblm e1nzilvr1">You have selected Home</span></div></h1></div></div></div></div></div><div data-stale="false" width="704.0017700195312" class="element-container st-emotion-cache-1aj9tr7 e1f1d6gn3" data-testid="element-container"><div class="stHeadingContainer"><div class="stMarkdown" style="width: 704.002px;"><div data-testid="stMarkdownContainer" class="st-emotion-cache-nahz7x e1nzilvr5" style="width: 704.002px;"><div class="st-emotion-cache-k7vsyb e1nzilvr2"><h1 id="only-here-in-home-page-home"><div data-testid="StyledLinkIconContainer" class="st-emotion-cache-zt5igj e1nzilvr4"><a href="#only-here-in-home-page-home" class="st-emotion-cache-15zrgzn e1nzilvr3"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a><span class="st-emotion-cache-10trblm e1nzilvr1">only here in home page Home</span></div></h1></div></div></div></div></div></div></div></div><div data-testid="IframeResizerAnchor" data-iframe-height="true" class="st-emotion-cache-1wrevtn ea3mdgi0"></div><div data-testid="AppViewBlockSpacer" class="st-emotion-cache-qcqlej ea3mdgi3"></div><footer class="st-emotion-cache-cio0dv ea3mdgi1">Made with <a href="//streamlit.io" target="_blank" class="st-emotion-cache-z3au9t ea3mdgi2">Streamlit</a></footer></section></div>

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>Shining A Light On Tomorrow!</h1>", unsafe_allow_html=True)



with st.sidebar:
    selected = option_menu(
        menu_title="Solar Panels", #required #bi-grid-3x2
        options=["Home", "Dirt Detection", "Power Prediction", "Best Locations"],
        icons = ["house" , "camera" , "bar-chart-line" , "pin-map"],
        default_index=0,
        #orientation="horizontal",
        )
if selected == "Home" :
    #st.title("**Shining A Light On Tomorrow!**")
    st.title("")
    st.header("Solar Panels",divider="gray")
    st.subheader('''
    Solar energy is a sustainable and renewable source has recently gained significant attention. Solar panels, also known as photovoltaic panels, harvest solar energy from the sun to provide the energy we use every day. Using renewable energy is commonly viewed as contingent upon developing sustainable energy sources, decreasing reliance on fossil fuels, and mitigating climate change. It is essential for halting global warming and cutting greenhouse gas emissions. Additionally, it might minimize the amount of water needed to produce energy and enhance air quality. ''')
    
    image = Image.open(r"C:\Users\dinaa\OneDrive\الصور\solar_home_page.png")
    st.image(image, caption='How Solar Panels Work')


    st.subheader('''Using photovoltaic cells, solar panels generate electricity by converting solar energy. Electrons move when sunlight strikes a solar panel's surface, generating an electrical current. The semiconductor materials used in the photovoltaic cells in the solar panel, such as silicon, can capture solar energy and transform it into electrical power. After being generated by the solar panels, the power is conveyed to an inverter that transforms the Direct Current (DC) electricity produced by the solar panels into Alternating Current (AC) electricity, which can be used to power buildings. '''
    )


if selected == "Dirt Detection" :
    st.title("")
    st.header(selected,divider="gray")
    dirt_detection()
    
if selected == "Power Prediction" :
    st.title("")
    st.header(selected,divider="gray")
    power_prediction()

if selected == "Best Locations":
    st.title ("")
    st.header(selected,divider="gray")
    solar_locations()











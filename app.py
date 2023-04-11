# Condition that removes all the rectangles and parallelograms except the first parallelogram

import streamlit as st
import zipfile
import io
import json

st.title('Automate your PBIX file')

# Upload the source zip file
ss = st.file_uploader('Upload a PBIX file')

# --------- Removing Streamlit's Hamburger and Footer starts ---------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            a {text-decoration: none;}
            .css-15tx938 {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --------- Removing Streamlit's Hamburger and Footer ends ------------
new_vc1 = {
    "id": 99999999,
    "x": 0,
    "y": 0,
    "z": 15000,
    "width": 1440.3516483516485,
    "height": 65,
    "config": "{\"name\":\"be03e83f8af4ed66720d\",\"layouts\":[{\"id\":0,\"position\":{\"x\":0,\"y\":0,\"z\":15000,\"width\":1440.3516483516485,\"height\":65,\"tabOrder\":15000}}],\"singleVisual\":{\"visualType\":\"shape\",\"drillFilterOtherVisuals\":true,\"objects\":{\"shape\":[{\"properties\":{\"tileShape\":{\"expr\":{\"Literal\":{\"Value\":\"'rectangle'\"}}},\"tabRoundCornerTop\":{\"expr\":{\"Literal\":{\"Value\":\"20L\"}}}}}],\"rotation\":[{\"properties\":{\"shapeAngle\":{\"expr\":{\"Literal\":{\"Value\":\"0L\"}}}}}],\"fill\":[{\"properties\":{\"fillColor\":{\"solid\":{\"color\":{\"expr\":{\"Literal\":{\"Value\":\"'#00519C'\"}}}}}},\"selector\":{\"id\":\"default\"}}]},\"vcObjects\":{\"title\":[{\"properties\":{\"text\":{\"expr\":{\"Literal\":{\"Value\":\"'Report title background'\"}}}}}]}}}",
    "filters": "[]",
    "tabOrder": 15000
}
new_vc2 = {
                    "id": 2539326977,
                    "x": 345.1685393258427,
                    "y": 11.985018726591761,
                    "z": 38000,
                    "width": 299.62546816479403,
                    "height": 64.71910112359551,
                    "config": "{\"name\":\"1ee7ff6475ab1fbc89b7\",\"layouts\":[{\"id\":0,\"position\":{\"x\":345.1685393258427,\"y\":11.985018726591761,\"z\":38000,\"width\":299.62546816479403,\"height\":64.71910112359551,\"tabOrder\":38000}}],\"singleVisual\":{\"visualType\":\"textbox\",\"drillFilterOtherVisuals\":true,\"objects\":{\"general\":[{\"properties\":{\"paragraphs\":[{\"textRuns\":[{\"value\":\"Dummy\",\"textStyle\":{\"fontWeight\":\"bold\",\"fontSize\":\"20pt\",\"color\":\"#ffffff\"}}]}]}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}}}",
                    "filters": "[]",
                    "tabOrder": 38000
                }


if ss:
    # In-memory byte stream to hold the destination zip file data
    zip_data = io.BytesIO()

    # Extract the files from the source zip file and re-zip them into a destination zip file
    with zipfile.ZipFile(ss, 'r') as source_zip:
        with zipfile.ZipFile(zip_data, 'w') as destination_zip:
            # Iterate over the files in the source zip file
            for name in source_zip.namelist():

                # Skip the Security Binding file
                if name == 'SecurityBindings':
                    continue

                # Manipulate the Layout file
                if name == 'Report/Layout':
                    # Read the contents of the layout file
                    data = source_zip.read(name).decode('utf-16 le')
                    # Old layout file
                    with open('app-og.json', 'w') as f:
                        a=json.loads(data)
                        json.dump(a, f)
                    try:
                        data=json.loads(data)
                        ##### Changing attributes of certain elements
                        for section in data['sections']:
                            # print(section,'section')
                            section['visualContainers'].append(new_vc1)
                            section['visualContainers'].append(new_vc2)
                                
                        # New Layout file
                        with open('app-generated.json', 'w') as f:
                            json.dump(data, f)
                    
                    except:
                        print('hi')
                    # Add the manipulated layout data to the destination zip file
                    data = json.dumps(data)
                    destination_zip.writestr(name, data.encode('utf-16 le'))
                
                else:
                    # Add the file to the destination zip file as-is
                    binary_data = source_zip.read(name)
                    destination_zip.writestr(name, binary_data)


    # Download the destination file
    st.download_button(
        label='Download Destination PBIX File',
        data=zip_data.getvalue(),
        file_name='destination.pbix',
        mime='application/pbix'
    )
else:
    
    st.warning('Please upload a pbix file')

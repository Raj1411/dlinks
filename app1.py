from pydrive.auth import GoogleAuth
import streamlit as st
from pydrive.drive import GoogleDrive
import keyboard
import base64
import pandas as pd
import io
import time


st.title('Extract Google Drive Links')

file_id=st.text_input('')
filelist=list(file_id.split(','))
print(filelist)
if file_id=='':
    'Please Enter File id '
else:
    # au=r"D:\Projects\Extract drive links with PyDrive\client_secrets.json"
    gauth=GoogleAuth()
    # gauth.LocalWebserverAuth()
    drive=GoogleDrive(gauth)
    # keyboard.press_and_release('ctrl+w')
    per={
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    }

    allfiles=[]
    with st.spinner('Please wait, We are extracting links for you...'):
        for flist in filelist:
            filelist1=drive.ListFile({'q': "'{}' in parents and trashed=false".format(flist)}).GetList()
            for file1 in filelist1:
                f=drive.CreateFile(file1)
                x=f.InsertPermission(per)
                allfiles.append(file1['id'])
    
    df=pd.DataFrame(allfiles,columns=['fileid'])
    towrite = io.BytesIO()
    df['file link']='https://drive.google.com/file/d/'+df['fileid']
    st.write('Extraction is Completed')
    downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="GoogleDriveLinks.xlsx">Download file</a>'
    st.markdown(linko, unsafe_allow_html=True)

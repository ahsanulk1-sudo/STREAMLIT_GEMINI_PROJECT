import  streamlit as st
import re
from api_calling import note_generator,audio_transcription,quiz_generator


from PIL import Image

st.title('Note Summary and Quiz Generator')

st.markdown('Upload upto 3 images to generate Note summary and quizes')

st.divider()


#SIDEBAR

with st.sidebar:
    st.header('Controls')
    images = st.file_uploader(
        'Upload the photos of your note',
        type = ['jpg','jpeg','png'],
        accept_multiple_files=True
    
    )
    
    pill_images =[]
    for img in images:
            pill_img = Image.open(img)
            
            
            pill_images.append(pill_img)
    
    #IMAGE
    
    if(images):
        if len(images)>3:
            st.error('Upload at max 3 images')
        else:
            st.subheader('Uploaded Images')
            col = st.columns(len(images))
            
             
            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)  
                    
                    
#DIFFICULTY

    selected_option = st.selectbox(
    
    'Enter the difficulty of your quiz',
    ('Easy','Medium','Hard'),
    index = None
)   
   
    pressed = st.button('Click the button to initiate AI',type = 'primary')



if pressed:
    if not images:
        st.error('You must upload one image')
        
    if not selected_option:
        st.error('You must select a difficulty')
        
        
    if images and selected_option:
        
        try:
        
            #CONTAINER FOR NOTEE
            
            with st.container(border =True):
                st.subheader('Your note')
                
                with st.spinner('AI is writting note for you'):
                    
                    
                    
                    generated_notes = note_generator(pill_images)
                    st.markdown(generated_notes)
                    
                 
                
                
            #CONTAINER FOR AUDIO
            
            with st.container(border =True):
                st.subheader('Audio Transcription')
                
                with st.spinner('AI is generating audio for you'):
                    
                    generated_notes = generated_notes.replace("#","")
                    generated_notes = generated_notes.replace("*","")
                    generated_notes = generated_notes.replace("-","")
                    generated_notes = generated_notes.replace("_","")
                    
                    
                    audio_transcript = audio_transcription(generated_notes)
                    st.audio(audio_transcript)
                
            #CONTAINER FOR QUIZ
            
            with st.container(border =2):
                st.subheader(f"Quiz{selected_option} Difficulty")
                
                
                with st.spinner("AI is generating quizzes for you"):
                    quizzes = quiz_generator(pill_images,selected_option)
                
                    st.markdown(quizzes)

        except Exception as e:
            if "429" in str(e):
                found = re.search(r"retryDelay': '(\d+)s", str(e))
                if found:
                    total_seconds = int(found.group(1))
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    st.warning(f'Daily limit reached. Please try again after {hours} hours {minutes} minutes.')
                else:
                    st.warning('Daily limit reached. Please try again later.')
            else:
                st.warning('Something went wrong. Please try again later.')

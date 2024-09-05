
import gradio as gr
import stylecloud
from PIL import Image
import os


import importlib.metadata

try:
    version = importlib.metadata.version('stylecloud')
    print(f'stylecloud version: {version}')
except importlib.metadata.PackageNotFoundError:
    print('stylecloud package is not installed')


import PIL
print(PIL.__version__)


# İkon etiketlerini ve değerlerini eşlemek için bir sözlük oluşturun
icon_map = {
    "Car": "fas fa-car",
    "Crescent and Star": "fas fa-star-and-crescent",
    "Trophy": "fas fa-trophy",
    "Heart": "fas fa-heart",
    "Cloud": "fas fa-cloud",
    "Gift": "fas fa-gift"
}

def create_stylecloud(file, text_input, language, icon_label):
    # Dosya veya text inputtan gelen metni kullan
    if file:
        text = file.decode('utf-8')
    elif text_input:
        text = text_input
    else:
        return None  # Eğer ikisi de yoksa None döner

    # İkon etiketini ikon değerine dönüştür
    icon = icon_map[icon_label]
    
    output_file = 'stylecloud.png'
    stylecloud.gen_stylecloud(
        text=text,
        icon_name=icon,
        size=500,
        output_name=output_file
    )
    
    image = Image.open(output_file)
    image = image.resize((300, 300))
    return image

with gr.Blocks() as demo:
    gr.Markdown('Word Cloud Generater')
    
    with gr.Row():
        input_choice = gr.Radio(choices=['Upload Your File', 'Enter Your Text'], label='Select Text Upload Format', value='Upload Your File')
    
    with gr.Row(visible=True) as file_input_row:
        file_input = gr.File(label='Upload Text File', type='binary')
        
    with gr.Row(visible=False) as text_input_row:
        text_input = gr.Textbox(label='Enter Your Text')

    with gr.Row():
        language = gr.Radio(choices=['TR', 'EN'], label='Language', value='TR')
    
    with gr.Row():
        icon = gr.Dropdown(choices=list(icon_map.keys()), label='Icon Selection', value='Crescent and Star')
    
    with gr.Row():
        create_button = gr.Button('Generate')
        output_image = gr.Image(label='Word Cloud')

        # butona basıldığında
        create_button.click(
            create_stylecloud,
            inputs=[file_input, text_input, language, icon],
            outputs=output_image
        )

    def update_input_visibility(choice):
        if choice == 'Upload Your File':
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)
    
    input_choice.change(
        update_input_visibility,
        inputs=[input_choice],
        outputs=[file_input_row, text_input_row]
    )
    
demo.launch(share=True)


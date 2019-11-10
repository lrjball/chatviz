from .main import visualize_chat
import matplotlib.pyplot as plt
import pandas as pd
from .load_data import prep_sms_data, prep_whatsapp_data, prep_facebook_data
import io


def visualize(upload_widget, file_type):
    file_object = list(upload_widget.value.values())[0]
    file_name = file_object['metadata']['name']
    byte_stream = io.BytesIO(file_object['content'])
    if file_type == 'Facebook':
        df = prep_facebook_data(byte_stream)
    elif file_type == 'WhatsApp':
        df = prep_whatsapp_data(byte_stream)
    elif file_type == 'SMS':
        df = prep_sms_data(byte_stream)
    elif file_type == 'CSV':
        df = pd.read_csv(byte_stream)
    else:
        raise ValueError(f'Invalid option {file_type}')
    visualize_chat(df, 'Example Plot')
    plt.show()

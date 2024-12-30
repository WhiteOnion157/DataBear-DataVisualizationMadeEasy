from matplotlib import pyplot as plt
import pandas as pd
import io
from discord import File

async def create_graph(message):
    # message contains len(message.attachments) attachments
    fig, axs = plt.subplots(len(message.attachments), 1, figsize=(10, 5*len(message.attachments)))
    if len(message.attachments) == 1:
        axs = [axs]
    for i, attachment in enumerate(message.attachments):
        file_content = await attachment.read()
        current_csv = pd.read_csv(io.BytesIO(file_content), header=None)
        current_csv = current_csv.sort_values(by=current_csv.columns[0])
        x = current_csv.iloc[:, 0]
        y = current_csv.iloc[:, 1]
        axs[i].plot(x, y, marker='x')
        axs[i].set_title(attachment.filename)
        axs[i].grid(True)

    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close(fig)
    return await message.channel.send(file=File(buffer, filename='plot.png'))
        

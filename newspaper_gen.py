import random

# Define the page dimensions
PAGE_WIDTH = 1500
PAGE_HEIGHT = 2000

# Define the range for chunk sizes
MIN_CHUNK_SIZE = 400
MAX_CHUNK_SIZE = 800

MIN_COLUMN_WIDTH = 200
MAX_COLUMN_WIDTH = 220

MIN_ROWS = 3

def generate_chunks():
    chunks = []
    remaining_height = PAGE_HEIGHT

    while remaining_height > 0 or len(chunks) < MIN_ROWS:
        row_chunks = []

        if remaining_height >= 2 * MIN_CHUNK_SIZE:
            row_height = random.randint(MIN_CHUNK_SIZE, min(MAX_CHUNK_SIZE, remaining_height - MIN_CHUNK_SIZE))
        else:
            row_height = remaining_height

        remaining_height -= row_height
        remaining_width = PAGE_WIDTH

        while remaining_width > 0:
            if remaining_width >= 2 * MIN_CHUNK_SIZE:
                chunk_width = random.randint(MIN_CHUNK_SIZE, min(MAX_CHUNK_SIZE, remaining_width - MIN_CHUNK_SIZE))
            else:
                chunk_width = remaining_width

            chunk_height = row_height
            row_chunks.append((chunk_width, chunk_height))
            remaining_width -= chunk_width

        chunks.append(row_chunks)

    # Randomly combine adjacent chunks horizontally
    for i in range(len(chunks)):
        j = 0
        while j < len(chunks[i]) - 1:
            if random.random() < 0.3:  # 30% probability of merging horizontally
                chunk_width = chunks[i][j][0] + chunks[i][j+1][0]
                chunk_height = chunks[i][j][1]
                chunks[i][j] = (chunk_width, chunk_height)
                del chunks[i][j+1]
            else:
                j += 1

    # Randomly combine adjacent chunks vertically
    i = 0
    while i < len(chunks) - 1:
        if random.random() < 0.2:  # 20% probability of merging vertically
            if len(chunks[i]) == len(chunks[i+1]):
                for j in range(len(chunks[i])):
                    chunk_width = chunks[i][j][0]
                    chunk_height = chunks[i][j][1] + chunks[i+1][j][1]
                    chunks[i][j] = (chunk_width, chunk_height)
                del chunks[i+1]
            else:
                i += 1
        else:
            i += 1

    return chunks

def split_chunks_into_columns(chunks):
    new_chunks = []

    for row_chunks in chunks:
        new_row_chunks = []

        for chunk_width, chunk_height in row_chunks:
            remaining_width = chunk_width
            columns = []

            while remaining_width > MAX_COLUMN_WIDTH:
                column_width = random.randint(MIN_COLUMN_WIDTH, MAX_COLUMN_WIDTH)
                columns.append((column_width, chunk_height))
                remaining_width -= column_width

            # Distribute the remaining width evenly among the columns
            num_columns = len(columns)
            if num_columns > 0:
                extra_width = remaining_width // num_columns
                remaining_width = remaining_width % num_columns

                for i in range(num_columns):
                    column_width, column_height = columns[i]
                    column_width += extra_width
                    if i < remaining_width:
                        column_width += 1
                    columns[i] = (column_width, column_height)
            else:
                columns.append((remaining_width, chunk_height))

            # Add a horizontal split for the heading text
            heading_height = random.randint(50, 80)
            content_height = chunk_height - heading_height

            new_chunk = {
                'heading': (chunk_width, heading_height),
                'content': {
                    'columns': columns,
                    'height': content_height
                }
            }
            new_row_chunks.append(new_chunk)

        new_chunks.append(new_row_chunks)

    return new_chunks


def generate_chunk_html(chunk):
    content_columns = chunk['content']['columns']
    content_height = chunk['content']['height']
    content_width = sum(column[0] for column in content_columns)

    html = f'<div class="chunk" style="width: {content_width}px;">\n'
    html += f'  <div class="heading" style="width: {content_width}px; height: 50px;"></div>\n'
    html += f'  <div class="content" style="height: {content_height}px;">\n'

    for column_width, _ in content_columns:
        html += f'    <div class="column" style="width: {column_width}px;"></div>\n'

    html += '  </div>\n'
    html += '</div>\n'

    return html

def generate_page():
    chunks = generate_chunks()
    sorted_chunks = sorted(chunks, key=lambda row: sum(chunk[0] * chunk[1] for chunk in row), reverse=True)
    column_chunks = split_chunks_into_columns(sorted_chunks)

    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Newspaper</title>
    <link rel="stylesheet" href="newspaper.css">
</head>
<body>
    <div class="newspaper">
        <div class="frame">
'''

    for row_chunks in column_chunks:
        html += f'<div class="row" width= {PAGE_WIDTH}>\n'
        for chunk in row_chunks:
            html += generate_chunk_html(chunk)
        html += '</div>\n'

    html += '''
        </div>
    </div>
</body>
</html>
'''
    return html

# Generate the HTML file
with open('newspaper.html', 'w') as file:
    file.write(generate_page())
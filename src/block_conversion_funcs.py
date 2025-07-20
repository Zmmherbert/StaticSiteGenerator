

def markdown_to_blocks(markdown):
    return list(filter(lambda item: item != "", list(map(lambda item: item.strip(), markdown.split("\n\n")))))
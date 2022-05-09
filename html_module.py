def generate_file(file_name):
    try:
        file = open('output/'+file_name+".html", 'x')
        content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>OpenX Task 1</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="big-box">
            <div class="header">
                <div class="arrow_col"></div>
                <div class="h_col">Seller's name</div>
                <div class="h_col">Seller's domain</div>
                <div class="h_col">Seller's type</div>
                <div class="h_col">Undersellers</div>
                <div class="h_col">Link</div>
                <div class="h_col">Depth</div>
            </div>
        """
        file.write(content)
        return True
    except:
        return False

def generate_row(name, domain, sellers_type, undersellers, link, file_name):
    content = '<div class="seller"><div class="seller-data"><div class="arrow">></div><div class="r_col">{}</div><div class="r_col">{}</div><div class="r_col">{}</div><div class="r_col">{}</div>{}'.format(name, domain, sellers_type, undersellers, link)
    file = open('output/'+file_name+".html", 'a')
    file.write(content)
    return 0

def generate_full_row(name, domain, sellers_type, undersellers, link, file_name):
    content = '<div class="seller"><div class="seller-data"><div class="arrow">></div><div class="r_col">{}</div><div class="r_col">{}</div><div class="r_col">{}</div><div class="r_col">{}</div>{}<div class="r_col"></div></div></div>'.format(name, domain, sellers_type, undersellers, link)
    file = open('output/'+file_name+".html", 'a', encoding='utf-8')
    file.write(content)
    return 0

def generate_undersellers_for_link(depth, file_name):
    content = '<div class="r_col">{}</div>'.format(depth)
    file = open('output/'+file_name+".html", 'a', encoding='utf-8')
    file.write(content)
    return 0

def end_row(file_name):
    content = "</div></div>"
    file = open('output/'+file_name+".html", 'a')
    file.write(content)
    return 0

def end_file(file_name):
    file = open('output/'+file_name+".html", 'a')
    content = """
</div>
</body>
</html>
    """
    file.write(content)
    return 0
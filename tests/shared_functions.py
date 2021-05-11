import tempfile


def generate_temp_file_with_content(content):
    tmp = tempfile.NamedTemporaryFile(suffix=".py")
    tmp.write(str.encode(content))
    tmp.seek(0)
    yield tmp.name
    tmp.close()

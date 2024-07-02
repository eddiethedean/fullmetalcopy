import io


def write_csv(csv_file: io.BytesIO) -> None:
    csv_file.writelines([
        b'id,x,y\n',
        b'1,a,33\n',
        b'2,b,66\n'
    ])
    csv_file.seek(0)
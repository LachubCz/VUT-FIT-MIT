import numpy

def format_matrix(header, matrix,
                  top_format, left_format, cell_format, row_delim, col_delim):
    table = [[''] + header] + [[name] + row for name, row in zip(header, matrix)]
    table_format = [['{:^{}}'] + len(header) * [top_format]] \
                 + len(matrix) * [[left_format] + len(header) * [cell_format]]
    col_widths = [max(
                      len(format.format(cell, 0))
                      for format, cell in zip(col_format, col))
                  for col_format, col in zip(zip(*table_format), zip(*table))]

    return row_delim.join(
               col_delim.join(
                   format.format(cell, width)
                   for format, cell, width in zip(row_format, row, col_widths))
               for row_format, row in zip(table_format, table))
def render():
    string = format_matrix(['','0','', '','1','', '','2','','', '3',''],
                        [[42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42], [0, 42.001, 0, 0, 42.002, 0, 0, 42.002, 0, 0, 42.002, 0], [42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42], 
                        [42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42],  [0, 42.002, 0, 0, 42.003, 0, 0, 42.002, 0, 0, 42.003, 0], [42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42], 
                        [42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42], [0, 42.002, 0, 0, 42.002, 0, 0, 42.002, 0, 0, 42.003, 0], [42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42], 
                        [42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42], [0, 42.003, 0, 0, 42.002, 0, 0, 42.002, 0, 0, 42.004, 0], [42, 0, 42, 42, 0, 42, 42, 0, 42, 42, 0, 42]],
                        '{:^{}}', '{:<{}}', '{:>{}.3f}', '\n', ' | ')
    string = string.replace('42.001', '   S  ')
    string = string.replace('42.002', '   F  ')
    string = string.replace('42.003', '   H  ')
    string = string.replace('42.004', '   G  ')
    print(string.replace('42.000', '      '))

from IPython.nbformat import read, write


def main(file_name, input_version=4, output_version=3):
    with open(file_name) as f:
        notebook = read(f, input_version)
    cells = notebook['cells']
    executable_cells = filter(lambda cell: 'execution_count' in cell and cell['execution_count'] is not None, cells)
    sorted_cells = sorted(executable_cells, key=lambda cell: cell['execution_count'])
    def setitem(dictionary, attr, value):
        dictionary[attr] = value
        return dictionary
    correctly_indexed = [setitem(cell, 'execution_count', i+1) for i, cell in enumerate(sorted_cells)]
    notebook['cells'] = correctly_indexed
    with open(file_name, 'w') as f:
        write(notebook, f, output_version)


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

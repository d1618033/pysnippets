from IPython import nbformat
import functools


def main(file_name):
    notebook = nbformat.read(file_name, nbformat.NO_CONVERT)
    cells = notebook['cells']
    executable_cells = filter(lambda cell: 'execution_count' in cell and cell['execution_count'] is not None, cells)
    sorted_cells = sorted(executable_cells, key=lambda cell: cell['execution_count'])
    def setitem(dictionary, attr, value):
        dictionary[attr] = value
        return dictionary
    correctly_indexed = [setitem(cell, 'execution_count', i+1) for i, cell in enumerate(sorted_cells)]
    notebook['cells'] = correctly_indexed
    nbformat.write(notebook, file_name)


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

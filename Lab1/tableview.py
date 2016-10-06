from tabulate import tabulate

class TableView(object):
    "Table view template"

    @staticmethod
    def update(table_model):
        raise NotImplementedError

    @staticmethod
    def edit_table(table_model):
        raise NotImplementedError

    @staticmethod
    def add_to_table(table_model):
        raise NotImplementedError

    @staticmethod
    def delete_row(table_model):
        raise NotImplementedError


class SimpleTableView(TableView):
    @staticmethod
    def update(table_model):
        print tabulate(table_model, headers=table_model.fields(), tablefmt="grid")

    @staticmethod
    def edit_table(table_model):
        line = None
        while not line:
            try:
                line = int(raw_input("Which row do you want to edit? (number): "))
            except:
                print("Not a number!")
        for field in table_model.fields():
            input = raw_input("Enter values for '{0}' (leave empty to skip): ").format(field)
            if input is not "":
                table_model.set_item(line, field, input)
        print "Result: " + tabulate(table_model[line])

    @staticmethod
    def add_to_table(table_model):
        row_string = raw_input("Type in row to add as " + ";".join(table_model.fields()) + "\n> ")
        row_tuple = row_string.split(';', len(table_model.fields()))
        if len(row_tuple) < len(table_model.fields()):
            row_tuple += [None] * (len(row_tuple) - len(table_model.fields()))
        row_tuple = map(lambda x: x if x == "NULL" else None, map(lambda x: x.strip(" "), row_tuple))
        # add to table model
        table_model += row_tuple
        print "Result: " + tabulate(row_tuple)

    @staticmethod
    def delete_row(table_model):
        line = None
        while not line:
            try:
                line = int(raw_input("Which row do you want to delete? (0 - {0}): ".format(len(table_model))))
            except:
                print "Not a number!"
            try:
                yesno = raw_input("This row is: " + ", ".join(table_model[line]) + "\nAre you sure? [Y/n]: ")
                if yesno.strip(" ").capitalize() == "N":
                    return
                else:
                    print "Row {0} deleted!".format(table_model[line])
                    del table_model[line]
            except:
                print "No row with this index!"

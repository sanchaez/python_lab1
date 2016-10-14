from tabulate import tabulate
from console_interface import Menu

class TableView(object):
    "Table view template"

    @staticmethod
    def update(table_controller):
        raise NotImplementedError

    @staticmethod
    def edit_table(table_controller):
        raise NotImplementedError

    @staticmethod
    def add_to_table(table_controller):
        raise NotImplementedError

    @staticmethod
    def delete_row(table_controller):
        raise NotImplementedError


class SimpleTableView(TableView):
    @staticmethod
    def update(table_controller):
        print tabulate(table_controller, headers=table_controller.fields(), tablefmt="grid", missingval="NULL")

    @staticmethod
    def edit_table(table_controller):
        line = None
        while not line:
            try:
                line = int(raw_input("Which row do you want to edit? (number): "))
            except:
                print("Not a number!")
        for field in table_controller.fields():
            input = raw_input("Enter values for '{0}' (leave empty to skip): ").format(field)
            if input is not "":
                table_controller.set_item(line, field, input)
        print "Result: " + tabulate(table_controller[line])

    @staticmethod
    def add_to_table(table_controller):
        row_string = raw_input("Type in row to add as " + ";".join(table_controller.fields()) + "\n> ")
        row_tuple = row_string.split(';', len(table_controller.fields()))
        if len(row_tuple) < len(table_controller.fields()):
            row_tuple += [None] * (len(row_tuple) - len(table_controller.fields()))
        row_tuple = map(lambda x: x if x == "NULL" else None, map(lambda x: x.strip(" "), row_tuple))
        # add to table model
        table_controller += row_tuple
        print "Result: " + tabulate(row_tuple)
        return row_tuple

    @staticmethod
    def delete_row(table_controller):
        line = None
        while not line:
            try:
                line = int(raw_input("Which row do you want to delete? (0 - {0}): ".format(len(table_controller))))
            except:
                print "Not a number!"
            try:
                yesno = raw_input("This row is: " + ", ".join(table_controller[line]) + "\nAre you sure? [Y/n]: ")
                if yesno.strip(" ").capitalize() == "N":
                    return
                else:
                    line_to_delete = table_controller[line]
                    print "Row {0} deleted!".format(line_to_delete)
                    del table_controller[line]
                    return line_to_delete
            except:
                print "No row with this index!"

    @staticmethod
    def search(table_controller):
        # select columns to search
        selected_columns = []
        confirm = False
        # each menu entry appends value to a list
        selector = Menu([x for x in table_controller.fields()]
                        + ["Revert last action", "Confirm"],
                        [lambda: selected_columns.append(x)
                         for x in table_controller.fields()
                         if x not in selected_columns]
                        + [selected_columns.pop, lambda: selector.bool_true_exit(confirm)],
                        name="Select columns to search")
        selector.loop()
        # returned from menu
        if not confirm:
            return
        del selector
        print("Selected columns: {0}").format(selected_columns)
        search_value = raw_input("Input value to search: ")
        # search in table and print results
        found_row = table_controller.find(search_value, selected_columns)
        if found_row:
            print "Row found: \n{0}".format(tabulate(found_row, table_controller.fields()))



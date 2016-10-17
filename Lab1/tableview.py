from tabulate import tabulate


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
        print tabulate(table_controller, headers='keys', tablefmt="grid", missingval="NULL")
        raw_input("Press Enter to continue...")

    @staticmethod
    def edit_table(table_controller):
        line = None
        SimpleTableView.update(table_controller)
        while line is None:
            try:
                line = int(raw_input("Which row do you want to edit? (0 - {0}): ").format(len(table_controller)))
            except:
                print("Not a number!")
                line = None
        print tabulate(table_controller[line].items())
        for field in table_controller.fields():
            input = raw_input("Enter values for {0} (leave empty to skip): ".format(field))
            if input:
                table_controller.set_item(line, field, input)
        print "Result: \n" + tabulate(table_controller[line].items())
        raw_input("Press Enter to continue...")

    @staticmethod
    def add_to_table(table_controller):
        row_string = raw_input("Type in row to add as " + ";".join(table_controller.fields()) + "\n> ")
        row_array = []
        if row_string:
            row_array = row_string.split(';', len(table_controller.fields()))
            if (len(row_array) <= len(table_controller.fields())):
                row_array += [None] * (len(table_controller.fields()) - len(row_array))
            row_array = map(lambda x: None if x == "NULL" else x, row_array)
        else:
            row_array += [None] * len(table_controller.fields())

        # add to table model
        table_controller += row_array
        print "Result: " + str(row_array)  # tabulate(row_array)
        raw_input("Press Enter to continue...")
        return row_array

    @staticmethod
    def delete_row(table_controller):
        line = None
        SimpleTableView.update(table_controller)
        while line is None:
            try:
                line = int(raw_input("Which row do you want to delete? (0 - {0}): ".format(len(table_controller))))
            except:
                print "Not a number!"
            print tabulate(table_controller[line].items())
            yesno = raw_input("Are you sure? [Y/n]: ")
            if yesno.strip(" ").capitalize() == "N":
                return
            else:
                line_to_delete = table_controller[line]
                print "Row {0} deleted!".format(line_to_delete)
                del table_controller[line]
                return line_to_delete
        raw_input("Press Enter to continue...")

    @staticmethod
    def search(table_controller):
        # select columns to search
        _input = raw_input("Enter columns to search (value;value){0}: ".format(table_controller.fields()))
        selected_columns = _input.split(";", len(table_controller.fields()))
        search_value = raw_input("Input value to search: ")
        # search in table and print results
        found_row = table_controller.find(search_value, selected_columns)
        if found_row:
            print "Row found: \n"
            print tabulate(found_row.items())
        else:
            print "Nothing found!"
        raw_input("Press Enter to continue...")

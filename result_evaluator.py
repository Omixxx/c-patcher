from modules.custom_types.TsvFileInput import TsvFileInput
import modules.utils as utils
import sys
from tabulate import tabulate
from decimal import Decimal, getcontext  # ottenere i dati dal tsv

# filtrare i metodi che hanno affrontato la test suite
# ordinare i metodi in base alla differenza tra la predizione e il valore originale
# stampare i metodi ordinati analisi statistica sui risultati: quanti metodi hanno ricevuto un incremento della leggibilità?
# quanti metodi hanno ricevuto un decremento della leggibilità?
# qual è la media dell'incremento della leggibilità (su tutti i progetti)?
# qual è il massimo incremento della leggibilità(tra tutti i progetti)?
# qual è il massimo decremento della leggibilità(tra tutti i progetti)?
# qual è la percentuale di metodi che hanno ricevuto un incremento della leggibilità riportano un malfunzionamento nel comportamento?
# qual è la percentuale di metodi che hanno ricevuto un decremento della leggibilità riportano un malfunzionamento nel comportamento?
# cosa è successo hai metodi che hanno ricevuto un incremento della leggibilità e hanno superato la test suite? (mostrare i metodi)
# cosa è successo hai metodi che hanno ricevuto un decremento della leggibilità e hanno superato la test suite? (mostrare i metodi)


# format="latex" to print in latex format
def __print_results(data, format="grid"):
    print(
        tabulate(
            data,
            # headers=[
            #     "System",
            #     "Label",
            #     "N. of methods",
            #     "Average Readability Score Differences",
            #     "N. of Test Passed",
            # ],
            tablefmt=format,
        )
    )


def __populate_table(system_name: str, rows: list[TsvFileInput]) -> list[list]:
    rows = [x for x in rows if x.manual_readability_score != ""]
    n_of_methods = len(rows)
    print(n_of_methods)
    avarage_readability_score_difference = sum(
        [
            Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore)
            for x in rows
        ]
    ) / Decimal(n_of_methods)
    number_of_test_passed = len([x for x in rows if x.does_test_suite_pass == "True"])
    percentage_number_of_test_passed = (number_of_test_passed / n_of_methods) * 100
    manual_readability_score = sum(
        [Decimal(x.manual_readability_score) for x in rows]
    ) / Decimal(n_of_methods)
    return [
        [
            system_name,
            rows[0].label,
            n_of_methods,
            avarage_readability_score_difference,
            (
                "%"
                + percentage_number_of_test_passed.__str__()
                + " ("
                + number_of_test_passed.__str__()
                + "/"
                + n_of_methods.__str__()
                + ")"
            ),
            manual_readability_score,
        ]
    ]


tsv = sys.argv[1]
rows: list[TsvFileInput] = utils.extract_rows(tsv)
system_name = sys.argv[1].split(".")[0]
tested_rows = [x for x in rows if x.does_test_suite_pass != ""]

low_rows = [x for x in tested_rows if x.label == "LOW"]
medium_rows = [x for x in tested_rows if x.label == "MID"]
high_rows = [x for x in tested_rows if x.label == "HIGH"]

print("Total number of methods: ", len(rows))
print("Number of methods that have faced the test suite: ", len(tested_rows))

__print_results(__populate_table(system_name, low_rows), "latex")
__print_results(__populate_table(system_name, medium_rows), "latex")
__print_results(__populate_table(system_name, high_rows), "latex")


# only_print_results = sys.argv[2] if len(sys.argv) > 2 else False
#
# filtered_rows = [
#     x for x in filtered_rows if (x.does_test_suite_pass != "" and x.does_contain_errors == "False") ]
# test_suite_passed_rows = [
#     x for x in filtered_rows if (x.does_test_suite_pass == "True")
# ]
# test_suite_failed_rows = [
#     x for x in filtered_rows if (x.does_test_suite_pass == "False")
# ]
# filtered_rows.sort(
#     key=lambda x: (float(x.predictions_readability_score) - float(x.readabilityScore)),
#     reverse=True,
# )
#
# if only_print_results == "-r":
#     data = __populate_table(filtered_rows)
#     __print_results(data, "latex")
#     exit()
#
# getcontext().prec = 6
# increment_readability_and_pass_tests = [x for x in test_suite_passed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) > 0)]
# print("Number of methods that have received an increment in readability and passed the test suite: ", increment_readability_and_pass_tests.__len__())
#
# increment_readability_and_fail_tests  = [x for x in test_suite_failed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) > 0)]
# print("Number of methods that have received an increment in readability and failed the test suite: ", increment_readability_and_fail_tests.__len__())
#
# decrement_readability_and_pass_tests = [x for x in test_suite_passed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) < 0)]
# print("Number of methods that have received a decrement in readability and passed the test suite: ", decrement_readability_and_pass_tests.__len__())
#
# decrement_readability_and_fail_tests = [x for x in test_suite_failed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) < 0)]
# print("Number of methods that have received a decrement in readability and failed the test suite: ", decrement_readability_and_fail_tests.__len__())
#
# positive_readability_increment = increment_readability_and_pass_tests + increment_readability_and_fail_tests
# print("Average readability increment: ", sum([Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) for x in positive_readability_increment]) / Decimal(len(positive_readability_increment)))
#
# negative_readability_increment = decrement_readability_and_pass_tests + decrement_readability_and_fail_tests
# print("Avarage readability decrement: ", sum([Decimal(x.readabilityScore) - Decimal(x.predictions_readability_score) for x in negative_readability_increment]) / Decimal(len(negative_readability_increment)))
#
# print("Avarage readability increment form methods that have passed the test suite: ", sum([Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) for x in increment_readability_and_pass_tests])/Decimal(len(increment_readability_and_pass_tests)))
#
# print("Avarage readability increment form methods that have failed the test suite: ", sum([Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) for x in increment_readability_and_fail_tests])/Decimal(len(increment_readability_and_fail_tests)))
#
# print("Avarage readability decrement form methods that have passed the test suite: ",0 if decrement_readability_and_pass_tests.__len__() == 0 else max([(Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore)).normalize() for x in decrement_readability_and_pass_tests]))
#
# print("Avarage readability decrement form methods that have failed the test suite: ", max([(Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore)).normalize() for x in decrement_readability_and_fail_tests]))

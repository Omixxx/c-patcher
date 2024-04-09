from modules.custom_types.TsvFileInput import TsvFileInput
import modules.utils as utils
import sys
from tabulate import tabulate
from decimal import Decimal, getcontext # ottenere i dati dal tsv
# filtrare i metodi che hanno affrontato la test suite
# ordinare i metodi in base alla differenza tra la predizione e il valore originale
# stampare i metodi ordinati
# analisi statistica sui risultati:

# quanti metodi hanno ricevuto un incremento della leggibilità?
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
            headers=[
                "Method",
                "Label",
                "Original readability",
                "Predicted readability",
                "Difference",
                "Does test suite pass",
            ],
            tablefmt=format,
        )
    )


def __populate_table(filtered_rows: list[TsvFileInput]) -> list[list]:
    data = []
    for row in filtered_rows:
        row_data = [
            row.name, row.label, row.readabilityScore.__str__(),
            row.predictions_readability_score.__str__(),
            Decimal(row.predictions_readability_score) - Decimal(row.readabilityScore),
            row.does_test_suite_pass.__str__(),
        ]
        data.append(row_data)
    return data


tsv = sys.argv[1]
only_print_results = sys.argv[2] if len(sys.argv) > 2 else False

filtered_rows: list[TsvFileInput] = utils.extract_rows(tsv)
filtered_rows = [
    x for x in filtered_rows if (x.does_test_suite_pass != "" and x.does_contain_errors == "False") ]
test_suite_passed_rows = [
    x for x in filtered_rows if (x.does_test_suite_pass == "True")
]
test_suite_failed_rows = [
    x for x in filtered_rows if (x.does_test_suite_pass == "False")
]
filtered_rows.sort(
    key=lambda x: (float(x.predictions_readability_score) - float(x.readabilityScore)),
    reverse=True,
)

if only_print_results == "-r":
    data = __populate_table(filtered_rows)
    __print_results(data, "latex")
    exit()

getcontext().prec = 6
increment_readability_and_pass_tests = [x for x in test_suite_passed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) > 0)]
print("Number of methods that have received an increment in readability and passed the test suite: ", increment_readability_and_pass_tests.__len__())

increment_readability_and_fail_tests  = [x for x in test_suite_failed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) > 0)]
print("Number of methods that have received an increment in readability and failed the test suite: ", increment_readability_and_fail_tests.__len__())

decrement_readability_and_pass_tests = [x for x in test_suite_passed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) < 0)]
print("Number of methods that have received a decrement in readability and passed the test suite: ", decrement_readability_and_pass_tests.__len__())

decrement_readability_and_fail_tests = [x for x in test_suite_failed_rows if (Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) < 0)]
print("Number of methods that have received a decrement in readability and failed the test suite: ", decrement_readability_and_fail_tests.__len__())

positive_readability_increment = increment_readability_and_pass_tests + increment_readability_and_fail_tests 
print("Average readability increment: ", sum([Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) for x in positive_readability_increment]) / Decimal(len(positive_readability_increment)))

negative_readability_increment = decrement_readability_and_pass_tests + decrement_readability_and_fail_tests 
print("Avarage readability decrement: ", sum([Decimal(x.readabilityScore) - Decimal(x.predictions_readability_score) for x in negative_readability_increment]) / Decimal(len(negative_readability_increment)))

print("Avarage readability increment form methods that have passed the test suite: ", sum([Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) for x in increment_readability_and_pass_tests])/Decimal(len(increment_readability_and_pass_tests)))

print("Avarage readability increment form methods that have failed the test suite: ", sum([Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore) for x in increment_readability_and_fail_tests])/Decimal(len(increment_readability_and_fail_tests)))

print("Avarage readability decrement form methods that have passed the test suite: ",0 if decrement_readability_and_pass_tests.__len__() == 0 else max([(Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore)).normalize() for x in decrement_readability_and_pass_tests]))

print("Avarage readability decrement form methods that have failed the test suite: ", max([(Decimal(x.predictions_readability_score) - Decimal(x.readabilityScore)).normalize() for x in decrement_readability_and_fail_tests]))

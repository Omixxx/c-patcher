from modules.custom_types.TsvFileInput import TsvFileInput
import modules.utils as utils
import sys
from tabulate import tabulate


tsv = sys.argv[1]
rows: list[TsvFileInput] = utils.extract_rows(tsv)
number_of_initial_methods = 100
number_of_faulty_methods = 0
difference_in_readability_from_original = []
number_of_methods_that_passed_the_test_suite = 0
number_of_method_that_not_contain_errors = 0



faulty_rows = [x for x in rows if x.does_contain_errors == "True"]
non_faulty_rows = [x for x in rows if x.does_contain_errors == "False"]

non_faulty_rows.sort(
    key=lambda x: (float(x.predictions_readability_score) - float(x.readabilityScore)),
    reverse=True,
)

data = []
for row in non_faulty_rows:
    number_of_method_that_not_contain_errors = number_of_method_that_not_contain_errors + 1
    row_data = [
        row.name,
        row.label,
        row.readabilityScore.__str__(),
        row.predictions_readability_score.__str__(),
        float(row.predictions_readability_score) - float(row.readabilityScore),
        row.does_test_suite_pass.__str__(),
    ]
    data.append(row_data)

    if row.does_contain_errors == "":
        break

    difference = float(row.predictions_readability_score) - float(row.readabilityScore)
    difference_in_readability_from_original.append(difference)

    if row.does_test_suite_pass == "True":
        number_of_methods_that_passed_the_test_suite = number_of_methods_that_passed_the_test_suite +  1

# print(
#     tabulate(
#         data,
#         headers=[
#             "Name",
#             "Label",
#             "Original Readability Score",
#             "Prediction Readability Score",
#             "Increment/Decrement" "Does test suite pass?",
#         ],
#         tablefmt="latex",
#     )
# )


# la contare quanti metodi (lable) dei metodi che risultati fallati 
print("Number of LOW methods that are faulty: ", [x for x in faulty_rows if x.label == "LOW"].__len__())
print("Number of LOW methods that are not faulty: ", [x for x in non_faulty_rows if x.label == "LOW"].__len__())
print("Number of MID methods that are faulty: ", [x for x in faulty_rows if x.label == "MID"].__len__())
print("Number of MID methods that are not faulty:", [x for x in non_faulty_rows if x.label =="MID"].__len__() )
print("Number of HIGH methods that are faulty: ", [x for x in non_faulty_rows if x.label == "HIGH"].__len__())
print("Number of HIGH methods that are not faulty: ", [x for x in non_faulty_rows if x.label == "HIGH"].__len__())


print("Number of initial methods: ", number_of_initial_methods)
print("Number of methods that do not contain errors: ", non_faulty_rows.__len__())
print("Number of methods that passed the test suite: ", number_of_methods_that_passed_the_test_suite)
print("Average difference in readability from original: ", sum(difference_in_readability_from_original) / len(difference_in_readability_from_original) if len(difference_in_readability_from_original) > 0 else 0)
print("Max difference in readability from original: ", max(difference_in_readability_from_original))
print("Min difference in readability from original: ", min(difference_in_readability_from_original))
print("Number of methods that are more readable than the original: ", len([x for x in difference_in_readability_from_original if x > 0]))
print("Number of methods that are less readable than the original: ", len([x for x in difference_in_readability_from_original if x < 0]))
print("Number of methods that have the same readability as the original: ", len([x for x in difference_in_readability_from_original if x == 0]))
print("Average readability score of the original methods: ", sum([float(x.readabilityScore) if x.does_contain_errors == "False" else 0.0 for x in non_faulty_rows]) / len(non_faulty_rows))
print("Average readability score of the predicted methods: ", sum([float(x.predictions_readability_score) if x.does_contain_errors == "False" else 0.0 for x in non_faulty_rows]) / len(non_faulty_rows))

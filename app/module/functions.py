# The following function returns the tuition cost for a given state and time period
# This data will provide the in-state and out of state tuition metric for the given State University


def find_tution_cost(state, timing, university_data):
    college_dict = {}
    for i in range(len(university_data)):
        if university_data[i]['STATE_NAME'] == state:
            if timing == 1:
                college_dict.update({"State": state, "University": university_data[i]['University'],
                                     "InState": university_data[i]['2020-21'], "OutState": university_data[i]['Out_2020_2021']})

            elif timing == 2:
                college_dict.update({"State": state, "University": university_data[i]['University'],
                                     "InState": university_data[i]['2021-22'], "OutState": university_data[i]['Out_2021_2022']})

            else:
                college_dict.update({"State": state, "University": university_data[i]['University'],
                                     "InState": university_data[i]['2021-22'], "OutState": university_data[i]['Out_2021_2022']})

    return college_dict


# The following function will return data and labels to be used for our charts using the Chart js library.
# It take one parameter of subject - which helps to map which mongo collection and data structure we are working
# with to provide the data
def prepare_chart_data(subject, university_data):
    labels = []
    in_state_labels = []
    out_state_labels = []
    data_values = []
    in_state_values = []
    out_state_values = []

    chart_data = {}
    count_for_in_state = 0

    if subject == 'university':
        for key in university_data[0].keys():

            if not (key == '_id' or key == 'University' or key == 'STATE'):
                labels.append(key)

        labels.pop(len(labels) - 1)

        # get a count for half of the list (i.e. in-state)
        count_for_in_state = len(labels) / 2

        # break the list into two separate lists (i.e. one for in_state and one for out of state)
        for i in range(int(count_for_in_state)):
            in_state_labels.append(labels[i])

        for i in range(int(count_for_in_state)-1, (int(count_for_in_state) * 2)-1, 1):
            out_state_labels.append(labels[i])

        for value in university_data[0].values():

            if not (type(value) == str):
                data_values.append(value)

        data_values.pop(0)

        # break the list into two separate lists (i.e. one for in_state and one for out of state)
        for i in range(int(count_for_in_state)):
            in_state_values.append(data_values[i])

        for i in range(int(count_for_in_state)-1, (int(count_for_in_state) * 2)-1, 1):
            out_state_values.append(data_values[i])

        chart_data.update({'in_state_labels': in_state_labels, 'in_state_values': in_state_values,
                           'out_state_labels': out_state_labels, 'out_state_values': out_state_values})

    return chart_data

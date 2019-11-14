import pickle
import numpy as np
import csv
import matplotlib.pyplot as plt

countries_insta = {
	"australia": "0",
	"brazil": "1",
	"canada": "2",
	"china": "3",
	"ethiopia": "4",
	"nigeria": "4",
	"germany": "5",
	"india": "6",
	"indonesia": "7",
	"iran": "8",
	"russia": "9"
	}

countries_utk = {
	"white": "0",
	"black": "1",
	"asian": "2",
	"indian": "3",
	"others": "4"
	}

def parse_record_fields(dataset, result):
    path = result['path']                       # /folder/folder/folder/
    name = result['name']                       # 12_1_@justinbieber
    exact_age = name.split('_')[0]              # 21 years
    # insta_labels: [age]_[country]_[username]
    # utk_labels: [age]_[gender]_[race]_[date&time].jpg
    if dataset == 'instagram':
        country_index = name.split('_')[1]
        country_name = list(countries_insta.keys())[list(countries_insta.values()).index(country_index)]
    if dataset == 'utk':
        country_index = name.split('_')[2]
        country_name = list(countries_utk.keys())[list(countries_utk.values()).index(country_index)]
    label_str = result['label-str']             # actual age10-19
    pred_label_str = result['pred-label-str']   # perceived age20-29
    label_num = result['label-num']             # 1
    pred_label_num = result['pred-label-num']   # 2
    probs = result['probs']                     # [%, %, ..., %]

    return path, name, exact_age, country_index, country_name, label_str, pred_label_str, label_num, pred_label_num, probs

#
# This function will draw a line in the line graph with the following attributes:
# 1. x axis represents the age
# 2. y axis represents the accuracy
# 3. each line represents one kind of the neural network, say one of the mlp, vgg, resnet
#
def plot_accuracy(net, dataset, bin, country = 'all'):
    # Load output
    path = './result_data/%s/pickle_%s_test_part_%s_bin_%s' %(dataset, net, dataset, bin)
    with open(path,'rb') as f:
        output = pickle.load(f)

    acc_age_correct = {}
    acc_age_total = {}
    acc_age_mean = {}
    acc_exact_age = {}

    for result in output:
        # Get Info
        path, name, exact_age, country_index, country_name, label_str, pred_label_str, label_num, pred_label_num, probs = parse_record_fields(dataset, result)

        # Calc Statistics
        if label_num not in acc_age_correct.keys():
            acc_age_correct[label_num] = 0
            acc_age_total[label_num] = 0
            acc_age_mean[label_num] = 0

        # add + 1 for correct classification
        if label_num == pred_label_num:
            acc_age_correct[label_num] = acc_age_correct[label_num] + 1
        # add + 1 to count total age to divide correct count into mean
        acc_age_total[label_num] = acc_age_total[label_num] + 1

    # calc mean for each class
    for label_num in acc_age_correct.keys():
        new_num = label_num * bin
        acc_exact_age[new_num] = 0

        acc_exact_age[new_num] = acc_age_correct[label_num] / acc_age_total[label_num]
        acc_age_mean[label_num] = acc_age_correct[label_num] / acc_age_total[label_num]

    #print(acc_age_mean)

    vals = acc_exact_age.keys()        
    lists = sorted(acc_exact_age.items()) # sorted by key, return a list of tuples
    x, y = zip(*lists) # unpack a list of pairs into two tuples
    plt.plot(x,y, label = net)

    if dataset == 'utk':
        scale = 100
    elif dataset == 'instagram':
        scale = 60

    plt.xticks(np.arange(0, scale, 6.0))
    plt.legend()

#
# This function will draw a line graph with the following attributes:
# 1. x axis represents the age
# 2. y axis represents the accuracy
# 3. each line represents one country for the network specified in the argument
#
def plot_country_accuracy(net, dataset, bin):
    path = './result_data/%s/pickle_%s_test_part_%s_bin_%s' %(dataset, net, dataset, bin)
    with open(path,'rb') as f:
        output = pickle.load(f)

        acc_age_correct = {}
        acc_age_total = {}
        acc_age_mean = {}
        acc_exact_age = {}
        acc_age_mean_country = {}

        for country in countries_utk.keys():

            for result in output:
                # Get Info
                path, name, exact_age, country_index, country_name, label_str, pred_label_str, label_num, pred_label_num, probs = parse_record_fields(dataset, result)

                # check for right country
                if country_name != country:
                    continue

                if label_num not in acc_age_correct.keys():
                    acc_age_correct[label_num] = 0
                    acc_age_total[label_num] = 0
                    acc_age_mean[label_num] = 0

                # add + 1 for correct classification
                if label_num == pred_label_num:
                    acc_age_correct[label_num] = acc_age_correct[label_num] + 1
                # add + 1 to count total age to divide correct count into mean
                acc_age_total[label_num] = acc_age_total[label_num] + 1

            # calc mean for each class
            for label_num in acc_age_correct.keys():
                new_num = label_num * bin
                acc_exact_age[new_num] = 0
                acc_age_mean[label_num] = acc_age_correct[label_num] / acc_age_total[label_num]
                acc_exact_age[new_num] = acc_age_correct[label_num] / acc_age_total[label_num]

            acc_age_mean_country[country] = acc_age_mean

            vals = acc_exact_age.keys()        
            lists = sorted(acc_exact_age.items()) # sorted by key, return a list of tuples
            x, y = zip(*lists) # unpack a list of pairs into two tuples
            plt.plot(x,y, label = country)

            plt.xticks(np.arange(0, 60, 6.0))
            plt.legend()

            #print(acc_age_mean)

    #print(acc_age_mean_country)

#
# This function will draw a line graph with the following attributes:
# 1. x axis represents the real age
# 2. y axis represents the predicted age
# 3. each line represents one country for the network specified in the argument
# 4. if no country specified, will use all data regardless of the country
#
def plot_data(net, bin, country = 'all', dataset='instagram'):
    path = './result_data/%s/pickle_%s_test_part_%s_bin_%s' %(dataset, net, dataset, bin)

    with open(path,'rb') as f:
        output = pickle.load(f)

        acc_age_shifts = {}
        acc_age_shifts_mean = {}
        acc_counts = {}
        acc_adj_age = {}
        acc_adj_bin = {}

        for i in range(0, 100):
            for result in output:
                # Get Info
                path, name, exact_age, country_index, country_name, label_str, pred_label_str, label_num, pred_label_num, probs = parse_record_fields(dataset, result)
                shift = pred_label_num - label_num 

                if country == country_name or country == 'all': 
                    if label_num not in acc_age_shifts.keys():
                        acc_age_shifts[label_num] = 0
                        acc_age_shifts_mean[label_num] = 0
                        acc_counts[label_num] = 0  
                    if label_num == i:
                        acc_age_shifts[label_num] += shift
                        acc_counts[label_num] += 1

    for label_num in acc_age_shifts.keys():
        new_num = label_num * bin
        acc_adj_age[new_num] = 0
        acc_adj_bin[label_num] = 0

        acc_age_shifts_mean[label_num] = acc_age_shifts[label_num] / acc_counts[label_num]
        acc_adj_age[new_num] = (label_num + acc_age_shifts_mean[label_num]) * bin
        acc_adj_bin[label_num] = (label_num + acc_age_shifts_mean[label_num])

        adult = [pred_age for age, pred_age in acc_adj_age.items() if age == 18]

    vals = acc_adj_age.keys()        
    lists = sorted(acc_adj_age.items()) # sorted by key, return a list of tuples
    x, y = zip(*lists) # unpack a list of pairs into two tuples

    scale = 60
    if dataset == 'utk':
        scale = 100
        
    b = np.linspace(0,scale)
    a = b
    plt.plot(a, b, color = 'red')
    plt.plot(x,y, label = country)

    plt.yticks(np.arange(0, scale, 6.0))
    plt.xticks(np.arange(0, scale, 6.0))
    plt.legend()

    #print(acc_adj_age)


#
# This function will draw a line graph with the following attributes:
# 1. x axis represents the accuracy
# 2. y axis represents the age
# 3. each line represents one country specified in the argument
# 4. if no country specified, will use all data regardless of the country
#
def plot_binary_data(net, bin, country = 'all', dataset = 'instagram'):
    path = './result_data/%s/pickle_%s_test_part_%s_bin_%s' %(dataset, net, dataset, bin)

    with open(path,'rb') as f:
        output = pickle.load(f)

        acc_age_correct = {}
        acc_age_total = {}
        acc_age_mean = {}

        for result in output:
            # Get Info
            path, name, exact_age, country_index, country_name, label_str, pred_label_str, label_num, pred_label_num, probs = parse_record_fields(dataset, result)

            adulthood = 18 / bin
            is_adult = label_num >= adulthood 
            is_pred_adult = pred_label_num >= adulthood 
            if country == country_name or country == 'all': 

                if label_num not in acc_age_correct.keys():
                    acc_age_correct[label_num] = 0
                    acc_age_total[label_num] = 0

                if is_adult == is_pred_adult:
                    acc_age_correct[label_num] += 1

                acc_age_total[label_num] += 1

    for label_num in acc_age_correct.keys():
        new_num = label_num * bin       
        acc_age_mean[new_num] = 0
        acc_age_mean[new_num] = acc_age_correct[label_num] / acc_age_total[label_num]

    #print(acc_age_mean)

    vals = acc_age_mean.keys()        
    lists = sorted(acc_age_mean.items())
    x, y = zip(*lists)

    plt.plot(x,y, label = country)
    plt.xticks(np.arange(0, 50, 6.0))
    plt.axvline(x = 18, color = 'red')

    plt.legend()

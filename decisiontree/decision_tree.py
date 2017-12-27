from util import entropy, information_gain, partition_classes
import numpy as np 
import ast

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = [[]]
        #self.tree = {}
        # pass
        self.leaf_size = 1
        self.depth_limit = 100
        self.verbose = False

    def learn(self, X, y, sr_no=0):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        # pass

        # Root node case
        # if sr_no == 0:

        num_features = len(X[0])
        num_data_points = len(y)

        table_rows = [[sr_no, -1, -1, 1, -1]]
        sr_no = sr_no + 1

        # Handle corner cases
        # If only one element in data given
        if len(X) == 1:
            # leaf = np.array([sr_no,-1,dataY,0,0])
            # y = y.tolist()
            table_rows[0][2] = y[0]
            table_rows[0][3] = 0
            table_rows[0][4] = 0
            # print table_rows
            return table_rows

        # if all same values of output in given data
        if len(np.unique(y)) == 1:
            # leaf = np.array([-1,-1,y[0],0,0])
            table_rows[0][2] = y[0]
            table_rows[0][3] = 0
            table_rows[0][4] = 0
            # print table_rows
            return table_rows

        # Is a Leaf test decided by num of elements remaining in X
        if len(X) <= self.leaf_size:
            # leaf = np.array([-1,-1,y.mean(),0,0])
            table_rows[0][2] = np.median(y)
            table_rows[0][3] = 0
            table_rows[0][4] = 0
            # print table_rows
            return table_rows

        # Usual case
        else:
            # cov = [0] * X.shape[1]
            # correl = [0] * X.shape[1]
            # for j in range(X.shape[1]):
            #     cov[j] = np.corrcoef([X[:,j],y])
            #     correl[j] = cov[j][0][1]
            #     if np.isnan(correl[j]):
            #         correl[j] = 0


            # Calculate gini gain for split on each features
            info_gains = [0]*num_features
            split_val = [0]*num_features

            max_info_gain = float("-inf")
            alpha_best = -1

            for alpha in range(num_features):
                ft = []
                for f in range(num_data_points):
                    ft.append(X[f][alpha])
                # ft = [X[f][alpha] for f in range(num_features)]
                # split_val[alpha] = np.mean(ft)

                if isinstance(ft[0], str):

                    ft.sort()
                    split_val[alpha] = ft[len(ft)/2]
                    # split_val[alpha] = np.median(ft)
                    test_split_classes = [[], []]
                    test_split_features = [[], []]

                    test_split_features[0], test_split_features[1], test_split_classes[0], test_split_classes[1] = partition_classes(X, y, alpha, split_val[alpha])

                    # for j in range(num_data_points):
                    #     if (X[j][alpha] <= split_val[alpha]):
                    #         test_split_features[0].append(X[j])
                    #         test_split_classes[0].append(y[j])
                    #     else:
                    #         test_split_features[1].append(X[j])
                    #         test_split_classes[1].append(y[j])

                    info_gains[alpha] = information_gain(y, test_split_classes)

                else:
                    split_val[alpha] = np.median(ft)
                    test_split_classes = [[],[]]
                    test_split_features = [[], []]

                    test_split_features[0], test_split_features[1], test_split_classes[0], test_split_classes[1] = partition_classes(X, y, alpha, split_val[alpha])

                    # for j in range(num_data_points):
                    #     if(X[j][alpha] <= split_val[alpha]):
                    #         test_split_features[0].append(X[j])
                    #         test_split_classes[0].append(y[j])
                    #     else:
                    #         test_split_features[1].append(X[j])
                    #         test_split_classes[1].append(y[j])

                    info_gains[alpha] = information_gain(y, test_split_classes)

            for alpha in range(num_features):

                if max_info_gain < info_gains[alpha]:
                    max_info_gain = info_gains[alpha]
                    alpha_best = alpha

            assert alpha_best >= 0
            opt_split_val = split_val[alpha_best]

            split_classes = [[], []]
            split_features = [[], []]

            split_features[0], split_features[1], split_classes[0], split_classes[1] = partition_classes(X, y, alpha_best, opt_split_val)
            # for j in range(num_data_points):
            #     if (X[j][alpha_best] <= opt_split_val):
            #         split_features[0].append(X[j])
            #         split_classes[0].append(y[j])
            #     else:
            #         split_features[1].append(X[j])
            #         split_classes[1].append(y[j])


            # best_feature = np.argmax(correl)
            # print correl
            # print best_feature
            # opt_split_val = np.median(X[:,alpha_best])

            # Take care of median cases here
            # If median doesnt yield new information then terminate as leaf node
            if (len(split_classes[0]) == num_data_points) or (len(split_classes[1]) == num_data_points):
                table_rows[0][2] = np.median(y) #mean is mode here!
                table_rows[0][3] = 0
                table_rows[0][4] = 0
                # print table_rows
                return table_rows

            leftree = self.learn(split_features[0], split_classes[0], sr_no)
            rightree = self.learn(split_features[1], split_classes[1], sr_no + len(leftree))

            # Update table entries for current node
            table_rows[0][1] = alpha_best
            table_rows[0][2] = opt_split_val
            table_rows[0][3] = 1
            table_rows[0][4] = 1 + len(leftree)

            for l in leftree:
                table_rows.append(l)
            for r in rightree:
                table_rows.append(r)

            # if self.verbose:
                # print table_rows

            return table_rows



    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        # pass

        if self.verbose:
            print record

        curr_node = self.tree[0]

        # while curr_node[3] != 0 and curr_node[4] != 0 :
        while True:

            if self.verbose:
                print curr_node

            # Reached leaf
            if curr_node[3] == 0 and curr_node[4] == 0:
                y = curr_node[2]

                if self.verbose:
                    print curr_node[2]

                break

            # Check whether to go in left or right branch
            if ((isinstance(record[curr_node[1]], str) and record[curr_node[1]] == curr_node[2]) or (isinstance(record[curr_node[1]], float) and record[curr_node[1]] <= curr_node[2])):
                curr_node = self.tree[curr_node[0] + curr_node[3]]
            else:
                curr_node = self.tree[curr_node[0] + curr_node[4]]

        return y


# def calculate_entropy(class_list):
#
#     classes = set(class_list)
#     counts = dict.fromkeys(classes, 0)
#     for c in class_list:
#         counts[c] = counts[c] + 1
#
#     prob = [c/float(sum(counts.values())) for c in counts.values()]
#
#     entropy = [0]*len(prob)
#     for i in range(len(prob)):
#         if prob[i] != 0:
#             entropy[i] = -prob[i] * np.log(prob[i], 2)
#         else:
#             entropy[i] = 0
#
#     total_entropy = sum(entropy)
#     return total_entropy
#
#
# def info_gain(previous_classes, current_classes):
#
#     total_entropy = calculate_entropy(previous_classes)
#
#     counts = [len(c) for c in current_classes]
#
#     assert(sum(counts) == len(previous_classes))
#
#     class_prob = [0]*len(current_classes)
#     class_entropy = [0]*len(current_classes)
#     remainder = 0.0
#
#     for i in range(len(current_classes)):
#         class_prob[i] = len(current_classes[i])/float(len(previous_classes))
#         class_entropy[i] = calculate_entropy(current_classes[i])
#         remainder = remainder + class_prob[i]*class_entropy[i]
#
#     info_gain = total_entropy - remainder
#     return info_gain

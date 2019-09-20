import pickle
import operator
import plotly
import plotly.plotly as py
import plotly.graph_objs as goo

# dataframe dict object for holding the history of timer uses
class pom_history(dict):
    # method to add new timer listing to the history
    def add_new(self,date,data):
        # see if date is already in history
        try:self[date]
        except:self[date] = {}
        # looks to see if assignment is already in history, then adds the information
        try:self[date][data[0]] = tuple(map(operator.add,self[date][data[0]],(data[1],data[2])))
        except:self[date][data[0]] = (data[1],data[2])
        # save dataframe in pickled object
        pickle_out = open("history.pkl", 'wb')
        pickle.dump(self, pickle_out, pickle.HIGHEST_PROTOCOL)
        pickle_out.close()

    # returns a list of all the assignment names in history
    def get_assns(self):
        assns = []
        [assns.append(asn) for dates in list(self.keys()) for asn in self[dates].keys() if asn not in assns]
        return assns

    def display_assns(self):
        fig = tools.subplots.make_subplots(rows=len(x), cols=1, shared_xaxes=True, shared_yaxes=True)
        dates,assns,vals = [],[],[]
        for item in list(self.items()):
            val_temp = []
            assn_temp = []
            dates.append(item[0])
            for assn in list(item[1].items()):
                assns.append(assn[0])
                assn_temp.append(assn[1])






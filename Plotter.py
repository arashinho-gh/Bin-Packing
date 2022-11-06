from matplotlib import pyplot as plt

class Plotter():

    def sortData(self,arr):
        arr.sort(key = lambda x: x[0])
        for i in range(len(arr)):
            arr[i] = arr[i][1]
        return arr
    
    def metric_graph(self, dic, xaxis, filename):

        for metric in dic.keys():
            fig = plt.figure()
            for algotype in dic[metric].keys():
                for algo, data in dic[metric][algotype].items():
                    data = self.sortData(data)
                    plt.plot(xaxis, data, linestyle='--', marker='o',label = f"{algo} - {algotype}")
                
            plt.title(f'{metric}')
            plt.xlabel('|weights|')
            plt.ylabel(metric)
            plt.legend()
            fig.savefig(f'{metric}-{filename}.png')

        
    def executionTime_graph(self, dic, xaxis, filename):

        def calcAvg(obs):
            for key, val in obs.items():
                obs[key] = (sum(val) / len(val)) * 1000
            return obs

        observed = calcAvg(dic)
        
        data = {}
        
        for key, val in (observed.items()):
            _type = key[0]
            algo_name = key[1]
            numWeights = key[2]
            cap = key[3]
            
            data[_type] = data.get(_type, {})
            data[_type][algo_name] = data[_type].get(algo_name, [])
            data[_type][algo_name].append((int(numWeights), val))

        # sort data
        for key, val in data.items():
            for algo in data[key]:
                temp = data[key][algo]
                data[key][algo] = self.sortData(temp)
        # plot
        for key in data.keys():
            fig = plt.figure()
            for algo in data[key]:
                # print(data[key][algo][1])
                plt.plot(xaxis, data[key][algo], label = algo + "-" + key, linestyle='--', marker='o')    
            plt.legend()
            plt.xlabel('|weights|')
            plt.ylabel('avg time(ms)')
            fig.savefig(f'./{key}-execution_benchmark-{filename}.png')

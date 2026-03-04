class Thread:
    def __init__(self):
        self.timelist = []

    class Parameter:
        '''
        Usage of running_or_waiting parameter: receive "running" "waiting" or 1 , 0  corresponding in order.
        '''
        def __init__(self, param: int | str):
            #check
            if isinstance(param, int):
                
                if param >= 2 or param < 0:
                    print("Warning: parameter is exceed to 1 or invalid, will directly mod 2")
                
                param%2 == 1 
            
            elif param == "running" or param == "waiting" :
                param = (1 if param == "running" else 0)
            else:
                raise ValueError(f"Invalid parameter:{param}")

            self._param = param

        def __str__(self):
            return "running" if self._param else "waiting"
        
        def switch(self):
            self._param = 0 if self._param else 1
        def __bool__(self):
            return True if self._param else False
        def __eq__(self,other):
            return self._param == other
        def __ne__(self,other):
            return self._param != other


    def add_time(self,time,running_or_waiting: int | str):

        #Value Check
        if not isinstance(time, int):
            print("Warning: time is not int.")
            try:
                time = int(time)
            except ValueError as e:
                print(f"Invalid time!: \n{e}")
                return
        elif time <= 0 :
            raise ValueError("Time won't be 0 or negative.")

        param = self.Parameter(running_or_waiting)

        #default running first than waiting
        flag = len(self.timelist) % 2
        if flag == param:
            print(f"The last time slice was {param}, will directly added.")
            self.timelist[-1] += time
        else:
            self.timelist.append(time)

    def __str__(self):
        output = "Time needed:\n"
        total = 0
        for i,time in enumerate(self.timelist):
            if i % 2:
                output += f"Waiting {time} sec\n"
            else:
                output += f"Running {time} sec\n"
            total += time
        output += f"Total need {total} times."
        return output




if __name__ == "__main__":
    thread1 = Thread()
    thread1.add_time(23, 1)
    thread1.add_time(15,0)
    thread1.add_time(42,1)
    thread1.add_time(52,0)
    print(thread1)



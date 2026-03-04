
class Status:
    '''
    Usage of running_or_waiting parameter: receive "running" "waiting" or 1 , 0  corresponding in order.
    '''
    def __init__(self, param: int | str):
        #check
        if isinstance(param, int):
            
            if param >= 2 or param < 0:
                raise ValueError("Warning: parameter is exceed to 1 or invalid, will directly mod 2")
            
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
        if isinstance(other, int):
            #print("Warning: Comparing to int, which is not recommend.")
            return self._param == other
        elif isinstance(other, Status):
            return self._param == other._param
        else:
            raise ValueError("Param not match.")

    def __ne__(self,other):
        return self._param != other


    def __add__(self, other):
        return self._param + other


class Thread:
    def __init__(self):
        self._timelist = []
        self.status = Status(1)

    def add_time(self,time,running_or_waiting: int | str):

        #Value Check
        if not isinstance(time, int):
            try:
                print("Warning: time is not int.")
                time = int(time)
            except ValueError as e:
                raise ValueError(f"Invalid time!: {time}\n{e}")
        elif time <= 0 :
            raise ValueError("Time won't be 0 or negative.")

        param = Status(running_or_waiting)

        #default running first than waiting
        if param == (self.status + len(self._timelist)-1 )%2 and len(self._timelist) != 0:
            print(f"The last time slice was {param}, will directly added.")
            self._timelist[-1] += time
        else:
            self._timelist.append(time)

    def __str__(self):
        output = "Time needed:\n"
        total = 0
        for i,time in enumerate(self._timelist):
            if  (self.status + i) % 2 :
                output += f"Running {time} sec\n"
            else:
                output += f"Waiting {time} sec\n"
            total += time
        output += f"Total need {total} times."
        return output

    def running(self, time, running_or_waiting):
        '''
        consume time and return times if left.
        '''
        status = Status(running_or_waiting)
        if self.status == status:
            if(time > self._timelist[0]):
                self.status.switch()
                return time - self._timelist.pop(0)
            else:
                self._timelist[0] -= time
                return 0
        else:
            raise TypeError("Status not match!")

class System:
    def __init__(self):
        self.threads = []

    def add(self,thread):
        self.threads.append(thread)

    def run(self,pid,time):
        if pid >= -1:
            remaining_time = 0
            if self.threads[pid].status == 1:
                remaining_time = self.threads[pid].running(time,1)
            else:
                raise ValueError(f"The {pid} thread can't be running as it is waiting for the IO stream. If you want to let CPU idle, please input pid -1")
            for index, thread in enumerate(self.threads):
                if index != pid and thread.status == 0:
                    thread.running(time - remaining_time,0)
            return remaining_time
        else:
            raise ValueError("The pid can't be negative except for -1(idle).")


    def __str__(self):
        output = "Running threads:\n"
        for pid,thread in enumerate(self.threads):
            output += f"Thread {pid}, {thread.status}\n"
        return output

    def threads_manager(self):
        '''
        Now you need to write the threads manager.
        There are several threads stored in self.threads
        each thread has its own status by checking the thread.status
        1 represents it should be tackled by cpu ASAP, and 0 represents it is waiting for the IO streaming.
        using self.run(pid,time) to let self.threads[pid] run {time} sec. or let cpu idle by setting pid -1.
        you need to find a way to run all the threads gracefully.
        Besides, I don't want you to use the other functions or parameters as they are useless or may causing weird bugs. 
        And the real system won't get the remaining running time of the threads
        But if you like, or you want to optimize it to be stronger, I will tell you that all of the Class has __str__ functions.
        Good luck.

        By the way, you can check the remaining time by the return value of the self.run() if a thread enters waiting status before {time} runs out.
        '''




if __name__ == "__main__":
    
    examples = [
    [3, 1, 2, 4, 1],
    [5, 2, 1],
    [2, 5, 3, 2],
    [7, 3, 2, 1, 4, 2],
    [4, 1],
    [6, 4, 3, 1, 2],
    [1, 2, 5, 3, 2, 1, 3],
    [8, 1]
    ]
    '''
    thread1 = Thread()
    thread1.add_time(23, 1)
    thread1.add_time(15,0)
    thread1.add_time(42,1)
    thread1.add_time(52,0)
    print(thread1)
    '''
    system = System()
    for example in examples:
        thread = Thread()
        for index,i in enumerate(example):
            thread.add_time(i,(index+1)%2)
            #print("A time slice added.")
        #print(f"A thread added: \n{thread}")
        system.add(thread)
    print(system)


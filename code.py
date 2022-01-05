import csv
import random
from timeit import default_timer as timer
from datetime import timedelta
import statistics as st


Main_list=[] #a String list include alle the file's info

with open('european_cities.csv', 'r') as csv_file:
    csv_file=csv.reader(csv_file)
    for line in csv_file:
        for e in line:
            Main_list.append(e.split(';'))

cities=Main_list[0] #make a new String list of the  cities' names

temp=Main_list[1:25][0:25] #copy the values of the file (without the first raw,i.e. cities' names)
distances=[]
#convert the values from String to float for comparing later
for list in temp:
    s=[]
    for element in list:
        s.append(float(element))
    distances.append(s)



inexesOfCities=[]




def perm1(lst):
	if len(lst) == 0:
		return []
	elif len(lst) == 1:
		return [lst]
	else:
		l = []
		for i in range(len(lst)):
			x = lst[i]
			xs = lst[:i] + lst[i+1:]
			for p in perm1(xs):
				l.append([x] + p)
		return l


def salesman_exhaustive_search(antall_cities):
    for i in range(antall_cities):  # number cities the salesman wil visit
            inexesOfCities.append(i)

    random_perms =perm1(inexesOfCities)
    sumlist=[]
    indexOfShortestPath=0
    totalDisforShotestPath=0
    for perm in random_perms:
        # print(perm)
        count=0
        sum=0
        while count<len(perm)-1:
            dis=distances[perm[count]][perm[count+1]]
            sum+=dis
            count+=1
        sum+=distances[perm[count]][perm[0]]  # add the distanse between the last city and the home city
        sumlist.append(sum)



    totalDisforShotestPath=min(sumlist)
    indexOfShortestPath = sumlist.index(min(sumlist))
    ShortestPath_sequenceOgCities=[]
    for i in random_perms[indexOfShortestPath]:
        ShortestPath_sequenceOgCities.append(cities[i])

    ShortestPath_sequenceOgCities.append(ShortestPath_sequenceOgCities[0])#add the home city(I mean go back home)
    return "Shortest path  via salesman_exhaustive_search for ",antall_cities," cities  is :", ShortestPath_sequenceOgCities,  "total ditanse among these  cities is: ", totalDisforShotestPath, "km"








def calculate_distanse(perm):
    for i in range(24):  # number cities the salesman wil visit
            inexesOfCities.append(i)
    count2=0
    distanse=0
    #sum/calculate the ditances among the cities for an improvement
    while count2<len(perm):
            #include in calculation the distance between the last city and home city
            if count2==len(perm)-1:
                distanse+=distances[perm[0]][perm[len(perm)-1]]
                count2+=1
            #calculate the ditances among the cities in current version of perm
            else:
                dis=distances[perm[count2]][perm[count2+1]]
                distanse+=dis
            count2+=1
    return distanse

def swapToCities(city1, city2, perm):
    if city1!= city2 :
        temp=perm[city1]
        perm[city1]=perm[city2]
        perm[city2]=temp

#................................... ...........................................................................
#.......................hill climber ...........................................................................
#................................... ...........................................................................



#method takes n number cities
def hill_climber(n_cities):

    perm=random.sample(range(0, n_cities),n_cities) #one single random perm

    ditances_perm=calculate_distanse(perm) #one single random perm

    temp_perm=perm.copy() #take a copy of perm to use it in the comparison

    for counter in range(100000): #3000000
        c1= random.randint(0,n_cities-1)# one random city
        c2= random.randint(0,n_cities-1)#another random city
        swapToCities(c1, c2, temp_perm) #swapping between cities

        if calculate_distanse(temp_perm) < ditances_perm :
            ditances_perm=calculate_distanse(temp_perm)
            perm=temp_perm.copy()
        else:
            temp_perm=perm.copy()

    return  ditances_perm, perm





#............................................................................
#................................Genetic algorithm...........................
#............................................................................


def crossover(dad, mum):
    i=random.randint(0,len(dad)-1)
    #j=random.randint(0,len(mum)-1)
    son=dad[0:i]
    for e in range(len(mum)):
        if mum[e] not in son:
            son.append(mum[e])

    daughter=mum[:i]
    for e in range(len(dad)):
        if dad[e] not in daughter:
            daughter.append(dad[e])
    return [son,daughter]



#generate a new population and calculate the total distance for every permutation in this population and does parents selsection
def population_and_totalDistanses():
        population,  evaluation_of_population=[], []
        for p in range(100): #I assumed that we have 100 generations
            population.append(random.sample(range(0, 24),24))#I assumed that we have 24 cities
        sumlist=[]
        for p in population:
            # print(perm)
            count=0
            sum=0
            while count<len(p)-1:
                dis=distances[p[count]][p[count+1]]
                # print("distanse", dis, " between", count, " and ", count+1)
                sum+=dis
                count+=1
            sum+=distances[p[count]][p[0]]  # add the distanse between the last city and the home city
            evaluation_of_population.append(sum)

        population_and_distanses=[]
        for i in range(100):
            population_and_distanses.append( [evaluation_of_population[i], population[i]])


        population_and_distanses.sort() # sort the list based on the distanse # the shortest paths come first
        #.....parent selection.....
        population_and_distanses= population_and_distanses[:50] # re-size the list # remain the best 50 solutions
        return population_and_distanses




#offspring_mutation_newGen
def offspring_mutation_newGen(population_and_distanses):

    #..................make offspring...............
    children=[]

    counter=0
    while counter <25:
        son_and_doughter= crossover( population_and_distanses[counter][1],population_and_distanses[counter+1][1])
        children.append([calculate_distanse(son_and_doughter[0]),son_and_doughter[0] ])
        children.append([calculate_distanse(son_and_doughter[1]),son_and_doughter[1] ])
        counter+=1

    #...........mutatation for the new candidates...............
    for i in range(50):
        temp_perm=children[i].copy() #take a copy of perm to begin with
        c1= random.randint(0,24-1)# one random city
        c2= random.randint(0,24-1)#another random city
        swapToCities(c1, c2,temp_perm[1]) #swapping between cities
        temp_per_distance=calculate_distanse(temp_perm[1])
        temp_perm[0]=temp_per_distance
        if temp_per_distance < children[i][0] :
            children[i]= temp_perm.copy()


    #...........make a new generation of the old one...............
    population_and_distanses.extend(children) # add the children with the fittest earlier generation as a new generation
    population_and_distanses.sort()
    return population_and_distanses


def Generate_generations():
    distanses=[]
    population_dis=population_and_totalDistanses()
    prev_generation=offspring_mutation_newGen(population_dis)
    for i in range(300): # I have chosen 50 generations
        next_gen=offspring_mutation_newGen(prev_generation)
        distanses.append(next_gen[i][0])
        prev_generation=next_gen
        #print("gen nr ",i)

    print("the best result is: ",prev_generation[0])
    print("the worst result is: ",prev_generation[-1])
    print("the standard deviation", st.stdev(distanses))


#....................................main area................................................................................

def main():


    print("................excustive search algorithm........................")
    start = timer()
    print( salesman_exhaustive_search(6))
    end = timer()
    print("estimated time:", timedelta(seconds=end-start))

    print("................hill climbing algorithm........................")
    distanses_and_perms=[]
    distanses=[] #just take out the distanses from the final distanses_and_perms to be able to use it as a parameter for stdev( ...)
    for e in range(20):
        #print("iteration", e )
        distanses_and_perms.append(hill_climber(24))
        distanses.append(distanses_and_perms[e][0])
    best_resultat=min(distanses_and_perms)
    print("the standard deviation", st.stdev(distanses))
    # worst_resultat=max(distanses_and_perms)   #remember to reverse the operator < in if-check
    print("After these 20 iterations, here is the best Best_result I have gotten: \n", best_resultat)
    # print("After 20 iterasjoner, her is the worst Best_result I have gotten: \n", worst_resultat)    #remember to reverse the operator < in if-check
    print("................Genetic algorithm........................")
    Generate_generations()
main()

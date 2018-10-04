default_students = [
	"Alice",
	"Bob",
	"Charlie",
	"David",
	"Eve",
	"Fred",
	"Ginny",
	"Harriet",
	"Ileana",
	"Joseph",
	"Kincaid",
	"Larry"
]

plants = { 
	'C':"Clover",
	'G':"Grass",
	'R':"Radishes",
	'V':"Violets" 
}

class Garden:
    def __init__(self, plants, students=default_students):
        self.students = sorted(students)
        self.plant = plants.split()

    def plants(self, student):
        pln_indx = self.students.index(student)*2
        s_plants = [self.plant[0][pln_indx], self.plant[0][pln_indx+1],
                    self.plant[1][pln_indx], self.plant[1][pln_indx+1]]
        return [plants[p] for p in s_plants]
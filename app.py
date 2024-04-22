import streamlit as st
#from IPython.display import clear_output

def main():
    st.title("Exam Scores")
    classNumber = st.number_input("Enter class number ( 1 - 8 ):", min_value =1, max_value =8)

    if st.button("CALCULATE"):
        FILE_PATH = "./Data Files/" + "class" + str(classNumber) + ".txt"
        f = open(FILE_PATH,"r+")
        # st.write(f.readlines())
        filename = "class"+ str(classNumber)
        #st.write(filename)

        def analyzeClass():
            st.write("   **** ANALYZING ****")
            k = 0 # number of lines
            error = 0 # number of lines error
            good_number = 0
            pretty_good_number = 0
            medium_number = 0
            bad_number = 0
            grade = [] #list grade
            valid_line = []
            highest = []
            good = []
            pretty_good =[]
            medium = []
            bad = []
            answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(",") 
            student_number = []
            skip_answer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            wrong_answer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            
            for line in f.readlines(): # vong lap kiem tra cac loi cua du lieu
                k += 1
                listValue = line.rstrip("\n").split(",")
            
                if len(listValue) !=26:
                    st.write("Invalid line of data: does not contain exactly 26 values:")
                    st.write(line,"\n")
                    error += 1
                elif not listValue[0][1:].isnumeric() or len(listValue[0]) !=9:
                    st.write("Invalid line of data --> N#:",listValue[0], "format is invalid:")
                    st.write(line,"\n")
                    error += 1
                else:
                    valid_line.append(listValue)

            for line in valid_line: # cham diem
                student_number.append(line[0])
                answer = line[1:]
                score = 0
                for j in range(25):
                    if answer[j] == answer_key[j]:
                        score += 4
                    elif answer[j] == "":
                        score += 0
                        skip_answer[j] += 1
                    else:
                        score -= 1
                        wrong_answer[j] += 1

                grade.append(score)
            
                
            skip_order = []
            for i in range(25):
                if skip_answer[i] == max(skip_answer):
                    skip_order.append(i+1)
            
            wrong_order = []
            for i in range(25):
                if wrong_answer[i] == max(wrong_answer):
                    wrong_order.append(i+1)
        
            FILE_PATH_GRADE = "./Data Files/" + filename + "_grade.txt"
            with open(FILE_PATH_GRADE,"w") as fw:
                for sn, gr in zip(student_number,grade):
                    fw.write(sn + ":" + str(gr) + "\n")
                    
            with open(FILE_PATH_GRADE,"r") as fr:        
                for line in fr.readlines():
                    if int(line[10:]) == max(grade):
                        highest.append(line[:9])       
                
            with open(FILE_PATH_GRADE,"r") as fr:        
                for line in fr.readlines():            
                    if int(line[10:]) >= 90:
                        good.append(line[:9])
                        good_number += 1
                    elif int(line[10:])>= 70 and int(line[10:]) < 90:
                        pretty_good.append(line[:9])
                        pretty_good_number +=1
                    elif int(line[10:])>= 50 and int(line[10:]) < 70:
                        medium.append(line[:9])
                        medium_number +=1
                    elif int(line[10:]) < 50:
                        bad.append(line[:9])
                        bad_number += 1
                    
            if error == 0:
                st.write("No errors found!\n")
            
            st.write("   ***** REPORT *****")
            st.write("Total valid lines of data:", k-error,"\n")
            st.write("Total invalid lines of data:", error,"\n")
            st.write("Mean (average) score:", sum(grade)/len(grade),"\n")
            st.write("Highest score:", max(grade))
            st.write(f"Students {highest} get the highest score:", max(grade), "\n")
            st.write("Lowest score:", min(grade), "\n")
            st.write("Range of scores:", max(grade) - min(grade), "\n")
            
            s = sorted(grade)
            n = len(grade)
            if n % 2 == 1:
                median = s[n//2]
            else:
                median = sum(s[n//2-1 : n//2+1])/2.0
            st.write("Median score:", median, "\n")
            
            st.write("Number of students achieving excellent results (score >= 90):", good_number,"/",k-error, "density", round(good_number/(k-error),2))
            st.write("Number of students achieving is quite good (70 <= score < 90):", pretty_good_number,"/",k-error, "density", round(pretty_good_number/(k-error),2))
            st.write("Number of students achieving average score (50 <= score < 70):", medium_number,"/",k-error, "density", round(medium_number/(k-error),2))
            st.write("Number of students scoring poorly (score < 50):", bad_number,"/",k-error, "density", round(bad_number/(k-error),2),"\n")
            st.write(f"Question that most people skip: order--> {skip_order} ," " quantity--> ",max(skip_answer), "ratio", max(skip_answer)*100//(k-error), "%\n")
            st.write(f"Question that most people answer incorrectly: order--> {wrong_order} ," " quantity--> ",max(wrong_answer), "ratio", max(wrong_answer)*100//(k-error), "%\n")
            
            st.write("Sucessfully write file " + filename + "_grade.txt \n")    
        analyzeClass()  
        

if __name__ == "__main__":
  main()
import subprocess
import plistlib as pb

"""
FUN FACT:
this script actually doesn't user any 3rd party libraries :)
(except of its use of pandoc ...)
"""

with open('semester.xml', 'rb') as file:
    plist = pb.load(file)

data = plist['data']
class_ = data['class']
name = data['name'] #string
subjects = data['subjects'] #array

md_file = ""

#filename for output files (one md one html)
filename = "semester.md"

sj_marks = 0
sj_marks_no = 0

pluspoints_all = 0

def add2mdfile(content):
    global md_file
    md_file += str(content)

def add_break(count):
    add2mdfile("\n"*count)

def add_row(exam, mark, weight, header=0):
    if header == 1:
        base_md = "|{}|{}|{}|\n"
    else:
        base_md = "| {} | {} | {} |\n"
    md_tb_row = base_md.format(exam, mark, weight)
    add2mdfile(md_tb_row)

def add_header(one, two, three):
    add_break(1)
    add_row(one, two, three)
    add_row("-"*3,"-"*3,"-"*3,header=1)

def add_h1(title):
   add2mdfile("""# {}\n""".format(title))

def round2_05(number):
    number = float(number)
    return round(number * 2)/2

# Parse Subjects' Exams, Marks
for sj in subjects:
    marks = 0
    marks_num = float(0)

    sj_name = sj['name']
    sj_exams = []

    add_h1(sj_name)
    add_header("Exam", "Mark", "Weight")

    for exam in sj['exams']:
        mark = exam['mark']
        weight = exam['weight']
        marks += float(mark) * (float(weight)*100) #converts weigt to percents % 
        marks_num += float(weight)

        add_row(exam['name'], str(mark), str(weight))

    # Calculate Average of the Subject
    # adds the average of the subjects' exams if not 0
    try:
        average = (marks/marks_num)/100 # because * 100 further up
        if sj['counted']:
            if float(average) > 0.0:
                sj_marks += average
                sj_marks_no += 1
        else:
            None
    except ZeroDivisionError:
        average = 0.0

    rounded_avg = float(round2_05(average))

    if sj['counted']:
        if average == 0.0:
            pluspoints = 0.0
        elif average < 4.0 and average > 0.0:
            pluspoints = (rounded_avg - 4.0)*2.0
        elif average >= 4.0:
            pluspoints = rounded_avg - 4.0
    else:
        pluspoints = 0.0
    
    pluspoints_all += pluspoints

    add_break(1)
    add2mdfile('_**∅:** {} ({})_ | _**PP**: {}_\n\n'.format(rounded_avg, average, pluspoints))

MARKDOWN = """
{}
# Average All Subjects: _{}_
# PlusPoints: _{}_
""".format(md_file, sj_marks/sj_marks_no, pluspoints_all)

with open(filename, 'wb') as out_md:
    out_md.write(MARKDOWN.encode('utf-8'))
    out_md.close()

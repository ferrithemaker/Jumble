import mysql.connector
from fpdf import FPDF

class CvPDF(FPDF):

	def header(self):
		# Set up a logo
		mycursor.execute("SELECT info FROM contents WHERE type='image'")
		myresult = mycursor.fetchone()
		self.image(myresult[0], 10, 8, 33)
		self.set_font('Arial', 'B', 15)
		mycursor.execute("SELECT info FROM contents WHERE type='name' or type='email' or type='address'")
		myresult = mycursor.fetchall()
		for element in myresult:
			self.cell(100)
			self.cell(0, 5, element[0], ln=1)
		# Line break
		self.ln(20)

	def footer(self):
		self.set_y(-10)
		self.set_font('Arial', 'I', 8)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="curriculum"
)

mycursor = mydb.cursor()


pdf = CvPDF()
# Create the special value {nb}
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 12)
line_no = 1
for i in range(50):
	pdf.cell(0, 10, txt="Line #{}".format(line_no), ln=1)
	line_no += 1
pdf.output('cv.pdf')

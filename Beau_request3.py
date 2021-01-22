import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

def get_soup(pages,stocks):
	requests.packages.urllib3.disable_warnings()
	response = requests.get("https://www.cophieu68.vn/historyprice.php?currentPage=%d&id=%s" %(pages,stocks),headers=HEADERS,verify=False).content 
	soupdata = bs(response, 'html.parser')
	return soupdata

def appending(objects):
	global content_array
	results= objects.text.split("\n")
	results= [e for e in results if e not in ('')]
	content_array.append(results)
	return None

def To_excels(objects,stocks):
	df=pd.DataFrame(objects) 
	df.to_excel('./All_prices/%s.xlsx'%(stocks),  engine='xlsxwriter' )
	return None

def write_txt(stocks):
	w= open("./All_prices/Done.txt","a+")
	w.write(stocks + ",")
	w.close()
	return None

def check_404(pages,stocks):
	global i
	while True:
		try:
			soup=get_soup(pages,stocks)
			head = soup.find("tr", class_="tr_header")
			# print(head)
			if head== None:
				i+=1
			else:
				appending(head)
				print("Đang thu thập mã: %s" %stocks)
				break
		except:
			pass
	return None


def check_ending(pages,stocks):
	while True:
		pages += 1 
		try:
			print("Đang thu thập dữ liệu từ trang: %s" %pages)
			soup=get_soup(pages,stocks)
			# Bodies= (soup.find_all("tr", onmouseover="hoverTR(this)"))
			Bodies= (soup.find_all("tr"))

			for i in range(0,7):
				Bodies.pop(0)

			# print(len(Bodies))

			if len(Bodies)==0:
				# print(len(Bodies))
				print("Đã thu thập dữ liệu cổ phiểu: %s, số trang: %d"%(stocks,pages))
				break
			else:
				# print(len(Bodies))
				for n in range(0,26):
					appending(Bodies[n])		
		except:
			pass
	return None

def input_data():
	cont = 0
	data = []
	while True:
		if cont != 'end':
			dat = input("Nhập mã cổ phiếu bạn muốn thu thập: ")
			data.append(dat)
			cont = input("Bạn có muốn nhập nữa không (Nhập end để kết thúc, nhập bất cứ ký tự nào khác để tiếp tục): ")
		else:
			break
	return data


# Ngành= input("Nhập tên ngành:")
# print("Thu thập dữ liệu ngành %s"%Ngành)
f= open("./All_prices/sorted_all_prices.txt","r")
String_tên_mã= f.read()
A= String_tên_mã.split(",")
f.close()
# print(A)

# Check for available:
# h= open("./Available_stock/All industry.txt","r")
# ind= g.read()
# B1= String_tên_mã.split(",")
try:
	g= open("./All_prices/Done.txt","r")
	String_tên_mã= g.read()
	B= String_tên_mã.split(",")
	lst=B[len(B)-2]
	i=A.index(lst)+1
	g.close()
except:
	i=0
print(i)

cont = A.index('SGC')
print(A[cont])

A = A[cont+1:]

# A = ["%5Evnindex"]

# A = ["GVR"]

print("{:*^100}".format("Chương trình thu thập giá cổ phiếu"),"\n")
# print("{:*^100}".format(" Hi chị Nguyệt ^^ "),"\n")
print("{:*^100}".format("Start"),"\n")
print("{:*^100}".format(""))

# A = input_data()

i=0

while True:
	if i<=len(A)-1:
		page=0
		content_array=[]

		# Xử lý 404 Forbiden:
		check_404(1,A[i])

		check_ending(page,A[i])

		To_excels(content_array,A[i])
		# write_txt(A[i])
		# print("Đã thu thập xong dữ liệu %s"%A[i])
		print("\n")

		i+=1 
	else:
		break

print("Đã xong!")






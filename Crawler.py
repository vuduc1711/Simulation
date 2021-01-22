# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


class stock_cp68:
    def __init__(self, stock_id, save_path):
        self.stock_id = stock_id
        self.save_path = save_path
        self.stock_data = pd.DataFrame()

    def crawl_stock(self):
        page = 1
        while True:  # Create a loop to take data
            # Link
            requests.packages.urllib3.disable_warnings()
            response = requests.get(f"https://www.cophieu68.vn/historyprice.php?currentPage={page}&id={self.stock_id}",
                                    verify=False).content
            soup = bs(response, 'html.parser')
            #             print(soup)
            # Check if the data table exist/ if exist crawl data
            if soup.select('.tr_header + tr'):
                print(f"Element exists! Crawling page {page}")
                #                 print(soup.select('.tr_header > td'))

                # Navigate through table
                datas = soup.select('.stock > tr > td')
                #                 print(datas)
                data_list = [data.text.replace('\n', '') for data in datas]
                #                 print(data_list)
                # Rearranging data into shape
                data_frame = [data_list[i:i + 13] for i in range(0, len(data_list), 13)]

                # Remove header
                data_frame.pop(0)

                # Join data
                self.stock_data.append(data_frame)

                # Next page
                page += 1

            else:
                print("Element not exists! Exit Crawl!")
                break

        # Append Header
        self.stock_data.columns = ['STT', 'Ngày', 'Giá Tham Chiếu', '+/- (*)', ' % (*)', 'Đóng Cửa (*)',
                                   'Khối Lượng', 'Mở Cửa (*)', 'Cao Nhất(*)', 'Thấp Nhất(*)',
                                   'Giao Dịch Thỏa Thuận', 'Nước Ngoài Mua', 'Nước Ngoài Bán']
        # Save to CSV
        self.stock_data.to_csv(f'{self.save_path}{self.stock_id}.csv', index=False)
        print(f'Done! Total page is:{page - 1}')


# -----Test-----
if __name__ == '__main__':
    # path = 'test_data/'
    # FPT = stock_cp68('FPT', path)
    # FPT.crawl_stock()

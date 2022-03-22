import csv
import os
from shortest_url_handler import Shortest_Url_Handler
import xlwt

if __name__ == '__main__':
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('data')
    ro = -1
    co = 0
    time = 0
    with open('files/ori_data.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cur = ''
        for row in reader:
            time += 1
            if time > 10:
                break
            if len(row[2]) != 0:
                ro += 1
                co = 0
                cur = row[2]
                print(cur)
                worksheet.write(ro, co, cur)
                co += 1

            items = [row[7], row[10], row[13]]
            for item in items:
                l = item.find('http://')
                if l == -1:
                    l = item.find('https://')
                if l == -1:
                    continue
                r = l
                while r < len(item) and item[r] != ' ' and item[r] != '\n':
                    r += 1
                url = item[l:r]
                suh = Shortest_Url_Handler(url)
                mes, url, similarity = suh.get_shortest_url()
                output = '{}: {} -> {:.2f}%'.format(mes, url, similarity*100)
                print(output)
                worksheet.write(ro, co, output)
                co += 1
        workbook.save('data.xlsx')
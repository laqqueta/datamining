import openpyxl as xl
import math
import pandas as pd

def to_array():
    arr = [[0]*3 for _ in range(200)]
    
    path = 'data-kmeans.xlsx'
    load_file = xl.load_workbook(path)
    xl_data = load_file.active
    
    row = 2
    
    for i in range(200):
        col = 1
        
        for j in range(3):
            arr[i][j] = xl_data.cell(row=row, column=col).value
            col += 1
        
        row += 1
    
    load_file.close()
    
    return arr

def main():
    data = to_array()
    
    cent = [
        [48, 101.41],
        [64, 239.64]
    ]
    
    c1_grp_tmp = []
    c2_grp_tmp = []
    iter = 1
    
    while True:
        c1 = []
        c2 = []
        c1_grouping = []
        c2_grouping = []
    
        print(f'Iterasi ke-{iter}')
        
        # Hitung jarak dari centeroid
        for db in range(len(data)):
            dk = 1
            res_c1 = 0
            res_c2 = 0
            
            for b in range(len(cent)):
                for k in range(len(cent)):
                    if k == 0:
                        res_c1 += pow(data[db][dk] - cent[k][b], 2)
                    else: # k+1 % 2 == 0
                        res_c2 += pow(data[db][dk] - cent[k][b], 2)
                dk += 1
                
            c1.append(math.sqrt(res_c1))
            c2.append(math.sqrt(res_c2))
        
        # Pengelompokan data
        for i in range(len(c1)):
            min_cent = min(c1[i], c2[i])
            
            if c1[i] == min_cent:
                c1_grouping.append([data[i][0], data[i][1], data[i][2]])
            else:
                c2_grouping.append([data[i][0], data[i][1], data[i][2]])
        
        # Output
        df_centeroid = pd.DataFrame(data={'ID' : [x[0] for x in data], 'C1' : [x for x in c1], 'C2' : [x for x in c2]})
        df_c1group = pd.DataFrame(data={'Subject ID' : [x[0] for x in c1_grouping], 'Umur' : [x[1] for x in c1_grouping], 'Rata - Rata Glukosa' : [x[2] for x in c1_grouping]})
        df_c2group = pd.DataFrame(data={'Subject ID' : [x[0] for x in c2_grouping], 'Umur' : [x[1] for x in c2_grouping], 'Rata - Rata Glukosa' : [x[2] for x in c2_grouping]})
        
        with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 2):
            
            print('Hasil Perhitungan Jarak dari Centeroid')
            print(df_centeroid.to_string(index=False))
            print('\nHasil Pengelompokan data: ')
            print('C1:')
            print(df_c1group.to_string(index=False))
            print('*'*60)
            print('C2: ')
            print(df_c2group.to_string(index=False))
        
        # Hitung centeroid baru
        for i in range(0, 2, 1):
            ind = 1
            for j in range(0, 2, 1):
                res = 0
                if i == 0:
                    for c1 in c1_grouping:
                        res += c1[ind]
                    cent[i][j] = res/len(c1_grouping)
                else:
                    for c2 in c2_grouping:
                        res += c2[ind]
                    cent[i][j] = res/len(c2_grouping)
                ind += 1

        if c1_grp_tmp == c1_grouping and c2_grp_tmp == c2_grouping:
            break
        else:
            print('\nHasil Perhitungan Centeroid baru')
            print(f'C1: {cent[0][0]}, {cent[0][1]}')
            print(f'C2: {cent[1][0]}, {cent[1][1]}')
        
        c1_grp_tmp = c1_grouping
        c2_grp_tmp = c2_grouping
        
        iter += 1
        print('='*40)
        input()
    
    print()
    print('-'*40)
    print('Final Result: \n')
    
    print('Anggota C1: \n')
    for c1 in c1_grouping:
        print(f'{c1[0]} ', end='')
    
    print()
    
    print('\nAnggota C2: \n')
    for c2 in c2_grouping:
        print(f'{c2[0]} ', end='')
                
if __name__ == "__main__":
    main()
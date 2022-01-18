import pandas as pd

def normalize(data_loc, col_name):
    c = False
    dl = []
        
    for data in data_loc:
        if len(data) > 1 or int(data) > 11:
            for i in range(len(data)-1):
                if (data[i] + data[i+1]) in col_name:
                    if (data[i] + data[i+1]) not in dl:
                        dl.append(data[i] + data[i+1])
                        c = False
                else:
                    if data[i] not in dl:
                        dl.append(data[i])
                    c = True
            if c:
                if data[i+1] not in dl:
                    dl.append(data[i+1])
        else:
            if len(data) > 1 and int(data) > 11:
                for d in data:
                    if d not in dl:
                        dl.append(d)
            else:
                if data not in dl:
                    dl.append(data)
                    
    return dl

def loc_of_min(min_val, df):
    min_data_loc = []
    
    i = 0
    for cl in df.columns:
        if min_val in df.iloc[:, i].to_list():
            min_data_loc.append(str(cl))
            break
        i += 1
        
    i = 0
    found = False
    for cl in df.columns:
        j = 0
        if found:
            break
        else:
            for rw in df.index:
                if min_val == df.iloc[i, j]:
                    min_data_loc.append(str(rw))
                    found = True
                    break
                j += 1
            i += 1
            
    return min_data_loc

def main():
    x = [125, 178, 178, 180, 167, 170, 173, 135, 120, 145, 125]
    y = [61, 90, 92, 83, 85, 89, 98, 40, 35, 70, 50]
    max_iter = 4
    
    res = []
    tempRes = []
    
    # Matrix awal
    for i2 in range(0, 11, 1):
        for j1 in range(0, 11, 1):
            tempRes.append(abs(x[i2] - x[j1]) + abs(y[i2] - y[j1]))
            
        res.append(tempRes)
        tempRes = []
    
    df_m = pd.DataFrame(res, columns=[str(i) for i in range(len(x))], index=[str(i) for i in range(len(x))])
    df_tmp = df_m.copy()

    while True:
        col_names = df_m.columns.tolist()
        col_names_ = df_tmp.columns.tolist()
        min_data_loc = []
        new_data = []
        
        # Nilai min pada matrix
        min_val = min(df_tmp[df_tmp > 0].min(axis=1))
        
        # Mencari lokasi nilai minimum pada matrix
        min_data_loc = loc_of_min(min_val, df_tmp)
        
        # Menormalize data lokasi nilai minimum berdasarkan
        # kolom pada matrix awal
        # Ex    : '12345', '6'
        # Res   : '1','2','3','4','5','6'
        normalize_data = normalize(min_data_loc, col_names)

        if len(df_tmp) == max_iter:
            break
        else:
            print('='*60)
            print(f'\n{df_tmp}')
            print(f'\nMin\t: {min_val}\nKelompok: {min_data_loc[0]} dan {min_data_loc[1]}')
            print(f'\nHitung Jarak: ')
        
        # Hitung dman
        for row in col_names_:
            dman = [] 
            
            if row not in min_data_loc:
                if int(row) <= 11 and len(row) < 3:
                    for col in normalize_data:
                        d_col = df_m[col]
                        d_val = d_col[row]
                        dman.append(d_val)
                else:
                    nr_r = normalize([row], col_names)

                    for col in normalize_data:
                        for nr in nr_r:
                            d_col = df_m[nr]
                            d_val = d_col[col]
                            dman.append(d_val)
                        
            if dman:
                dman_min = min(dman)
                new_data.append(dman_min)
                
                print(dman, end='')
                print(f' = {dman_min}')
        
        for i,cn in enumerate(col_names_):
            if cn == min_data_loc[0]:
                new_data.insert(i, 0)
                break

        # Menghapus kolom dan index pada matrix
        # Lalu buat kolom baru dan isi dengan value yang ada
        # pada variable new data
        df_tmp.drop(index=[str(min_data_loc[1])], inplace=True)
        df_tmp.drop(columns=[str(min_data_loc[1])], inplace=True)

        for i in df_tmp.columns:
            if int(i) == int(min_data_loc[0]):
                df_tmp[i] = new_data
                break
        
        j = 0
        for i in df_tmp.columns:
            df_tmp.loc[str(min_data_loc[0]), [i]] = new_data[j]
            j += 1
        
        col_nm = ''.join(x for x in min_data_loc)
        
        df_tmp.rename(columns={min_data_loc[0] : col_nm}, inplace=True)
        df_tmp.rename(index={min_data_loc[0] : col_nm}, inplace=True)
    
    print('\n')
    print('='*30)
    print('Final Result: \n')
    print(df_tmp)    
    
if __name__ == "__main__":
    main()
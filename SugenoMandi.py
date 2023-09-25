import numpy as np
import random as rd
import xlrd
import json
import jsonEncoder

class SugenoMandi:
    def Inputing(info):
        classes = info['classes']
        location_file = info['file']
        wb = xlrd.open_workbook(location_file)
        sheet = wb.sheet_by_index(0)
        row_number = sheet.nrows
        cols_number = sheet.ncols
        n = row_number
        m = cols_number
        
        first_Matrix = np.zeros((n,m))
        for i in range(row_number):
            for j in range(cols_number):
                first_Matrix[i][j] = sheet.cell(i,j).value
        diapasons_class = info['diapasons']
        datas = {}
        datas['first_matrix'] = first_Matrix
        datas['cols_number'] = cols_number
        datas['row_number'] = row_number
        datas['diapasons_class'] = diapasons_class
        datas['classes'] = classes
        return datas
    def calculating_Module(matrix):
        n = matrix['row_number']
        m = matrix['cols_number']
        diapasons_class = matrix['diapasons_class']
        first_Matrix = matrix['first_matrix']
        classes = matrix['classes']
        l = 2
        parametrs = [0,1,2]
        dt = 1
        max_Value = first_Matrix.max()
        min_Value = first_Matrix.min()
        U = np.zeros((n,m))
        index_Maxs = np.zeros((n,m))
        if max_Value-min_Value != 0:
            for i in range(n):
                for j in range(m):
                    U[i][j] = l*((first_Matrix[i][j]-min_Value)/(max_Value-min_Value)) 
        else:
            for i in range(n):
                for j in range(m):
                    U[i][j] = l*(first_Matrix[i][j]-min_Value) 
        summ = 0
        sums = []
        P_M = np.zeros((n,m))
        Maxs = np.zeros((n,m))
        for i in range(n):
            for j in range(m):
                sums.clear()
                for k in parametrs:
                    summ = float(1/(1+(((U[i][j]-k)/dt)**2)))
                    sums.insert(k,summ)
                Maxs[i][j] = max(sums)
                P_M[i][j] = sums.index(max(sums))
        Mu_All = []
        Mu_mins = []
        Mu_maxs = []
        Betta = []
        for i in range(n):
            for k in range(n):
                for q in range(m):
                    s = float(1/(1+((U[i][q]-P_M[k][q])/1)**2))
                    Mu_All.append(s)
            Mu = np.reshape(Mu_All,(n,m))
            Mu_All.clear()
            k = 0
            for diap in diapasons_class:
                while k<diap:
                    Mu_mins.append(min(Mu[k]))
                    k = k+1
                k = diap
                Mu_maxs.append(max(Mu_mins))
                Mu_mins.clear()
            summa = 0
            for q1 in Mu_maxs:
                summa = summa + float(q1)
            
            for q2 in Mu_maxs:
                Betta.append(float(q2/summa))
            Mu_maxs.clear()

        Betta = np.reshape(Betta,(n,classes))
        A1 = []
        k=0
        for i in range(n):
            for j in range(m):
                for q in range(classes):
                    A1.append(float(first_Matrix[i][j])*float(Betta[i][q]))
        A1 = np.reshape(A1,newshape = (n,m*classes))
        A = np.concatenate((Betta,A1),axis=1)
        Y = []
        k = 1
        j = 0
        for i in diapasons_class:
            while j<i:
                Y.append(k)
                j = j + 1
            k=k+1
        A_t = np.transpose(A)
        b1 = np.dot(A_t,A)
        ## there can be singular matrix
        try:
            ## A_1 is A -1 in stepen
            A_1 = np.linalg.inv(b1)
            AT_A_1 = np.dot(A_1,A_t)
        except:
            U, s, V = np.linalg.svd(b1)
            ## this is the s - 1
            s_1 = np.linalg.inv(s)
            ## here U_t is Transparent of the U
            U_t = np.transpose(U)
            AT_A_1 = np.dot(np.dot(V, s_1), U_t)
        B = np.dot(AT_A_1, Y)
        U_1 = np.ones((n,1))
        X = np.concatenate((U_1,first_Matrix),axis=1)
        Ys = []
        BB = []
        
        D = A.dot(B)
        i = 0
        for i in range(classes):
            for q in range(i,classes*(m+1),classes):
                BB.append(B[q])
        BB = np.reshape(BB,(classes,m+1))
        ds = []
        summa = 0
        for r in range(n):
            for i in range(classes):
                for j in range(m+1):
                    summa = summa + Betta[r][i]*BB[i][j]*X[r][j]
            Ys.append(summa)
            summa = 0
        Ys = np.reshape(Ys,(n,1))
        D = np.reshape(D,(n,1))
        data = {}
        data['B'] = BB
        data['Bettas'] = Betta
        dumped = json.dumps(data,cls = jsonEncoder.NumpyEncoder)
        with open('train.json','w') as jsonFile:
            json.dump(dumped, jsonFile)
        return data
def reproduce_vs_google():
    local = [False, False, False, False, False, False, True, False, False, True, False, False, True, False, False, False, True, True, False, False, False, False, True, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, True, True, False, False, False, False, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, True, True, False, False, True, False, False, False, False, False, False, False, False]
    # print(len(local))
    google = [False, False, False, False, False, False, True, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, True, True, False, False, False, False, False, True, True, False, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False]
    # print(len(google))
    assert len(local) == len(google)
    n = len(local)
    res_local = [1 if local[0]==True else 0]
    res_google = [1 if google[0]==True else 0]
    for i in range(1,n):
        if local[i]==True:
            res_local.append(res_local[-1]+1)
        else:
            res_local.append(res_local[-1])
        if google[i]==True:
            res_google.append(res_google[-1]+1)
        else:
            res_google.append(res_google[-1])
    print(res_local)
    print(res_google)
    col = [i for i in range(1,n+1)]
    df = pd.DataFrame({'Case':col, 'OSS Reproducer':res_local})
    df = df.join(pd.DataFrame({'Google':res_google}))
    df.to_csv(r'../Data/vsgoogle.csv', index=False)
    print("[+] Exported to vsgoogle.csv\n")
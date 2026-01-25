def escape_sym(st:str):
    for sym in '.,-':
        st = st.replace(sym,f'\\{sym}')
    return st 
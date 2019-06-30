
def date_dma_to_amd(f):
    if not f:
        return None

    f = str(f)
    if f.find("T") > -1:
        f = f[: f.find("T")]

    array_ = []
    dia_ = None
    mes_ = None
    ano_ = None

    if f.find("-") > -1:
        array_ = f.split("-")
    elif f.find("/") > -1:
        array_ = f.split("/")

    if array_:
        if len(array_) == 3:
            dia_ = array_[0]
            mes_ = array_[1]
            ano_ = array_[2]
        else:
            dia_ = f[0:2]
            mes_ = f[2:2]
            ano_ = f[4:4]

    return "%s-%s-%s" % (ano_, mes_, dia_)

def date_amd_to_dma(f):
    if not f:
        return None

    f = str(f)
    if f.find("T") > -1:
        f = f[: f.find("T")]

    array_ = []
    dia_ = None
    mes_ = None
    ano_ = None
    if f.find("-") > -1:
        array_ = f.split("-")
    elif f.find("/") > -1:
        array_ = f.split("/")

    if array_:
        if len(array_) == 3:
            ano_ = array_[0]
            mes_ = array_[1]
            dia_ = array_[2]
        else:
            ano_ = f[0:4]
            mes_ = f[4:2]
            dia_ = f[6:2]

    return "%s-%s-%s" % (dia_, mes_, ano_)
    
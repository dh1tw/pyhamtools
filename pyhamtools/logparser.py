import os
import re
from datetime import datetime

def import_cabrillo(filename):
    log = None;
    log_import = None
    with open(filename, 'r') as f:
        log_import = f.read()
    log = []
    log_import = log_import.split("\r\n")

    for qso in log_import:

        if re.match("^QSO", qso):
            freq = int(qso[4:11])
            mode = qso[11:13]
            time = datetime.strptime(qso[14:29], "%Y-%m-%d %H%M")
            frm = qso[30:44].strip()
            sent_rst = int(qso[44:47])
            sent_exchange = qso[48:55].strip()
            qso_partner = qso[55:68].strip()
            rcvd_rst = int(qso[69:72])
            rcvd_exchange = qso[73:79].strip()
            station = int(qso[80])
            log.append({
                "freq": freq,
                "mode":mode,
                "time":time,
                "from": frm,
                "sent_rst":sent_rst,
                "sent_exchange": sent_exchange,
                "qso_partner": qso_partner,
                "rcvd_rst": rcvd_rst,
                "rcvd_exchange": rcvd_exchange,
                "station": station
             })
    return log
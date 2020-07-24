import sys

sys.path.append('./..')
sys.path.append('./../..')

from flask import render_template


def render():
    # --------------------
    # read in List of IPs
    # --------------------
    with open("./../data/MainData/Processed/VALID_IP_LIST.txt", "r") as fh:
        ip_list = fh.readlines()
    ip_list = [ip.strip('\n') for ip in ip_list]
    sys.stdout.flush()

    _dict = {
        'IP_List': ip_list
    }
    return render_template('generatedData_page.html', **_dict)

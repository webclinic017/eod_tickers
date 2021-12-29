import requests
import datetime
import pandas as pd
from pandas.api.types import is_number
from urllib.parse import urlencode


def _init_session(session):
    """
    Returns a requests.Session (or CachedSession)
    """
    if session is None:
        return requests.Session()
    return session


def _url(url, params):
    """
    Returns long url with parameters
    http://mydomain.com?param1=...&param2=...
    """
    if params is not None and len(params) > 0:
        return url + "?" + urlencode(params)
    else:
        return url


class RemoteDataError(IOError):
    """
    Remote data exception
    """
    pass


def _format_date(dt):
    """
    Returns formated date
    """
    if dt is None:
        return dt
    return dt.strftime("%Y-%m-%d")


def _sanitize_dates(start, end):
    """
    Return (datetime_start, datetime_end) tuple
    """
    if is_number(start):
        # regard int as year
        start = datetime.datetime(start, 1, 1)
    start = pd.to_datetime(start)

    if is_number(end):
        # regard int as year
        end = datetime.datetime(end, 1, 1)
    end = pd.to_datetime(end)

    if start is not None and end is not None:
        if start > end:
            raise Exception("end must be after start")

    return start, end

tickers_to_skip = ['GRUI:US', 'GRYEF:US', 'GRYG:US', 'GRZZP:US', 'GS-PA:US', 'GS-PC:US', 'GS-PD:US', 'GS-PJ:US', 'GS-PK:US', 'GSAH:US', 'GSDC:US', 'GSEFF:US', 'GSFD:US', 'GSGTF:US', 'GSIH:US', 'GSL-PB:US', 'GSLO:US', 'GSML:US', 'GSNC:US', 'GSPH:US', 'GSQD-U:US', 'GSQD-WS:US', 'GSRX:US', 'GSUXF:US', 'GSVI:US', 'GTCP:US', 'GTGT:US', 'GTLA:US', 'GTMEF:US', 'GTMEY:US', 'GTMIF:US', 'GTN-A:US', 'GTRL:US', 'GTTN:US', 'GUAA:US', 'GUFAF:US', 'GUOHF:US', 'GUT-PA:US', 'GUT-PC:US', 'GV:US', 'GVFF:US', 'GVFG:US', 'GVHIB:US', 'GWH-WS:US', 'GWIO:US', 'GWMGF:US', 'GWOX:US', 'GWPC:US', 'GWYT:US', 'GXO-W:US', 'GXSBF:US', 'GXSBY:US', 'GYC:US', 'GYPHQ:US', 'GYSN:US', 'GYUAF:US', 'GZCC:US', 'GZPZY:US', 'HABC:US', 'HABK:US', 'HACBF:US', 'HACBY:US', 'HAHI:US', 'HAIPF:US', 'HALN:US', 'HARY:US', 'HASGF:US', 'HAZAF:US', 'HAZH:US', 'HBBHF:US', 'HBMBF:US', 'HBMK:US', 'HBPE:US', 'HBTC:US', 'HBUV:US', 'HCBP:US', 'HCCA:US', 'HCEI:US', 'HCGS:US', 'HCKG:US', 'HCLC:US', 'HCPHF:US', 'HCXLF:US', 'HDIH:US', 'HEC:US', 'HEHSF:US', 'HEI-A:US', 'HERC:US', 'HEXEY:US', 'HFBG:US', 'HFGVF:US', 'HFIAF:US', 'HFRO-PA:US', 'HGGGQ:US', 'HGLC:US', 'HGTY-WS:US', 'HHBHF:US', 'HHBT:US', 'HHER:US', 'HHGI:US', 'HHLA-U:US', 'HHLA-WS:US', 'HHSRF:US', 'HIBRF:US', 'HIG-PG:US', 'HIGA-U:US', 'HIGA-WS:US', 'HIGR:US', 'HIMS-WS:US', 'HINOF:US', 'HINOY:US', 'HISJF:US', 'HITD:US', 'HIZOF:US', 'HKBT:US', 'HKBV:US', 'HKUOF:US', 'HKUOY:US', 'HKWO:US', 'HL-PB:US', 'HLCN:US', 'HLLF:US', 'HLLY-WS:US', 'HLMB:US', 'HLMNY:US', 'HLOI:US', 'HLOSF:US', 'HLPMF:US', 'HLRD:US', 'HLTEF:US', 'HLTY:US', 'HLUN:US', 'HLVTY:US', 'HMAGF:US', 'HMBG:US', 'HMGN:US', 'HMLP-PA:US', 'HMNKF:US', 'HMRZF:US', 'HMTLF:US', 'HMTLY:US', 'HNFSB:US', 'HNHAF:US', 'HNHPF:US', 'HNTHF:US', 'HNTM:US', 'HOFBF:US', 'HOFJF:US', 'HOFVW:US', 'HOIEF:US', 'HOILF:US', 'HOKCF:US', 'HOKCY:US', 'HOKUQ:US', 'HOLI:US', 'HOLX:US', 'HOMB:US', 'HOMU:US', 'HON:US', 'HONE:US', 'HONT:US', 'HOOB:US', 'HOOD:US', 'HOOK:US', 'HOPE:US', 'HOPHF:US', 'HORIU:US', 'HOSXF:US', 'HOTF:US', 'HOTH:US', 'HOV:US', 'HOYFF:US', 'HPHTF:US', 'HPP-P-C:US', 'HPTN:US', 'HPURF:US', 'HQGE:US', 'HQI:US', 'HQL:US', 'HQY:US', 'HR:US', 'HRAA:US', 'HRAL:US', 'HRB:US', 'HRBK:US', 'HRBR:US', 'HRC:US', 'HRCR:US', 'HRCXF:US', 'HRDDF:US', 'HRDI:US', 'HRDIL:US', 'HRIBF:US', 'HRLDF:US', 'HROEY:US', 'HRPMF:US', 'HRSEF:US', 'HRSR:US', 'HRST:US', 'HRTT:US', 'HRVFF:US', 'HSCHF:US', 'HSCM:US', 'HSCO:US', 'HSEN:US', 'HSFI:US', 'HSHIF:US', 'HSHZY:US', 'HSITF:US', 'HSTG:US', 'HT-PC:US', 'HT-PD:US', 'HT-PE:US', 'HTCKF:US', 'HTCMF:US', 'HTCMY:US', 'HTDS:US']
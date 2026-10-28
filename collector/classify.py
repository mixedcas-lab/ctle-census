"""Classification and spec extraction for continuous-time linear equalizer (CTLE) papers.

Pure functions (no network, no files) so they can be unit-tested and re-run over the
cached records whenever the rules change. Abstracts are inputs only; they are never
written to the output.
"""
import re

I = re.IGNORECASE

# ---------------------------------------------------------------- relevance
# the equalizer named in the title: CTLE, or a linear/analog equalizer (the name used before "CTLE" caught on)
CTLE = re.compile(r"\bCTLEs?\b|continuous[- ]time (?:linear |analog |adaptive )?equali[sz]|"
                  r"\b(?:linear|analog(?:ue)?|passive|active|inductorless|inductor[- ]less|cable|line|"
                  r"high[- ]frequency[- ]boost(?:ing)?|peaking|gm[- ]C|RC[- ]degenerated)[- ]equali[sz]", I)
# CTLE work without the word: spectrum-balancing adaptation, analog peaking stages
RESCUE = re.compile(r"spectrum[- ]balanc\w* (?:adaptive )?equali|analog peaking|peaking control|active[- ]inductor(?:[- ]based)? equali", I)
# a bare "equalizer" in a wireline title is analog unless it says otherwise
EQ = re.compile(r"\bequali[sz](?:er|ers|ation|ing)\b", I)
NOT_LINEAR = re.compile(r"decision[- ]feedback|transmit|finite impulse|\bDFEs?\b|feed[- ]?forward|\bFFEs?\b|\bFIR\b|digital|discrete[- ]time|"
                        r"\b\d+[- ]tap|taps?\b|crosstalk|\bXTC\b|transmitters?|\bTX\b|pre[- ]?emphasis|de[- ]?emphasis|"
                        r"\bMLSD\b|Viterbi|\bDSP\b|ADC[- ]based|switched[- ]capacitor|charge[- ]domain|oversampl|decision|transversal|"
                        r"phase|jitter|timing|clock|duty[- ]cycle|skew|delay[- ]line|IIR|algorithm", I)
# the link context of a bare "equalizer"
WIRE = re.compile(r"wireline|SerDes|\bPAM[- ]?\d|\bNRZ\b|duobinary|Gb/s|Gbps|Tb/s|GBaud|GBd|Mb/s|backplane|"
                  r"chip[- ]to[- ]chip|die[- ]to[- ]die|serial|links?\b|\bI/Os?\b|transceivers?|receivers?|\bRX\b|"
                  r"copper|cable|coax|twisted[- ]pair|PCB|interconnect|channel|PCIe|Ethernet|\bUSB\b|DisplayPort|\bHDMI|\bMIPI|"
                  r"\bHBM|\bGDDR|\bLPDDR|\bDDR\d|memory interface|optical|\bVCSEL|photo|\bTIA\b|transimpedance|"
                  r"limiting amplifier|data[- ]rate", I)
# radio links share words like "receiver" and "Gb/s"
WIRELESS = re.compile(r"wireless|\bRF\b|radio|mm-?wave|millimeter|\b[56]G\b|antenna|\bLNA\b|phased[- ]array|beamform|"
                      r"D-band|W-band|E-band|sub-THz|terahertz|THz|radar|\bBLE\b|Wi-?Fi|UWB|"
                      r"body[- ]channel|\bNFC\b|optical wireless|backscatter|uplink|downlink|baseband|cellular|MIMO|"
                      r"audio|acoustic|hearing|speaker|loudspeaker|video|image|display driver|"
                      r"\bLDO\b|regulator|converter|charger|power amplifier|\bPA\b", I)
NON_PAPER = re.compile(
    r"^(front cover|back cover|table of contents|contents|author index|index|"
    r"call for papers|editorial|guest editorial|reviewers|session \d+ overview|session \d+\s*[-:]\s*(?=\w)|comments on|"
    r"(?:tutorials?|short course|evening (?:event|session)|forum|panel)(?=\s*:|\s*$)|"
    r"(ieee )?(transactions|journal) .*information|blank page|copyright)\b", I)
# a CTLE named in the abstract of a link paper
CTLE_ABS = re.compile(r"\bCTLEs?\b|continuous[- ]time (?:linear |analog )?equali[sz]|"
                      r"\b(?:linear|analog(?:ue)?|passive|active|high[- ]frequency[- ]boost(?:ing)?|peaking) equali[sz]", I)
LINK = re.compile(r"transceivers?|receivers?|\bRX\b|SerDes|\bPHY\b|serial (?:link|I/O)|links?\b|\bI/Os?\b|interfaces?|"
                  r"\bCDRs?\b|clock and data recovery|equaliz\w*|\bDFE\b|\bFFE\b|retimers?|repeaters?|redrivers?|"
                  r"analog front[- ]ends?|\bAFE\b|\bTIAs?\b|transimpedance|limiting amplifiers?", I)
LINK_CTX = re.compile(r"wireline|SerDes|\bPAM[- ]?\d|\bNRZ\b|Gb/s|Gbps|Tb/s|GBaud|backplane|chip[- ]to[- ]chip|die[- ]to[- ]die|"
                      r"serial|\bCDR\b|\bDFE\b|\bFFE\b|copper|cable|PCIe|Ethernet|\bUSB\b|\bHBM|\bGDDR|\bLPDDR|\bDDR\d|"
                      r"memory interface|optical|\bVCSEL|photonic|interconnect|DisplayPort|\bHDMI|\bMIPI", I)


# not a link equalizer although the title says so
OFF_TOPIC = re.compile(r"side[- ]channel|\bAES\b|security|SRAM|bit[- ]?line|Ising|intermodulation|\bIM3\b|direct[- ]conversion|"
                       r"chao(?:s|tic)|blind|theorem|neural|\bMMSE\b|model predictive|channelizer|\bEDGE\b|signal processing|"
                       r"\bDLMS\b|\bFEXT\b|\bNEXT\b|trellis|decoder|line coding|encoding|equalizer[- ]free|pulse[- ]width|"
                       r"biomedical|\bEEG\b|\bECG\b|sensor|drivers?\b|laser|modulator|nonlinear equaliz|pre[- ]equaliz", I)
# a title that is about the whole link, where "equalization" may be any equalizer (TX FFE, DFE, ...)
LINK_TITLE = re.compile(r"transceivers?|receivers?|\bRX\b|\bTRX\b|SerDes|interfaces?|DRAM|\bPHY\b|links?\b|\bCDRs?\b|"
                        r"\bI/Os?\b|chiplets?|front[- ]ends?|macro|\bTIA\b|repeaters?", I)
# the abstract shows the equalizer is analog and continuous-time
ANALOG_ABS = re.compile(r"\bCTLE|continuous[- ]time|analog|peaking|zeros?\b|boost|inductor|degenerat|high[- ]frequency gain", I)
# ... or that it is a DFE, FIR or digital equalizer
DIGITAL_ABS = re.compile(r"decision[- ]feedback|\bDFE|\bFIR\b|finite impulse|\btaps?\b|digital|\bMIMO\b|frequency[- ]domain|speculative", I)


def relevance(title, abstract):
    """'core': the title is about a CTLE (or a linear/analog equalizer of a wired link).
    'rx': a wireline receiver or transceiver that uses a CTLE (named in the abstract). None otherwise."""
    t, a = title or "", abstract or ""
    if WIRELESS.search(t) and not re.search(r"wireline|SerDes|serial link|backplane|cable|chip[- ]to[- ]chip|die[- ]to[- ]die|\bCTLE", t, I):
        return None
    if re.search(r"Ising|SRAM|bit[- ]?line", t, I):
        return None
    if CTLE.search(t) or RESCUE.search(t):
        return "core"
    if OFF_TOPIC.search(t):
        return None
    # a bare "equalizer": analog unless the title or abstract says otherwise
    if EQ.search(t) and WIRE.search(t) and not NOT_LINEAR.search(t):
        if re.search(r"\bequali[sz]ers?\b", t, I) or not LINK_TITLE.search(t):
            if ANALOG_ABS.search(a) or not DIGITAL_ABS.search(a):
                return "core"           # the equalizer is the subject of the title
        elif ANALOG_ABS.search(a):
            return "rx"                 # "a transceiver with ... equalization"
    if CTLE_ABS.search(a) and LINK.search(t) and LINK_CTX.search(t):
        return "rx"
    return None


# ------------------------------------------------------------- technique / application / modulation
ARCH_RULES = [
    ("Inductive peaking",   r"inductive[- ]peaking|inductor|inductance|T[- ]coil|\bLC\b|shunt[- ]peak|series[- ]peak"),
    ("Passive",             r"passive (?:CTLE|equaliz|linear)|passive[- ]network|\bRLC\b network"),
    ("RC degeneration",     r"source[- ]degenerat|RC[- ]degenerat|capacitive[- ]degenerat|degenerated|degeneration"),
    ("Active feedback",     r"active[- ]feedback|Cherry[- ]Hooper|negative[- ](?:capacitance|impedance|resistance|Miller)|"
                            r"capacitance[- ]cancel|(?<!decision )(?<!decision-)\bfeedback (?:CTLE|equaliz|amplifier)"),
    ("Multi-path",          r"multi[- ]?path|dual[- ]path|parallel[- ]path|split[- ]path|two[- ]path|feed[- ]?forward (?:CTLE|path|zero)|"
                            r"forward[- ]path"),
    ("Multi-stage",         r"multi[- ]stage|cascaded|two[- ]stage|three[- ]stage|2[- ]stage|3[- ]stage"),
    ("Low/mid-frequency EQ", r"low[- ]frequency equaliz|\bLFEQ\b|mid[- ]frequency|long[- ]tail|low[- ]frequency (?:zero|boost|peaking)"),
    ("Inverter-based",      r"inverter[- ]based|CMOS inverter|current[- ]reuse|current[- ]reused"),
    ("With DFE",            r"\bDFE\b|decision[- ]feedback"),
    ("With FFE",            r"\bFFE\b|feed[- ]?forward equaliz|\bFIR\b"),
    ("Optical (TIA)",       r"\bTIA\b|transimpedance|photodiode|optical receiver"),
]
ARCH_RX = [(n, re.compile(p, I)) for n, p in ARCH_RULES]

MOD_RULES = [("NRZ", r"\bNRZ\b|PAM[- ]?2\b"), ("PAM3", r"PAM[- ]?3\b"), ("PAM4", r"PAM[- ]?4\b|\b4[- ]PAM"),
             ("PAM6", r"PAM[- ]?6\b"), ("PAM8", r"PAM[- ]?8\b"), ("Duobinary", r"duo[- ]?binary|Duo[- ]PAM")]
MOD_RX = [(n, re.compile(p, I)) for n, p in MOD_RULES]


def _first(abstract, n=2):
    return " ".join(re.split(r"(?<=[.!?])\s+", abstract or "")[:n])


def architectures(title, abstract):
    """Circuit techniques named in the title or the first three sentences of the abstract."""
    def scan(text):
        return [n for n, rx in ARCH_RX if rx.search(text or "")]
    tags = scan(title)
    for t in scan(_first(abstract, 3)):
        if t not in tags:
            tags.append(t)
    return tags


def modulations(title, abstract):
    first = _first(abstract)
    return [n for n, rx in MOD_RX if rx.search(title or "") or rx.search(first)]


APP_RULES = [
    ("Long-reach/backplane", r"long[- ]reach|\bLR\b|backplane|[3-9]\d(?:\.\d)?[- ]?dB[- ](?:channel[- ]|insertion[- ])?loss|loss (?:of |exceeding |over |beyond )?>?\s?[3-9]\d[- ]?dB|copper cable|\bCEI\b|\bKR\b"),
    ("Cable",                r"cable|coax|twisted[- ]pair|\bUTP\b"),
    ("Optical/data center",  r"optical|VCSEL|photonic|photodiode|data[- ]?center|co[- ]packaged|\bCPO\b|\bLPO\b|\bTIA\b"),
    ("Die-to-die/chiplet",   r"die[- ]to[- ]die|\bD2D\b|chiplet|\bUCIe|interposer|2\.5[- ]?D|short[- ]reach|\bXSR\b|\bUSR\b"),
    ("Memory interface",     r"\bHBM|\bGDDR|\bLPDDR|\bDDR\d|DRAM|memory interface"),
    ("PCIe/Ethernet/USB",    r"PCIe|PCI Express|Ethernet|\bUSB\b|Thunderbolt"),
    ("Display/automotive",   r"display|\bHDMI|DisplayPort|\bMIPI|automotive|in[- ]vehicle"),
    ("Storage read channel", r"read channel|disk drive|magnetic|tape drive|\bPRML\b"),
]
APP_RX = [(n, re.compile(p, I)) for n, p in APP_RULES]
ADAPT_RX = re.compile(r"adaptive|adaptation|adapt(?:s|ed)\b|\bLMS\b|\bSS-LMS\b|spectrum[- ]balanc|eye[- ]opening monitor|"
                      r"background calibrat|self[- ]calibrat|auto(?:matic)?[- ](?:tun|adjust)", I)


def applications(title, abstract):
    text = (title or "") + " " + (abstract or "")
    return [n for n, rx in APP_RX if rx.search(text)]


def is_adaptive(title, abstract):
    return bool(ADAPT_RX.search((title or "") + " " + (abstract or "")))


# ------------------------------------------------------------- spec parsing
NUM = r"(\d+(?:\.\d+)?)"
_SI = {"a": 1e-18, "f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "μ": 1e-6,
       "m": 1e-3, "": 1.0, "k": 1e3, "K": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}
_RNG = r"(?:" + NUM + r"\s*(?:-|–|to|-to-)\s*)?"
RATE_RX = re.compile(r"(?<![\w.])" + _RNG + NUM + r"\s*-?\s*([MGT])\s?(?:b/s|bps|b/s/pin|bit/s)\b", I)
LOSS_RX = [re.compile(r"(?:>|over|up to|beyond|exceeding|of)?\s*" + NUM + r"\s*-?\s*dB(?:[- ](?:channel[- ])?(?:loss|insertion loss|attenuation)| (?:of )?(?:channel )?loss)", I),
           re.compile(r"(?:loss|insertion loss|attenuation)(?: of)?\s*(?:>|over|up to|exceeding)?\s*" + NUM + r"\s*-?\s*dB", I)]
# the equalizer's own high-frequency boost (peaking gain); "X-dB loss" is the channel, not the boost
_BOOST_WORD = r"(?:peaking|boost(?:ing)?|equali[sz]ation(?: range| gain)?|high[- ]frequency gain|(?:AC|peak) gain)"
BOOST_RX = [re.compile(NUM + r"\s*-?\s*dB(?:\s+of)?\s+(?:of\s+)?(?:maximum\s+|max\.?\s+|high[- ]frequency\s+)?" + _BOOST_WORD, I),
            re.compile(_BOOST_WORD + r"(?:\s+\w+){0,2}?\s+(?:of|up to|over|exceeding|is|reaches|>|=)?\s*(?:up to\s+|over\s+|>\s*)?" + NUM + r"\s*-?\s*dB(?![- ]?(?:\w+[- ])?(?:loss|insertion|attenuation|channel))", I)]
NODE_NM_RX = re.compile(r"(?<![\w.])(\d{1,3})\s*-?\s*nm\b", I)
NODE_UM_RX = re.compile(r"(?<![\w.])(0\.\d{1,3})\s*-?\s*[µμu]m\b", I)
POWER_VAL = NUM + r"\s*-?\s*([nuµμm]?)W\b(?!\s*/)"
POWER_CTX_RX = re.compile(r"(?:consum\w*|dissipat\w*|power(?:\s+consumption)?|draw(?:s|ing)|drains?|burns?)[^.;]{0,40}?" + POWER_VAL, I)
POWER_AFTER_RX = re.compile(POWER_VAL + r"\s*(?:of\s+)?(?:total\s+|overall\s+)?(?:power|consumption|dissipation)", I)
POWER_TITLE_RX = re.compile(POWER_VAL)
AREA_RX = re.compile(NUM + r"\s*-?\s*mm\s*(?:2|²|\^2)", I)
_FIXES = [(re.compile(r"(\d)\.\s(\d)"), r"\1.\2"), (re.compile(r"(\d)\s*-?\s*mu(m|W|A|V|s|J)\b"), r"\1 µ\2"),
          (re.compile(r"([µμ])\s+m\b"), r"\1m"), (re.compile(r"\\?hbox\s*"), ""), (re.compile(r"Gbps", I), "Gb/s"),
          (re.compile(r"Mbps", I), "Mb/s")]


def _norm(text):
    for rx, rep in _FIXES:
        text = rx.sub(rep, text)
    return text


def _vals(rxs, text, conv, lo, hi):
    """Every plausible value (rounded to 3 significant digits for comparison)."""
    out = {}
    for rx in rxs:
        for m in rx.finditer(text or ""):
            try:
                v = conv(m)
            except (ValueError, KeyError):
                continue
            if v is not None and lo <= v <= hi:
                out.setdefault(float("%.3g" % v), v)
    return set(out.values())


def _pick(t, a, cands, best=max):
    """The title's value if it states one, else the abstract's only value; nothing when the abstract lists several."""
    vt, va = cands(t), cands(a)
    if vt:
        return best(vt)
    if len(va) == 1:
        return va.pop()
    return None


def _rate(m):
    return float(m.group(2)) * _SI[m.group(3).upper()]


def parse_specs(title, abstract):
    t, a = _norm(title or ""), _norm(abstract or "")
    out = {}

    def put(k, v):
        if v is not None:
            out[k] = v
    put("rate", _pick(t, a, lambda x: _vals([RATE_RX], x, _rate, 1e8, 5e12)))
    put("loss", _pick(t, a, lambda x: _vals(LOSS_RX, x, lambda m: float(m.group(1)), 3, 80)))
    put("boost", _pick(t, a, lambda x: _vals(BOOST_RX, x, lambda m: float(m.group(1)), 1, 60)))
    put("node", _pick(t, a, lambda x: _vals([NODE_NM_RX], x, lambda m: int(m.group(1)), 2, 500)
                      or _vals([NODE_UM_RX], x, lambda m: int(round(float(m.group(1)) * 1000)), 10, 1000)))
    put("p", _pick(t, a, lambda x: _vals([POWER_TITLE_RX] if x is t else [POWER_CTX_RX, POWER_AFTER_RX], x,
                                         lambda m: float(m.group(1)) * _SI[m.group(2) or ""], 1e-6, 1e2)))
    put("area", _pick(t, a, lambda x: _vals([AREA_RX], x, lambda m: float(m.group(1)), 1e-4, 1e3)))
    return out


def spec_sources(title, abstract):
    """parse_specs() plus where each value came from: {"key": "t" | "a"}."""
    full = parse_specs(title, abstract)
    only_title = parse_specs(title, "")
    return full, {k: ("t" if only_title.get(k) == v else "a") for k, v in full.items()}


# ------------------------------------------------------------- affiliations and dates (same rules as adc-census)
ORG_HINT = re.compile(r"universit|institut|college|school|KAIST|POSTECH|UNIST|DGIST|GIST|\bETH\b|EPFL|\bMIT\b|"
                      r"laborator|\blabs?\b|inc\b|ltd|corp|company|co\.|electronics|semiconductor|technolog|"
                      r"research|centre|center|academy|imec|tsmc|samsung|sk hynix|intel|mediatek|qualcomm|"
                      r"apple|google|huawei|broadcom|analog devices|texas instruments|nvidia|\bamd\b|\bibm\b|microsoft", I)


def org_and_country(aff):
    if not aff:
        return None, None
    parts = [p.strip() for p in aff.split(",") if p.strip()]
    if not parts:
        return None, None
    country = re.sub(r"\s+\d[\d\- ]*$", "", parts[-1])
    if re.fullmatch(r"(korea|south korea|republic of korea|korea \(south\))", country, I):
        country = "South Korea"
    elif re.fullmatch(r"(usa|u\.s\.a\.|united states|united states of america|us)", country, I):
        country = "USA"
    elif re.fullmatch(r"(prc|p\.r\. china|people's republic of china)", country, I):
        country = "China"
    org = None
    for p in parts:
        if ORG_HINT.search(p) and not re.match(r"(department|dept|school of|faculty|division)\b", p, I):
            org = p
            break
    if org is None:
        org = parts[1] if len(parts) > 2 else parts[0]
    if len(country) > 30 or re.search(r"\d", country):
        country = None
    return org, country


MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def parse_month(pubdate, year):
    s = (pubdate or "").lower()
    m = re.match(r"((?:19|20)\d{2})-(\d{2})", s)     # ISO dates from Crossref/OpenAlex
    if m:
        return "%s-%s" % m.groups()
    years = re.findall(r"(?:19|20)\d{2}", s)
    y = years[-1] if years else (str(year) if year else None)
    mon = None
    for tok in re.findall(r"[a-z]{3,}", s):
        if tok[:3] in MONTHS:
            mon = MONTHS[tok[:3]]
            break
    if y and mon:
        return "%s-%02d" % (y, mon)
    return y or ""

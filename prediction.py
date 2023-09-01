from contextlib import suppress
from pronounciation_map import map
from numpy import exp
from config import DEBUG

sus_tlds = ("win", "pw", "bid", "ph", "zip", "rs", "top", "ro", "biz", "tk", "cc", "io", "fi", "to", "website", "info",
            "ru", "help", "wang", "mx")
impersonate_list = ('gmail', 'ebay', 'apple', 'avast', 'microsoft', 'google', 'facebook', 'airbnb', 'netflix', 'icloud',
                    'amazon', 'gouv', 'gov', 'paypal', 'iphone', 'office365', 'minecraft', 'itunes')
finance_list = ('business', 'exchange', 'sales', 'casino', 'bank', 'cash', 'payment', 'remboursement', 'billing',
                'wallet', 'free', 'giveaway', 'crypto')
others_list = ('security', 'register', 'secur', 'server', 'download', 'auth', 'ddos', 'private', 'update', 'love',
               'beauty', 'admin', 'verify', 'warning', 'recovery', 'system', 'confirmation', 'alert', 'lock',
               'identity',
               'protection', 'hacking')


def keywords(domain, words_list):
    level = 0
    for w in words_list:
        if w in domain:
            level += 1
    return level


def numbers(domain):
    level = 0
    for c in domain:
        if c.isdigit():
            level += 1
    if level <= .2*len(domain): return 0
    return .2*(level-.2*len(domain))


def TLD(domain):
    level = 0
    tld = domain.split(".")[-1]
    if tld in sus_tlds:
        level = 1
    return level


vowels = ("a", "e", "i", "o", "u")


def pro_domain(domain_txt):
    score = 0
    domain = domain_txt.split(".")
    size = 0
    for e in domain:
        size += len(e)
    for word in domain[:-1]:
        wscore = 0
        word = word.lower()
        for i in range(0, len(word) - 1):
            with suppress(KeyError):
                if not word[i + 1] in map[word[i]]:
                    wscore += 1
        score += wscore ** 2 / (len(word) / 1.5)
    vowels_c = 0
    for c in domain_txt:
        if c in vowels:
            vowels_c += 1
    if vowels_c > len(domain_txt.replace(".", "")) * 0.5:
        score *= (vowels_c * 6 / len(domain_txt.replace(".", "")))
    return score


def scanDomain(domain):
    score = -2.3616
    score += pro_domain(domain) * 0.65
    score += numbers(domain) * 0.1108
    score += TLD(domain) * 2.75
    score += keywords(domain, impersonate_list) * 0.45
    score += keywords(domain, finance_list) * 0.25
    score += keywords(domain, others_list) * 0.13
    return 1 / (1 + exp(-score))
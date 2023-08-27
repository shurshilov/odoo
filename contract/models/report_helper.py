import re
from datetime import datetime

from pytils import dt, numeral


class Helper:
    def numer(self, name):
        if name:
            numeration = re.findall(r"\d+$", name)
            if numeration:
                return numeration[0]
        return ""

    def ru_date(self, date):
        if date and date != "False":
            return dt.ru_strftime(
                '"%d" %B %Y года',
                date=datetime.strptime(str(date), "%Y-%m-%d"),
                inflected=True,
            )
        return ""

    def ru_date2(self, date):
        if date and date != "False":
            return dt.ru_strftime(
                "%d %B %Y г.",
                date=datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S"),
                inflected=True,
            )
        return ""

    def in_words(self, number):
        return numeral.in_words(number)

    def rubles(self, sum):
        "Transform sum number in rubles to text"
        text_rubles = numeral.rubles(int(sum))
        copeck = round((sum - int(sum)) * 100)
        text_copeck = numeral.choose_plural(
            int(copeck), ("копейка", "копейки", "копеек")
        )
        return ("%s %02d %s") % (text_rubles, copeck, text_copeck)

    def initials(self, fio):
        if fio:
            return (
                fio.split()[0]
                + " "
                + "".join([fio[0:1] + "." for fio in fio.split()[1:]])
            ).strip()
        return ""

    def address(self, partner):
        repr = []
        if partner.zip:
            repr.append(partner.zip)
        if partner.city:
            repr.append(partner.city)
        if partner.street:
            repr.append(partner.street)
        if partner.street2:
            repr.append(partner.street2)
        return ", ".join(repr)

    def representation(self, partner):
        repr = []
        if partner.name:
            repr.append(partner.name)
        if partner.inn:
            repr.append("ИНН " + partner.inn)
        if partner.kpp:
            repr.append("КПП " + partner.kpp)
        repr.append(self.address(partner))
        return ", ".join(repr)

    def full_representation(self, partner):
        repr = [self.representation(partner)]
        if partner.phone:
            repr.append("тел.: " + partner.phone)
        elif partner.parent_id.phone:
            repr.append("тел.: " + partner.parent_id.phone)
        bank = None
        if partner.bank_ids:
            bank = partner.bank_ids[0]
        elif partner.parent_id.bank_ids:
            bank = partner.parent_id.bank_ids[0]
        if bank and bank.acc_number:
            repr.append("р/сч " + bank.acc_number)
        if bank and bank.bank_name:
            repr.append("в банке " + bank.bank_name)
        if bank and bank.bank_bic:
            repr.append("БИК " + bank.bank_bic)
        if bank and bank.bank_corr_acc:
            repr.append("к/с " + bank.bank_corr_acc)
        return ", ".join(repr)
